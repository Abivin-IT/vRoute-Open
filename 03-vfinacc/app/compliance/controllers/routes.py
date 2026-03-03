# =============================================================
# vFinacc — Compliance REST API Routes
# GovernanceID: vfinacc.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.compliance.controllers import service
from app.compliance.models.schema import ComplianceCheckRequest, ComplianceCheckOut

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc – compliance"])


@router.get("/compliance")
async def list_compliance(result: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    checks = await service.list_compliance_checks(db, result)
    return {"count": len(checks), "checks": [ComplianceCheckOut.model_validate(c) for c in checks]}


@router.post("/compliance/check", status_code=201)
async def check_compliance(body: ComplianceCheckRequest, db: AsyncSession = Depends(get_db)):
    check = await service.run_compliance_check(db, body)
    return ComplianceCheckOut.model_validate(check)


@router.get("/compliance/summary")
async def compliance_summary(db: AsyncSession = Depends(get_db)):
    return await service.get_compliance_summary(db)
