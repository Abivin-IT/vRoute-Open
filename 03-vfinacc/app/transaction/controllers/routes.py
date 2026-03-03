# =============================================================
# vFinacc — Transaction REST API Routes
# GovernanceID: vfinacc.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.transaction.controllers import service
from app.transaction.models.schema import TransactionCreate, TransactionOut

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc – transaction"])


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
