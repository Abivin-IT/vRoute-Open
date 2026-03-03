# =============================================================
# vDesign Physical — Lab Test Business Logic Service
# GovernanceID: vdesign-physical.1.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.lab_test.models.entity import LabTest
from app.lab_test.models.schema import LabTestCreate


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
