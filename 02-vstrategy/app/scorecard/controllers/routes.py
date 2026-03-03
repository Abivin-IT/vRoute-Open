# =============================================================
# scorecard/controllers/routes.py — Scorecard REST endpoint
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.scorecard.controllers import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy – scorecard"])


@router.get("/plans/{plan_id}/scorecard")
async def get_scorecard(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await service.get_scorecard(db, plan_id)
