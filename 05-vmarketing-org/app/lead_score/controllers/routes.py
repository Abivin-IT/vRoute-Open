# =============================================================
# vMarketing Org — LeadScore Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.lead_score.controllers import service
from app.lead_score.models.schema import LeadScoreCreate, LeadScoreOut

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org – lead_score"])


@router.get("/leads", response_model=list[LeadScoreOut])
async def list_leads(grade: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_leads(db, grade)


@router.get("/leads/{lead_id}", response_model=LeadScoreOut)
async def get_lead(lead_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_lead(db, lead_id)
    if not row:
        raise HTTPException(404, "Lead not found")
    return row


@router.post("/leads", response_model=LeadScoreOut, status_code=201)
async def upsert_lead(body: LeadScoreCreate, db: AsyncSession = Depends(get_db)):
    return await service.upsert_lead(db, body.model_dump())


@router.post("/leads/{lead_id}/qualify", response_model=LeadScoreOut)
async def qualify_lead(lead_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.qualify_lead(db, lead_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Lead not found")
    return row


@router.post("/leads/{lead_id}/handoff", response_model=LeadScoreOut)
async def handoff_lead(lead_id: uuid.UUID, handed_off_to: str, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.handoff_lead(db, lead_id, handed_off_to)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Lead not found")
    return row


@router.post("/leads/{lead_id}/disqualify", response_model=LeadScoreOut)
async def disqualify_lead(lead_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.disqualify_lead(db, lead_id)
    if not row:
        raise HTTPException(404, "Lead not found")
    return row
