# =============================================================
# vMarketing Org — ContentAsset Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.content_asset.models.entity import ContentAsset

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")

VALID_ASSET_TYPES = {"WHITEPAPER", "CASE_STUDY", "VIDEO", "INFOGRAPHIC", "BLOG"}


async def list_assets(db: AsyncSession, asset_type: Optional[str] = None):
    stmt = select(ContentAsset).where(ContentAsset.tenant_id == TENANT)
    if asset_type:
        stmt = stmt.where(ContentAsset.asset_type == asset_type.upper())
    stmt = stmt.order_by(ContentAsset.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_asset(db: AsyncSession, asset_id: uuid.UUID):
    return await db.get(ContentAsset, asset_id)


async def create_asset(db: AsyncSession, data: dict):
    at = data.get("asset_type", "").upper()
    if at not in VALID_ASSET_TYPES:
        raise ValueError(f"Invalid asset_type: {at}. Must be one of {VALID_ASSET_TYPES}")
    data["asset_type"] = at
    row = ContentAsset(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Asset created: %s", row.asset_code)
    return row


async def publish_asset(db: AsyncSession, asset_id: uuid.UUID):
    row = await db.get(ContentAsset, asset_id)
    if not row:
        return None
    if row.status != "DRAFT":
        raise ValueError(f"Cannot publish asset in status {row.status}")
    row.status = "PUBLISHED"
    await db.commit()
    await db.refresh(row)
    log.info("Asset published: %s", row.asset_code)
    return row


async def archive_asset(db: AsyncSession, asset_id: uuid.UUID):
    row = await db.get(ContentAsset, asset_id)
    if not row:
        return None
    row.status = "ARCHIVED"
    await db.commit()
    await db.refresh(row)
    log.info("Asset archived: %s", row.asset_code)
    return row
