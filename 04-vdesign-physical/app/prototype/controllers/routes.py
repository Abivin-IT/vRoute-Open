# =============================================================
# vDesign Physical — Prototype REST API Routes
# GovernanceID: vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.prototype.controllers import service
from app.prototype.models.schema import PrototypeCreate, PrototypeOut

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical – prototype"])


@router.get("/prototypes")
async def list_prototypes(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    prototypes = await service.list_prototypes(db, status)
    return {"count": len(prototypes), "prototypes": [PrototypeOut.model_validate(p) for p in prototypes]}


@router.post("/prototypes", status_code=201)
async def create_prototype(body: PrototypeCreate, db: AsyncSession = Depends(get_db)):
    proto = await service.create_prototype(db, body)
    return PrototypeOut.model_validate(proto)


@router.get("/prototypes/{proto_id}")
async def get_prototype(proto_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    proto = await service.get_prototype(db, proto_id)
    return PrototypeOut.model_validate(proto)


@router.post("/prototypes/{proto_id}/retire")
async def retire_prototype(proto_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    proto = await service.retire_prototype(db, proto_id)
    return PrototypeOut.model_validate(proto)
