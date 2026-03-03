# =============================================================
# scorecard/controllers/service.py — Balanced Scorecard computation
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.alignment.models.entity import AlignmentNode


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
