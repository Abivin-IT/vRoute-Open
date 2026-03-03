# =============================================================
# vMarketing Org — AudienceSegment Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.segment.controllers import service
from app.segment.models.schema import AudienceSegmentCreate, AudienceSegmentOut

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org – segment"])


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
