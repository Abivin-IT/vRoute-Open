# =============================================================
# vFinacc — Transaction Business Logic Service
# GovernanceID: vfinacc.1.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.transaction.models.entity import Transaction
from app.transaction.models.schema import TransactionCreate


# ===================== TRANSACTIONS (SyR-FIN-01) =====================

async def list_transactions(db: AsyncSession, status: str | None = None) -> list[Transaction]:
    stmt = select(Transaction).order_by(Transaction.created_at.desc())
    if status:
        stmt = stmt.where(Transaction.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_transaction(db: AsyncSession, txn_id: uuid.UUID) -> Transaction:
    result = await db.execute(select(Transaction).where(Transaction.id == txn_id))
    txn = result.scalar_one_or_none()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


async def ingest_transaction(db: AsyncSession, data: TransactionCreate) -> Transaction:
    txn = Transaction(
        source=data.source,
        amount=data.amount,
        currency=data.currency,
        counterparty=data.counterparty,
        transaction_date=data.transaction_date,
        description=data.description,
        external_id=data.external_id,
        metadata_json=data.metadata_json or {},
    )
    db.add(txn)
    await db.flush()
    await db.refresh(txn)
    return txn
