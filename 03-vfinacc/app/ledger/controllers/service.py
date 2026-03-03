# =============================================================
# vFinacc — Ledger Business Logic Service
# GovernanceID: vfinacc.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ledger.models.entity import LedgerEntry
from app.ledger.models.schema import LedgerEntryCreate, LedgerEntryUpdate


# ===================== LEDGER ENTRIES (SyR-FIN-00) =====================

async def list_ledger_entries(db: AsyncSession, status: str | None = None) -> list[LedgerEntry]:
    stmt = select(LedgerEntry).order_by(LedgerEntry.created_at.desc())
    if status:
        stmt = stmt.where(LedgerEntry.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_ledger_entry(db: AsyncSession, entry_id: uuid.UUID) -> LedgerEntry:
    result = await db.execute(select(LedgerEntry).where(LedgerEntry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Ledger entry not found")
    return entry


async def create_ledger_entry(db: AsyncSession, data: LedgerEntryCreate) -> LedgerEntry:
    entry = LedgerEntry(
        entry_number=data.entry_number,
        entry_date=data.entry_date,
        description=data.description,
        debit_account=data.debit_account,
        credit_account=data.credit_account,
        amount=data.amount,
        currency=data.currency,
        cost_center=data.cost_center,
        created_by=data.created_by,
    )
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    return entry


async def update_ledger_entry(db: AsyncSession, entry_id: uuid.UUID, data: LedgerEntryUpdate) -> LedgerEntry:
    entry = await get_ledger_entry(db, entry_id)
    if entry.status != "DRAFT":
        raise HTTPException(status_code=400, detail="Only DRAFT entries can be updated")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entry, key, value)
    entry.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(entry)
    return entry


async def post_ledger_entry(db: AsyncSession, entry_id: uuid.UUID) -> LedgerEntry:
    """Transition a DRAFT entry to POSTED (finalize)."""
    entry = await get_ledger_entry(db, entry_id)
    if entry.status != "DRAFT":
        raise HTTPException(status_code=400, detail=f"Cannot post entry in status '{entry.status}' — must be DRAFT")
    entry.status = "POSTED"
    entry.posted_by = "system"
    entry.posted_at = datetime.now(timezone.utc)
    entry.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(entry)
    return entry
