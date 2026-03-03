# =============================================================
# vMarketing Org — Campaign Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.campaign.models.entity import Campaign

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")


async def list_campaigns(db: AsyncSession, status: Optional[str] = None):
    stmt = select(Campaign).where(Campaign.tenant_id == TENANT)
    if status:
        stmt = stmt.where(Campaign.status == status.upper())
    stmt = stmt.order_by(Campaign.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    return await db.get(Campaign, campaign_id)


async def create_campaign(db: AsyncSession, data: dict):
    row = Campaign(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Campaign created: %s", row.campaign_code)
    return row


async def update_campaign(db: AsyncSession, campaign_id: uuid.UUID, data: dict):
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    for k, v in data.items():
        if v is not None:
            setattr(row, k, v)
    await db.commit()
    await db.refresh(row)
    return row


async def launch_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition DRAFT → ACTIVE."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status != "DRAFT":
        raise ValueError(f"Cannot launch campaign in status {row.status}")
    row.status = "ACTIVE"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign launched: %s", row.campaign_code)
    return row


async def pause_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition ACTIVE → PAUSED."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status != "ACTIVE":
        raise ValueError(f"Cannot pause campaign in status {row.status}")
    row.status = "PAUSED"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign paused: %s", row.campaign_code)
    return row


async def complete_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition ACTIVE|PAUSED → COMPLETED."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status not in ("ACTIVE", "PAUSED"):
        raise ValueError(f"Cannot complete campaign in status {row.status}")
    row.status = "COMPLETED"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign completed: %s", row.campaign_code)
    return row
