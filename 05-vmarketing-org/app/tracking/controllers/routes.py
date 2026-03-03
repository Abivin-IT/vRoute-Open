# =============================================================
# vMarketing Org — TrackingEvent Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.tracking.controllers import service
from app.tracking.models.schema import TrackingEventCreate, TrackingEventOut

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org – tracking"])


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
