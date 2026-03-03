# =============================================================
# vDesign Physical — Golden Sample REST API Routes
# GovernanceID: vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.golden_sample.controllers import service
from app.golden_sample.models.schema import (
    GoldenSampleCreate, GoldenSampleOut, GoldenSampleUpdate,
)

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical – golden_sample"])


@router.get("/golden-samples")
async def list_golden_samples(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    samples = await service.list_golden_samples(db, status)
    return {"count": len(samples), "samples": [GoldenSampleOut.model_validate(s) for s in samples]}


@router.post("/golden-samples", status_code=201)
async def create_golden_sample(body: GoldenSampleCreate, db: AsyncSession = Depends(get_db)):
    sample = await service.create_golden_sample(db, body)
    return GoldenSampleOut.model_validate(sample)


@router.get("/golden-samples/{sample_id}")
async def get_golden_sample(sample_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    sample = await service.get_golden_sample(db, sample_id)
    return GoldenSampleOut.model_validate(sample)


@router.put("/golden-samples/{sample_id}")
async def update_golden_sample(sample_id: uuid.UUID, body: GoldenSampleUpdate, db: AsyncSession = Depends(get_db)):
    sample = await service.update_golden_sample(db, sample_id, body)
    return GoldenSampleOut.model_validate(sample)


@router.post("/golden-samples/{sample_id}/seal")
async def seal_golden_sample(sample_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    sample = await service.seal_golden_sample(db, sample_id)
    return GoldenSampleOut.model_validate(sample)


@router.post("/golden-samples/{sample_id}/compromise")
async def compromise_golden_sample(sample_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    sample = await service.compromise_golden_sample(db, sample_id)
    return GoldenSampleOut.model_validate(sample)
