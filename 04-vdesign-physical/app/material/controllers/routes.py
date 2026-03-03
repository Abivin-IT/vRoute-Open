# =============================================================
# vDesign Physical — Material Inbox REST API Routes
# GovernanceID: vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.material.controllers import service
from app.material.models.schema import MaterialInboxCreate, MaterialInboxOut

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical – material"])


@router.get("/materials")
async def list_materials(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    materials = await service.list_materials(db, status)
    return {"count": len(materials), "materials": [MaterialInboxOut.model_validate(m) for m in materials]}


@router.post("/materials", status_code=201)
async def ingest_material(body: MaterialInboxCreate, db: AsyncSession = Depends(get_db)):
    mat = await service.ingest_material(db, body)
    return MaterialInboxOut.model_validate(mat)


@router.get("/materials/{material_id}")
async def get_material(material_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    mat = await service.get_material(db, material_id)
    return MaterialInboxOut.model_validate(mat)


@router.post("/materials/{material_id}/scrap")
async def scrap_material(material_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    mat = await service.scrap_material(db, material_id)
    return MaterialInboxOut.model_validate(mat)
