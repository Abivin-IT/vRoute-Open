# =============================================================
# vDesign Physical — Lab Test REST API Routes
# GovernanceID: vdesign-physical.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.lab_test.controllers import service
from app.lab_test.models.schema import LabTestCreate, LabTestOut

router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical – lab_test"])


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
