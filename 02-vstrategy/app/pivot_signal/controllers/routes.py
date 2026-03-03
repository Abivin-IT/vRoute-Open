# =============================================================
# pivot_signal/controllers/routes.py — Pivot Signal REST endpoints
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.pivot_signal.models.schema import SignalCheck, SignalOut
from app.pivot_signal.controllers import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy – pivot_signal"])


@router.get("/plans/{plan_id}/signals")
async def get_signals(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    signals = await service.get_signals(db, plan_id)
    return {"count": len(signals), "signals": [SignalOut.model_validate(s) for s in signals]}


@router.post("/plans/{plan_id}/signals/check")
async def check_signal(plan_id: uuid.UUID, body: SignalCheck, db: AsyncSession = Depends(get_db)):
    signal = await service.check_pivot_signal(db, plan_id, body.rule_code, body.actual_value, body.description)
    return SignalOut.model_validate(signal)
