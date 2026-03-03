# =============================================================
# vMarketing Org — AudienceSegment Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.segment.models.entity import AudienceSegment

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")


async def list_segments(db: AsyncSession, tier: Optional[str] = None):
    stmt = select(AudienceSegment).where(AudienceSegment.tenant_id == TENANT)
    if tier:
        stmt = stmt.where(AudienceSegment.tier == tier.upper())
    stmt = stmt.order_by(AudienceSegment.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_segment(db: AsyncSession, segment_id: uuid.UUID):
    return await db.get(AudienceSegment, segment_id)


async def create_segment(db: AsyncSession, data: dict):
    row = AudienceSegment(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Segment created: %s", row.segment_code)
    return row


async def archive_segment(db: AsyncSession, segment_id: uuid.UUID):
    row = await db.get(AudienceSegment, segment_id)
    if not row:
        return None
    row.status = "ARCHIVED"
    await db.commit()
    await db.refresh(row)
    log.info("Segment archived: %s", row.segment_code)
    return row
