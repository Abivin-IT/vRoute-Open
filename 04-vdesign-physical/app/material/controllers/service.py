# =============================================================
# vDesign Physical — Material Inbox Business Logic Service
# GovernanceID: vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.material.models.entity import MaterialInbox
from app.material.models.schema import MaterialInboxCreate


async def list_materials(db: AsyncSession, status: str | None = None) -> list[MaterialInbox]:
    stmt = select(MaterialInbox).order_by(MaterialInbox.created_at.desc())
    if status:
        stmt = stmt.where(MaterialInbox.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_material(db: AsyncSession, material_id: uuid.UUID) -> MaterialInbox:
    result = await db.execute(select(MaterialInbox).where(MaterialInbox.id == material_id))
    mat = result.scalar_one_or_none()
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")
    return mat


async def ingest_material(db: AsyncSession, data: MaterialInboxCreate) -> MaterialInbox:
    valid_sources = {"SUPPLIER", "COMPETITOR", "RND_HANDMADE", "MARKET"}
    if data.source_type not in valid_sources:
        raise HTTPException(status_code=400, detail=f"Invalid source_type: {data.source_type}. Must be one of {valid_sources}")
    mat = MaterialInbox(
        item_code=data.item_code,
        source_type=data.source_type,
        supplier_name=data.supplier_name,
        description=data.description,
        material_type=data.material_type,
        initial_assessment=data.initial_assessment,
        qr_tag_id=data.qr_tag_id,
        received_by=data.received_by,
    )
    db.add(mat)
    await db.flush()
    await db.refresh(mat)
    return mat


async def scrap_material(db: AsyncSession, material_id: uuid.UUID) -> MaterialInbox:
    """Mark material as SCRAPPED."""
    mat = await get_material(db, material_id)
    if mat.status == "SCRAPPED":
        raise HTTPException(status_code=400, detail="Material already scrapped")
    mat.status = "SCRAPPED"
    mat.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(mat)
    return mat
