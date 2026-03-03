# =============================================================
# sop/controllers/service.py — S&OP 68/27/5 Validation logic
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.alignment.models.entity import AlignmentNode
from app.plan.controllers.service import get_plan


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
