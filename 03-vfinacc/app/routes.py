# =============================================================
# vFinacc — REST API Routes (FastAPI Router)
# Ledger, Transactions, Reconciliation, Cost Centers, Compliance.
#
# @GovernanceID vfinacc.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    LedgerEntryCreate, LedgerEntryOut, LedgerEntryUpdate,
    TransactionCreate, TransactionOut,
    ReconciliationRunRequest, ReconciliationOut,
    CostAllocationCreate, CostAllocationOut,
    ComplianceCheckRequest, ComplianceCheckOut,
)
from app import service

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc"])


# ===================== LEDGER ENTRIES (SyR-FIN-00) =====================

@router.get("/ledger")
async def list_ledger(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    entries = await service.list_ledger_entries(db, status)
    return {"count": len(entries), "entries": [LedgerEntryOut.model_validate(e) for e in entries]}


@router.post("/ledger", status_code=201)
async def create_ledger(body: LedgerEntryCreate, db: AsyncSession = Depends(get_db)):
    entry = await service.create_ledger_entry(db, body)
    return LedgerEntryOut.model_validate(entry)


@router.get("/ledger/{entry_id}")
async def get_ledger(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    entry = await service.get_ledger_entry(db, entry_id)
    return LedgerEntryOut.model_validate(entry)


@router.put("/ledger/{entry_id}")
async def update_ledger(entry_id: uuid.UUID, body: LedgerEntryUpdate, db: AsyncSession = Depends(get_db)):
    entry = await service.update_ledger_entry(db, entry_id, body)
    return LedgerEntryOut.model_validate(entry)


@router.post("/ledger/{entry_id}/post")
async def post_ledger(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    entry = await service.post_ledger_entry(db, entry_id)
    return LedgerEntryOut.model_validate(entry)


# ===================== TRANSACTIONS (SyR-FIN-01) =====================

@router.get("/transactions")
async def list_transactions(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    txns = await service.list_transactions(db, status)
    return {"count": len(txns), "transactions": [TransactionOut.model_validate(t) for t in txns]}


@router.post("/transactions", status_code=201)
async def ingest_transaction(body: TransactionCreate, db: AsyncSession = Depends(get_db)):
    txn = await service.ingest_transaction(db, body)
    return TransactionOut.model_validate(txn)


@router.get("/transactions/{txn_id}")
async def get_transaction(txn_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    txn = await service.get_transaction(db, txn_id)
    return TransactionOut.model_validate(txn)


# ===================== RECONCILIATION (SyR-FIN-02) =====================

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


# ===================== COST CENTERS (SyR-FIN-03) =====================

@router.get("/cost-centers")
async def list_cost_centers(category: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    allocations = await service.list_cost_allocations(db, category)
    return {"count": len(allocations), "allocations": [CostAllocationOut.model_validate(a) for a in allocations]}


@router.post("/cost-centers", status_code=201)
async def create_cost_center(body: CostAllocationCreate, db: AsyncSession = Depends(get_db)):
    alloc = await service.create_cost_allocation(db, body)
    return CostAllocationOut.model_validate(alloc)


@router.get("/cost-centers/summary")
async def cost_center_summary(db: AsyncSession = Depends(get_db)):
    return await service.get_cost_center_summary(db)


# ===================== COMPLIANCE (SyR-FIN-04) =====================

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


# ===================== HEALTH =====================

@router.get("/health")
async def health():
    return {"app": "vFinacc", "version": "1.0.0", "status": "UP"}
