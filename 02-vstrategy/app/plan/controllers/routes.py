# =============================================================
# plan/controllers/routes.py — Plan REST endpoints
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.plan.models.schema import PlanCreate, PlanOut, PlanUpdate
from app.plan.controllers import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy – plan"])


@router.get("/plans")
async def list_plans(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    plans = await service.list_plans(db, status)
    return {"count": len(plans), "plans": [PlanOut.model_validate(p) for p in plans]}


@router.post("/plans", status_code=201)
async def create_plan(body: PlanCreate, db: AsyncSession = Depends(get_db)):
    plan = await service.create_plan(db, body)
    return PlanOut.model_validate(plan)


@router.get("/plans/{plan_id}")
async def get_plan(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    plan = await service.get_plan(db, plan_id)
    return PlanOut.model_validate(plan)


@router.put("/plans/{plan_id}")
async def update_plan(plan_id: uuid.UUID, body: PlanUpdate, db: AsyncSession = Depends(get_db)):
    plan = await service.update_plan(db, plan_id, body)
    return PlanOut.model_validate(plan)
