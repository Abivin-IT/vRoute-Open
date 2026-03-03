# =============================================================
# vMarketing Org — ContentAsset Routes
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.content_asset.controllers import service
from app.content_asset.models.schema import ContentAssetCreate, ContentAssetOut

log = logging.getLogger("vmarketing-org.routes")

router = APIRouter(prefix="/api/v1/vmarketing-org", tags=["vMarketing-Org – content_asset"])


@router.get("/assets", response_model=list[ContentAssetOut])
async def list_assets(asset_type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await service.list_assets(db, asset_type)


@router.get("/assets/{asset_id}", response_model=ContentAssetOut)
async def get_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.get_asset(db, asset_id)
    if not row:
        raise HTTPException(404, "Asset not found")
    return row


@router.post("/assets", response_model=ContentAssetOut, status_code=201)
async def create_asset(body: ContentAssetCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await service.create_asset(db, body.model_dump())
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.post("/assets/{asset_id}/publish", response_model=ContentAssetOut)
async def publish_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        row = await service.publish_asset(db, asset_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if not row:
        raise HTTPException(404, "Asset not found")
    return row


@router.post("/assets/{asset_id}/archive", response_model=ContentAssetOut)
async def archive_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await service.archive_asset(db, asset_id)
    if not row:
        raise HTTPException(404, "Asset not found")
    return row
