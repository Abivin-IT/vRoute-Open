# =============================================================
# vDesign Physical — Golden Sample Business Logic Service
# GovernanceID: vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.golden_sample.models.entity import GoldenSample
from app.golden_sample.models.schema import GoldenSampleCreate, GoldenSampleUpdate


async def list_golden_samples(db: AsyncSession, status: str | None = None) -> list[GoldenSample]:
    stmt = select(GoldenSample).order_by(GoldenSample.created_at.desc())
    if status:
        stmt = stmt.where(GoldenSample.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_golden_sample(db: AsyncSession, sample_id: uuid.UUID) -> GoldenSample:
    result = await db.execute(select(GoldenSample).where(GoldenSample.id == sample_id))
    sample = result.scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Golden sample not found")
    return sample


async def create_golden_sample(db: AsyncSession, data: GoldenSampleCreate) -> GoldenSample:
    sample = GoldenSample(
        sample_code=data.sample_code,
        product_name=data.product_name,
        material=data.material,
        weight_actual=data.weight_actual,
        weight_spec=data.weight_spec,
        dimension_x_mm=data.dimension_x_mm,
        dimension_y_mm=data.dimension_y_mm,
        dimension_z_mm=data.dimension_z_mm,
        convergence_pct=data.convergence_pct,
        storage_zone=data.storage_zone,
        storage_shelf=data.storage_shelf,
        custodian=data.custodian,
        seal_tag_id=data.seal_tag_id,
        linked_spec_id=data.linked_spec_id,
        notes=data.notes,
        created_by=data.created_by,
    )
    db.add(sample)
    await db.flush()
    await db.refresh(sample)
    return sample


async def update_golden_sample(db: AsyncSession, sample_id: uuid.UUID, data: GoldenSampleUpdate) -> GoldenSample:
    sample = await get_golden_sample(db, sample_id)
    if sample.status == "COMPROMISED":
        raise HTTPException(status_code=400, detail="Cannot update a COMPROMISED sample")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sample, key, value)
    sample.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(sample)
    return sample


async def seal_golden_sample(db: AsyncSession, sample_id: uuid.UUID) -> GoldenSample:
    """Transition sample to SEALED (lock for archival)."""
    sample = await get_golden_sample(db, sample_id)
    if sample.status not in ("ACTIVE",):
        raise HTTPException(status_code=400, detail=f"Cannot seal sample in status '{sample.status}' — must be ACTIVE")
    sample.status = "SEALED"
    sample.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(sample)
    return sample


async def compromise_golden_sample(db: AsyncSession, sample_id: uuid.UUID) -> GoldenSample:
    """Mark sample as COMPROMISED (tamper detected or damaged)."""
    sample = await get_golden_sample(db, sample_id)
    if sample.status == "COMPROMISED":
        raise HTTPException(status_code=400, detail="Sample is already COMPROMISED")
    sample.status = "COMPROMISED"
    sample.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(sample)
    return sample
