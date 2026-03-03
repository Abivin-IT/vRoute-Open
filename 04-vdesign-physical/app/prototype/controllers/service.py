# =============================================================
# vDesign Physical — Prototype Business Logic Service
# GovernanceID: vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.prototype.models.entity import Prototype
from app.prototype.models.schema import PrototypeCreate


async def list_prototypes(db: AsyncSession, status: str | None = None) -> list[Prototype]:
    stmt = select(Prototype).order_by(Prototype.created_at.desc())
    if status:
        stmt = stmt.where(Prototype.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_prototype(db: AsyncSession, proto_id: uuid.UUID) -> Prototype:
    result = await db.execute(select(Prototype).where(Prototype.id == proto_id))
    proto = result.scalar_one_or_none()
    if not proto:
        raise HTTPException(status_code=404, detail="Prototype not found")
    return proto


async def create_prototype(db: AsyncSession, data: PrototypeCreate) -> Prototype:
    proto = Prototype(
        proto_code=data.proto_code,
        product_name=data.product_name,
        version_label=data.version_label,
        fabrication_method=data.fabrication_method,
        rfid_tag_id=data.rfid_tag_id,
        location=data.location,
        notes=data.notes,
        created_by=data.created_by,
    )
    db.add(proto)
    await db.flush()
    await db.refresh(proto)
    return proto


async def retire_prototype(db: AsyncSession, proto_id: uuid.UUID) -> Prototype:
    """Mark prototype as OBSOLETE."""
    proto = await get_prototype(db, proto_id)
    if proto.status == "OBSOLETE":
        raise HTTPException(status_code=400, detail="Prototype is already OBSOLETE")
    proto.status = "OBSOLETE"
    proto.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(proto)
    return proto
