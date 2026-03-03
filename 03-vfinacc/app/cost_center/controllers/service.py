# =============================================================
# vFinacc — Cost Center Business Logic Service
# GovernanceID: vfinacc.1.0
# =============================================================
from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cost_center.models.entity import CostAllocation
from app.cost_center.models.schema import CostAllocationCreate


# ===================== COST CENTER MANAGEMENT (SyR-FIN-03) =====================

async def list_cost_allocations(db: AsyncSession, category: str | None = None) -> list[CostAllocation]:
    stmt = select(CostAllocation).order_by(CostAllocation.created_at.desc())
    if category:
        stmt = stmt.where(CostAllocation.category == category)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_cost_allocation(db: AsyncSession, data: CostAllocationCreate) -> CostAllocation:
    valid_categories = {"GROW", "RUN", "TRANSFORM", "GIVE"}
    if data.category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category: {data.category}. Must be one of {valid_categories}")
    alloc = CostAllocation(
        cost_center_code=data.cost_center_code,
        cost_center_name=data.cost_center_name,
        category=data.category,
        budget_amount=data.budget_amount,
        actual_amount=data.actual_amount,
        currency=data.currency,
        period_label=data.period_label,
        owner=data.owner,
    )
    db.add(alloc)
    await db.flush()
    await db.refresh(alloc)
    return alloc


async def get_cost_center_summary(db: AsyncSession) -> dict:
    """GROW/RUN/TRANSFORM/GIVE summary with target vs actual comparison."""
    result = await db.execute(select(CostAllocation))
    allocations = list(result.scalars().all())

    total_budget = sum(float(a.budget_amount or 0) for a in allocations)
    total_actual = sum(float(a.actual_amount or 0) for a in allocations)

    # Target ratios (from policy)
    targets = {"GROW": 68.0, "RUN": 27.0, "TRANSFORM": 5.0, "GIVE": 0.1}
    tolerance = 2.0

    by_category: dict[str, dict] = {}
    for a in allocations:
        cat = a.category
        if cat not in by_category:
            by_category[cat] = {"budget": 0.0, "actual": 0.0}
        by_category[cat]["budget"] += float(a.budget_amount or 0)
        by_category[cat]["actual"] += float(a.actual_amount or 0)

    breakdown = []
    all_on_track = True
    for cat in ["GROW", "RUN", "TRANSFORM", "GIVE"]:
        target = targets.get(cat, 0)
        cat_data = by_category.get(cat, {"budget": 0, "actual": 0})
        actual_pct = (cat_data["budget"] / total_budget * 100) if total_budget > 0 else 0
        on_track = abs(actual_pct - target) <= tolerance
        if not on_track:
            all_on_track = False
        breakdown.append({
            "category": cat,
            "target_pct": target,
            "actual_pct": round(actual_pct, 1),
            "budget_amount": cat_data["budget"],
            "actual_amount": cat_data["actual"],
            "status": "ON_TRACK" if on_track else "VIOLATION",
        })

    return {
        "valid": all_on_track,
        "total_budget": total_budget,
        "total_actual": total_actual,
        "breakdown": breakdown,
    }
