# =============================================================
# pivot_signal/controllers/service.py — Pivot Signal detection logic
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.pivot_signal.models.entity import PivotSignal


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
