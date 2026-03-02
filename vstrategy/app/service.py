# =============================================================
# vStrategy — Business Logic Service
# Alignment Tree propagation, S&OP 68/27/5 validation,
# pivot signal detection, scorecard computation.
#
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Plan, AlignmentNode, PivotSignal
from app.schemas import PlanCreate, PlanUpdate, NodeCreate, NodeUpdate


# ===================== PLAN CRUD =====================

async def list_plans(db: AsyncSession, status: str | None = None) -> list[Plan]:
    stmt = select(Plan).order_by(Plan.created_at.desc())
    if status:
        stmt = stmt.where(Plan.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_plan(db: AsyncSession, plan_id: uuid.UUID) -> Plan:
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


async def create_plan(db: AsyncSession, data: PlanCreate) -> Plan:
    plan = Plan(
        period_label=data.period_label,
        period_type=data.period_type,
        created_by=data.created_by,
    )
    db.add(plan)
    await db.flush()
    await db.refresh(plan)
    return plan


async def update_plan(db: AsyncSession, plan_id: uuid.UUID, data: PlanUpdate) -> Plan:
    plan = await get_plan(db, plan_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)
    plan.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(plan)
    return plan


# ===================== ALIGNMENT TREE =====================

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

    node.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(node)
    return node


# ===================== STATUS PROPAGATION =====================

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
            parent.updated_at = datetime.utcnow()
            changed.append({"id": str(parent.id), "progress_pct": float(avg_pct), "status": new_status})

        current_parent_id = parent.parent_id

    await db.flush()
    return changed


# ===================== BALANCED SCORECARD =====================

async def get_scorecard(db: AsyncSession, plan_id: uuid.UUID) -> dict:
    result = await db.execute(
        select(AlignmentNode)
        .where(AlignmentNode.plan_id == plan_id, AlignmentNode.node_level == "BSC_PERSPECTIVE")
    )
    bsc_nodes = list(result.scalars().all())

    perspectives = [
        {
            "perspective": n.bsc_perspective,
            "title": n.title,
            "progress_pct": float(n.progress_pct),
            "status": n.status,
        }
        for n in bsc_nodes
    ]

    overall_pct = (
        Decimal(str(sum(float(n.progress_pct) for n in bsc_nodes) / len(bsc_nodes)))
        .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if bsc_nodes
        else Decimal("0")
    )

    return {
        "plan_id": str(plan_id),
        "overall_progress_pct": float(overall_pct),
        "overall_status": AlignmentNode.traffic_light(overall_pct),
        "perspectives": perspectives,
    }


# ===================== S&OP 68/27/5 VALIDATION =====================

async def validate_sop(db: AsyncSession, plan_id: uuid.UUID) -> dict:
    plan = await get_plan(db, plan_id)
    sop_config = plan.sop_config_json or {}

    grow_target = float(sop_config.get("grow_pct", 68))
    run_target = float(sop_config.get("run_pct", 27))
    transform_target = float(sop_config.get("transform_pct", 5))
    give_target = float(sop_config.get("give_pct", 0.1))
    tolerance = float(sop_config.get("tolerance_pct", 2))

    result = await db.execute(
        select(AlignmentNode)
        .where(AlignmentNode.plan_id == plan_id, AlignmentNode.resource_category.isnot(None))
    )
    initiatives = list(result.scalars().all())

    total_budget = sum(float(n.budget_amount or 0) for n in initiatives)

    by_category: dict[str, float] = {}
    for n in initiatives:
        cat = n.resource_category
        by_category[cat] = by_category.get(cat, 0) + float(n.budget_amount or 0)

    grow_actual = (by_category.get("GROW", 0) / total_budget * 100) if total_budget > 0 else 0
    run_actual = (by_category.get("RUN", 0) / total_budget * 100) if total_budget > 0 else 0
    trans_actual = (by_category.get("TRANSFORM", 0) / total_budget * 100) if total_budget > 0 else 0
    give_actual = (by_category.get("GIVE", 0) / total_budget * 100) if total_budget > 0 else 0

    grow_ok = abs(grow_actual - grow_target) <= tolerance
    run_ok = abs(run_actual - run_target) <= tolerance
    trans_ok = abs(trans_actual - transform_target) <= tolerance
    give_ok = give_actual <= give_target + tolerance

    valid = grow_ok and run_ok and trans_ok and give_ok

    total_headcount = sum(int(n.headcount_fte or 0) for n in initiatives)

    def sop_row(cat: str, owner: str, target: float, actual: float, ok: bool, amount: float) -> dict:
        return {
            "category": cat,
            "owner": owner,
            "target_pct": target,
            "actual_pct": round(actual, 1),
            "status": "ON_TRACK" if ok else "VIOLATION",
            "amount": amount,
        }

    breakdown = [
        sop_row("GROW", "CMO", grow_target, grow_actual, grow_ok, by_category.get("GROW", 0)),
        sop_row("RUN", "CAO", run_target, run_actual, run_ok, by_category.get("RUN", 0)),
        sop_row("TRANSFORM", "CPO", transform_target, trans_actual, trans_ok, by_category.get("TRANSFORM", 0)),
        sop_row("GIVE", "CEO", give_target, give_actual, give_ok, by_category.get("GIVE", 0)),
    ]

    return {
        "valid": valid,
        "total_budget": total_budget,
        "total_headcount": total_headcount,
        "breakdown": breakdown,
    }


# ===================== PIVOT SIGNALS =====================

async def get_signals(db: AsyncSession, plan_id: uuid.UUID) -> list[PivotSignal]:
    result = await db.execute(
        select(PivotSignal)
        .where(PivotSignal.plan_id == plan_id)
        .order_by(PivotSignal.created_at.desc())
    )
    return list(result.scalars().all())


async def check_pivot_signal(
    db: AsyncSession, plan_id: uuid.UUID, rule_code: str, actual_value: float, description: str | None = None
) -> PivotSignal:
    if rule_code == "RUNWAY_SECURITY":
        threshold = Decimal("6")
        is_triggered = actual_value < float(threshold)
        severity = "CRITICAL" if is_triggered else "INFO"
        recommendation = (
            f"PIVOT REQUIRED \u2014 Runway at {actual_value} months (< 6 months threshold)"
            if is_triggered
            else f"SAFE ZONE \u2014 Runway at {actual_value} months"
        )
    elif rule_code == "GROWTH_MOMENTUM":
        threshold = Decimal("20")
        is_triggered = actual_value > float(threshold)
        severity = "CRITICAL" if is_triggered else "INFO"
        recommendation = (
            f"PIVOT REQUIRED \u2014 Revenue drop {actual_value}% (> 20% threshold)"
            if is_triggered
            else f"SAFE ZONE \u2014 Revenue variance at {actual_value}%"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown rule_code: {rule_code}. Use RUNWAY_SECURITY or GROWTH_MOMENTUM.",
        )

    actual_dec = Decimal(str(actual_value))
    variance = (
        ((actual_dec - threshold) / threshold * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if threshold != 0
        else Decimal("0")
    )

    signal = PivotSignal(
        plan_id=plan_id,
        rule_code=rule_code,
        rule_description=description or rule_code,
        threshold_value=threshold,
        actual_value=actual_dec,
        variance_pct=variance,
        triggered=is_triggered,
        severity=severity,
        recommendation=recommendation,
    )
    db.add(signal)
    await db.flush()
    await db.refresh(signal)
    return signal
