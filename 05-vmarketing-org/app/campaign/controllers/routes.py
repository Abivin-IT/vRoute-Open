# =============================================================
# vMarketing Org — Campaign Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.campaign.controllers import service
from app.campaign.models.schema import CampaignCreate, CampaignUpdate, CampaignOut

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org – campaign"])


@router.get("/campaigns", response_model=list[CampaignOut])
async def list_campaigns(status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_campaigns(db, status)


@router.get("/campaigns/{campaign_id}", response_model=CampaignOut)
async def get_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_campaign(db, campaign_id)
    if not row:
        raise HTTPException(404, "Campaign not found")
    return row


@router.post("/campaigns", response_model=CampaignOut, status_code=201)
async def create_campaign(body: CampaignCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_campaign(db, body.model_dump())


@router.patch("/campaigns/{campaign_id}", response_model=CampaignOut)
async def update_campaign(campaign_id: uuid.UUID, body: CampaignUpdate, db: AsyncSession = Depends(get_db)):
    row = await service.update_campaign(db, campaign_id, body.model_dump(exclude_unset=True))
    if not row:
        raise HTTPException(404, "Campaign not found")
    return row


@router.post("/campaigns/{campaign_id}/launch", response_model=CampaignOut)
async def launch_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.launch_campaign(db, campaign_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Campaign not found")
    return row


@router.post("/campaigns/{campaign_id}/pause", response_model=CampaignOut)
async def pause_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.pause_campaign(db, campaign_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Campaign not found")
    return row


@router.post("/campaigns/{campaign_id}/complete", response_model=CampaignOut)
async def complete_campaign(campaign_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.complete_campaign(db, campaign_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Campaign not found")
    return row
