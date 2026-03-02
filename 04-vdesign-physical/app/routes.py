# =============================================================
# vDesign Physical — REST API Routes (FastAPI Router)
# Golden Samples, Materials, Prototypes, Lab Tests, Handover Kits.
#
# @GovernanceID vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    GoldenSampleCreate, GoldenSampleOut, GoldenSampleUpdate,
    MaterialInboxCreate, MaterialInboxOut,
    PrototypeCreate, PrototypeOut,
    LabTestCreate, LabTestOut,
    HandoverKitCreate, HandoverKitOut,
)
from app import service

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical"])


# ===================== GOLDEN SAMPLES (SyR-PHY-00) =====================

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


# ===================== MATERIALS (SyR-PHY-01) =====================

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


# ===================== PROTOTYPES (SyR-PHY-02) =====================

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


# ===================== LAB TESTS (SyR-PHY-03) =====================

@router.get("/lab-tests")
async def list_lab_tests(result: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    tests = await service.list_lab_tests(db, result)
    return {"count": len(tests), "tests": [LabTestOut.model_validate(t) for t in tests]}


@router.post("/lab-tests", status_code=201)
async def create_lab_test(body: LabTestCreate, db: AsyncSession = Depends(get_db)):
    test = await service.create_lab_test(db, body)
    return LabTestOut.model_validate(test)


@router.get("/lab-tests/summary")
async def lab_test_summary(db: AsyncSession = Depends(get_db)):
    return await service.get_lab_summary(db)


@router.get("/lab-tests/{test_id}")
async def get_lab_test(test_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    test = await service.get_lab_test(db, test_id)
    return LabTestOut.model_validate(test)


@router.post("/lab-tests/{test_id}/complete")
async def complete_lab_test(test_id: uuid.UUID, result: str = Query(...), db: AsyncSession = Depends(get_db)):
    test = await service.complete_lab_test(db, test_id, result)
    return LabTestOut.model_validate(test)


# ===================== HANDOVER KITS (SyR-PHY-04) =====================

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


# ===================== HEALTH =====================

@router.get("/health")
async def health():
    return {"app": "vDesign Physical", "version": "1.0.0", "status": "UP"}
