# =============================================================
# vDesign Physical — Business Logic Service
# Spec Master Vault, Idea Inbox, Version Control,
# Feasibility Checker, Handover Kit.
#
# @GovernanceID vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import GoldenSample, MaterialInbox, Prototype, LabTest, HandoverKit
from app.schemas import (
    GoldenSampleCreate, GoldenSampleUpdate,
    MaterialInboxCreate,
    PrototypeCreate,
    LabTestCreate,
    HandoverKitCreate,
)


# ===================== GOLDEN SAMPLES (SyR-PHY-00) =====================

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


# ===================== MATERIAL INBOX (SyR-PHY-01) =====================

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


# ===================== PROTOTYPES (SyR-PHY-02) =====================

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


# ===================== LAB TESTS (SyR-PHY-03) =====================

async def list_lab_tests(db: AsyncSession, result_filter: str | None = None) -> list[LabTest]:
    stmt = select(LabTest).order_by(LabTest.created_at.desc())
    if result_filter:
        stmt = stmt.where(LabTest.result == result_filter)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_lab_test(db: AsyncSession, test_id: uuid.UUID) -> LabTest:
    result = await db.execute(select(LabTest).where(LabTest.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return test


async def create_lab_test(db: AsyncSession, data: LabTestCreate) -> LabTest:
    valid_types = {"STRESS", "DROP", "THERMAL", "CHEMICAL", "HARDNESS"}
    if data.test_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid test_type: {data.test_type}. Must be one of {valid_types}")
    test = LabTest(
        test_code=data.test_code,
        test_type=data.test_type,
        golden_sample_id=data.golden_sample_id,
        prototype_id=data.prototype_id,
        measured_value=data.measured_value,
        threshold_value=data.threshold_value,
        notes=data.notes,
        tested_by=data.tested_by,
    )
    db.add(test)
    await db.flush()
    await db.refresh(test)
    return test


async def complete_lab_test(db: AsyncSession, test_id: uuid.UUID, result_val: str) -> LabTest:
    """Complete a running lab test with PASSED / FAILED / CONDITIONAL."""
    valid_results = {"PASSED", "FAILED", "CONDITIONAL"}
    if result_val not in valid_results:
        raise HTTPException(status_code=400, detail=f"Invalid result: {result_val}. Must be one of {valid_results}")
    test = await get_lab_test(db, test_id)
    if test.result != "RUNNING":
        raise HTTPException(status_code=400, detail=f"Test already completed with result '{test.result}'")
    test.result = result_val
    await db.flush()
    await db.refresh(test)
    return test


async def get_lab_summary(db: AsyncSession) -> dict:
    """Summary of all lab tests."""
    result = await db.execute(select(LabTest))
    tests = list(result.scalars().all())
    total = len(tests)
    passed = sum(1 for t in tests if t.result == "PASSED")
    failed = sum(1 for t in tests if t.result == "FAILED")
    running = sum(1 for t in tests if t.result == "RUNNING")
    conditional = sum(1 for t in tests if t.result == "CONDITIONAL")
    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "running": running,
        "conditional": conditional,
        "pass_rate_pct": round(passed / total * 100, 1) if total > 0 else 0,
    }


# ===================== HANDOVER KITS (SyR-PHY-04) =====================

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
