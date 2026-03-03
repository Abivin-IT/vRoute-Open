# =============================================================
# plan/controllers/service.py — Plan CRUD business logic
# @GovernanceID vstrategy.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.plan.models.entity import Plan
from app.plan.models.schema import PlanCreate, PlanUpdate


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
    plan.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(plan)
    return plan
