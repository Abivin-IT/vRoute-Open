# =============================================================
# vFinacc — Ledger REST API Routes
# GovernanceID: vfinacc.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.ledger.controllers import service
from app.ledger.models.schema import LedgerEntryCreate, LedgerEntryOut, LedgerEntryUpdate

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc – ledger"])


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
