# =============================================================
# vDesign Physical — Handover Kit Business Logic Service
# GovernanceID: vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.handover_kit.models.entity import HandoverKit
from app.handover_kit.models.schema import HandoverKitCreate


async def list_handover_kits(db: AsyncSession, status: str | None = None) -> list[HandoverKit]:
    stmt = select(HandoverKit).order_by(HandoverKit.created_at.desc())
    if status:
        stmt = stmt.where(HandoverKit.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_handover_kit(db: AsyncSession, kit_id: uuid.UUID) -> HandoverKit:
    result = await db.execute(select(HandoverKit).where(HandoverKit.id == kit_id))
    kit = result.scalar_one_or_none()
    if not kit:
        raise HTTPException(status_code=404, detail="Handover kit not found")
    return kit


async def create_handover_kit(db: AsyncSession, data: HandoverKitCreate) -> HandoverKit:
    kit = HandoverKit(
        kit_code=data.kit_code,
        product_name=data.product_name,
        contents_summary=data.contents_summary,
        destination=data.destination,
        packed_by=data.packed_by,
        notes=data.notes,
    )
    db.add(kit)
    await db.flush()
    await db.refresh(kit)
    return kit


async def dispatch_handover_kit(db: AsyncSession, kit_id: uuid.UUID) -> HandoverKit:
    """Transition kit: PACKING → READY → DISPATCHED."""
    kit = await get_handover_kit(db, kit_id)
    transitions = {"PACKING": "READY", "READY": "DISPATCHED"}
    next_status = transitions.get(kit.status)
    if not next_status:
        raise HTTPException(status_code=400, detail=f"Cannot advance kit in status '{kit.status}'")
    kit.status = next_status
    if next_status == "DISPATCHED":
        kit.dispatched_at = datetime.now(timezone.utc)
    kit.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(kit)
    return kit


async def receive_handover_kit(db: AsyncSession, kit_id: uuid.UUID) -> HandoverKit:
    """Mark dispatched kit as RECEIVED at destination."""
    kit = await get_handover_kit(db, kit_id)
    if kit.status != "DISPATCHED":
        raise HTTPException(status_code=400, detail=f"Cannot receive kit in status '{kit.status}' — must be DISPATCHED")
    kit.status = "RECEIVED"
    kit.received_at = datetime.now(timezone.utc)
    kit.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(kit)
    return kit
