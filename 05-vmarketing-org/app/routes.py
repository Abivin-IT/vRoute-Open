# =============================================================
# vMarketing Org — FastAPI Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    CampaignCreate, CampaignUpdate, CampaignOut,
    TrackingEventCreate, TrackingEventOut,
    AudienceSegmentCreate, AudienceSegmentOut,
    ContentAssetCreate, ContentAssetOut,
    LeadScoreCreate, LeadScoreOut,
)
from app import service

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org"])


# ---- Campaign ----

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


# ---- Tracking Event ----

@router.get("/tracking-events", response_model=list[TrackingEventOut])
async def list_events(organization: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_tracking_events(db, organization)


@router.get("/tracking-events/{event_id}", response_model=TrackingEventOut)
async def get_event(event_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_tracking_event(db, event_id)
    if not row:
        raise HTTPException(404, "Tracking event not found")
    return row


@router.post("/tracking-events", response_model=TrackingEventOut, status_code=201)
async def ingest_event(body: TrackingEventCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await service.ingest_event(db, body.model_dump())
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.get("/tracking-events/intent-summary/{organization}")
async def intent_summary(organization: str, db: AsyncSession = Depends(get_db)):
    return await service.intent_summary(db, organization)


# ---- Audience Segment ----

@router.get("/segments", response_model=list[AudienceSegmentOut])
async def list_segments(tier: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_segments(db, tier)


@router.get("/segments/{segment_id}", response_model=AudienceSegmentOut)
async def get_segment(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_segment(db, segment_id)
    if not row:
        raise HTTPException(404, "Segment not found")
    return row


@router.post("/segments", response_model=AudienceSegmentOut, status_code=201)
async def create_segment(body: AudienceSegmentCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_segment(db, body.model_dump())


@router.post("/segments/{segment_id}/archive", response_model=AudienceSegmentOut)
async def archive_segment(segment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.archive_segment(db, segment_id)
    if not row:
        raise HTTPException(404, "Segment not found")
    return row


# ---- Content Asset ----

@router.get("/assets", response_model=list[ContentAssetOut])
async def list_assets(asset_type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_assets(db, asset_type)


@router.get("/assets/{asset_id}", response_model=ContentAssetOut)
async def get_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_asset(db, asset_id)
    if not row:
        raise HTTPException(404, "Asset not found")
    return row


@router.post("/assets", response_model=ContentAssetOut, status_code=201)
async def create_asset(body: ContentAssetCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await service.create_asset(db, body.model_dump())
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.post("/assets/{asset_id}/publish", response_model=ContentAssetOut)
async def publish_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.publish_asset(db, asset_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Asset not found")
    return row


@router.post("/assets/{asset_id}/archive", response_model=ContentAssetOut)
async def archive_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.archive_asset(db, asset_id)
    if not row:
        raise HTTPException(404, "Asset not found")
    return row


# ---- Lead Score ----

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
