# =============================================================
# alignment/controllers/service.py — Alignment Tree business logic
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.alignment.models.entity import AlignmentNode
from app.alignment.models.schema import NodeCreate, NodeUpdate


async def get_tree(db: AsyncSession, plan_id: uuid.UUID) -> list[AlignmentNode]:
    result = await db.execute(
        select(AlignmentNode)
        .where(AlignmentNode.plan_id == plan_id)
        .order_by(AlignmentNode.sort_order)
    )
    return list(result.scalars().all())


async def add_node(db: AsyncSession, plan_id: uuid.UUID, data: NodeCreate) -> AlignmentNode:
    node = AlignmentNode(
        plan_id=plan_id,
        parent_id=data.parent_id,
        node_level=data.node_level,
        code=data.code,
        title=data.title,
        owner=data.owner,
        bsc_perspective=data.bsc_perspective,
        progress_pct=data.progress_pct,
        status=AlignmentNode.traffic_light(data.progress_pct),
        resource_category=data.resource_category,
        budget_amount=data.budget_amount,
        headcount_fte=data.headcount_fte,
        priority=data.priority,
        sort_order=data.sort_order,
    )
    db.add(node)
    await db.flush()
    await db.refresh(node)
    return node


async def update_node(db: AsyncSession, node_id: uuid.UUID, data: NodeUpdate) -> AlignmentNode:
    result = await db.execute(select(AlignmentNode).where(AlignmentNode.id == node_id))
    node = result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(node, key, value)

    if "progress_pct" in update_data and update_data["progress_pct"] is not None:
        node.status = AlignmentNode.traffic_light(update_data["progress_pct"])

    node.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(node)
    return node


async def propagate_status(db: AsyncSession, node_id: uuid.UUID) -> list[dict]:
    """Walk up the parent chain recalculating avg progress and traffic-light."""
    result = await db.execute(select(AlignmentNode).where(AlignmentNode.id == node_id))
    node = result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    changed: list[dict] = []
    current_parent_id = node.parent_id

    while current_parent_id is not None:
        result = await db.execute(select(AlignmentNode).where(AlignmentNode.id == current_parent_id))
        parent = result.scalar_one_or_none()
        if not parent:
            break

        # Get all children of this parent
        siblings_result = await db.execute(
            select(AlignmentNode)
            .where(AlignmentNode.parent_id == parent.id)
            .order_by(AlignmentNode.sort_order)
        )
        siblings = list(siblings_result.scalars().all())
        if not siblings:
            break

        total = sum(float(s.progress_pct) for s in siblings)
        avg_pct = Decimal(str(total / len(siblings))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        new_status = AlignmentNode.traffic_light(avg_pct)

        status_changed = parent.status != new_status or parent.progress_pct != avg_pct
        if status_changed:
            parent.progress_pct = avg_pct
            parent.status = new_status
            parent.updated_at = datetime.now(timezone.utc)
            changed.append({"id": str(parent.id), "progress_pct": float(avg_pct), "status": new_status})

        current_parent_id = parent.parent_id

    await db.flush()
    return changed
