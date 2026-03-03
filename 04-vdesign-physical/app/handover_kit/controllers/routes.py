# =============================================================
# vDesign Physical — Handover Kit REST API Routes
# GovernanceID: vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.handover_kit.controllers import service
from app.handover_kit.models.schema import HandoverKitCreate, HandoverKitOut

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical – handover_kit"])


@router.get("/handover-kits")
async def list_handover_kits(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    kits = await service.list_handover_kits(db, status)
    return {"count": len(kits), "kits": [HandoverKitOut.model_validate(k) for k in kits]}


@router.post("/handover-kits", status_code=201)
async def create_handover_kit(body: HandoverKitCreate, db: AsyncSession = Depends(get_db)):
    kit = await service.create_handover_kit(db, body)
    return HandoverKitOut.model_validate(kit)


@router.get("/handover-kits/{kit_id}")
async def get_handover_kit(kit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    kit = await service.get_handover_kit(db, kit_id)
    return HandoverKitOut.model_validate(kit)


@router.post("/handover-kits/{kit_id}/advance")
async def advance_handover_kit(kit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    kit = await service.dispatch_handover_kit(db, kit_id)
    return HandoverKitOut.model_validate(kit)


@router.post("/handover-kits/{kit_id}/receive")
async def receive_handover_kit(kit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    kit = await service.receive_handover_kit(db, kit_id)
    return HandoverKitOut.model_validate(kit)
