# =============================================================
# vFinacc — Reconciliation REST API Routes
# GovernanceID: vfinacc.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.reconciliation.controllers import service
from app.reconciliation.models.schema import ReconciliationRunRequest, ReconciliationOut

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc – reconciliation"])


@router.get("/reconciliation")
async def list_reconciliation(match_type: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    matches = await service.list_reconciliation_matches(db, match_type)
    return {"count": len(matches), "matches": [ReconciliationOut.model_validate(m) for m in matches]}


@router.post("/reconciliation/run", status_code=201)
async def run_reconciliation(body: ReconciliationRunRequest, db: AsyncSession = Depends(get_db)):
    match = await service.run_reconciliation(db, body)
    return ReconciliationOut.model_validate(match)


@router.get("/reconciliation/summary")
async def reconciliation_summary(db: AsyncSession = Depends(get_db)):
    return await service.get_reconciliation_summary(db)
