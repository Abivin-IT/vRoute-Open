# =============================================================
# sop/controllers/routes.py — S&OP Validation REST endpoint
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.sop.controllers import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy – sop"])


@router.get("/plans/{plan_id}/sop/validate")
async def validate_sop(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await service.validate_sop(db, plan_id)
