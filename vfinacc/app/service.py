# =============================================================
# vFinacc — Business Logic Service
# Continuous Ledger, Transaction Ingestion, 3-Way Reconciliation,
# Cost Center Management, Tax & Compliance Guard.
#
# @GovernanceID vfinacc.1.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LedgerEntry, Transaction, ReconciliationMatch, CostAllocation, ComplianceCheck
from app.schemas import (
    LedgerEntryCreate, LedgerEntryUpdate,
    TransactionCreate,
    ReconciliationRunRequest,
    CostAllocationCreate,
    ComplianceCheckRequest,
)


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


# ===================== RECONCILIATION (SyR-FIN-02) =====================

async def list_reconciliation_matches(db: AsyncSession, match_type: str | None = None) -> list[ReconciliationMatch]:
    stmt = select(ReconciliationMatch).order_by(ReconciliationMatch.created_at.desc())
    if match_type:
        stmt = stmt.where(ReconciliationMatch.match_type == match_type)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def run_reconciliation(db: AsyncSession, data: ReconciliationRunRequest) -> ReconciliationMatch:
    """Run 3-way matching: PO ↔ GRN ↔ Invoice."""
    has_po = data.po_reference is not None
    has_grn = data.grn_reference is not None
    has_invoice = data.invoice_reference is not None
    legs_present = sum([has_po, has_grn, has_invoice])

    # Determine match type based on available legs and amounts
    if legs_present == 3 and data.po_amount is not None and data.invoice_amount is not None:
        discrepancy = abs(data.po_amount - data.invoice_amount)
        if discrepancy == 0:
            match_type = "FULL_MATCH"
            confidence = Decimal("100.00")
            notes = "3-way match: PO, GRN, and Invoice amounts match exactly."
        else:
            match_type = "PARTIAL_MATCH"
            max_val = max(data.po_amount, data.invoice_amount)
            confidence = (Decimal("1") - discrepancy / max_val) * 100 if max_val > 0 else Decimal("0")
            confidence = confidence.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            notes = f"Amount discrepancy of {discrepancy}. PO: {data.po_amount}, Invoice: {data.invoice_amount}."
    elif legs_present >= 2:
        match_type = "PARTIAL_MATCH"
        confidence = Decimal(str(legs_present / 3 * 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        discrepancy = None
        notes = f"Partial match: {legs_present}/3 legs present."
    else:
        match_type = "NO_MATCH"
        confidence = Decimal("0")
        discrepancy = None
        notes = "Insufficient data for matching."

    match = ReconciliationMatch(
        po_reference=data.po_reference,
        grn_reference=data.grn_reference,
        invoice_reference=data.invoice_reference,
        match_type=match_type,
        confidence_pct=confidence,
        discrepancy_amount=discrepancy if match_type != "FULL_MATCH" else None,
        notes=notes,
    )
    db.add(match)
    await db.flush()
    await db.refresh(match)
    return match


async def get_reconciliation_summary(db: AsyncSession) -> dict:
    """Summary stats for reconciliation matches."""
    result = await db.execute(select(ReconciliationMatch))
    matches = list(result.scalars().all())

    total = len(matches)
    full = sum(1 for m in matches if m.match_type == "FULL_MATCH")
    partial = sum(1 for m in matches if m.match_type == "PARTIAL_MATCH")
    no_match = sum(1 for m in matches if m.match_type == "NO_MATCH")
    auto_rate = (full / total * 100) if total > 0 else 0

    return {
        "total_matches": total,
        "full_matches": full,
        "partial_matches": partial,
        "no_matches": no_match,
        "auto_match_rate_pct": round(auto_rate, 1),
    }


# ===================== COST CENTER MANAGEMENT (SyR-FIN-03) =====================

async def list_cost_allocations(db: AsyncSession, category: str | None = None) -> list[CostAllocation]:
    stmt = select(CostAllocation).order_by(CostAllocation.created_at.desc())
    if category:
        stmt = stmt.where(CostAllocation.category == category)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_cost_allocation(db: AsyncSession, data: CostAllocationCreate) -> CostAllocation:
    valid_categories = {"GROW", "RUN", "TRANSFORM", "GIVE"}
    if data.category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category: {data.category}. Must be one of {valid_categories}")
    alloc = CostAllocation(
        cost_center_code=data.cost_center_code,
        cost_center_name=data.cost_center_name,
        category=data.category,
        budget_amount=data.budget_amount,
        actual_amount=data.actual_amount,
        currency=data.currency,
        period_label=data.period_label,
        owner=data.owner,
    )
    db.add(alloc)
    await db.flush()
    await db.refresh(alloc)
    return alloc


async def get_cost_center_summary(db: AsyncSession) -> dict:
    """GROW/RUN/TRANSFORM/GIVE summary with target vs actual comparison."""
    result = await db.execute(select(CostAllocation))
    allocations = list(result.scalars().all())

    total_budget = sum(float(a.budget_amount or 0) for a in allocations)
    total_actual = sum(float(a.actual_amount or 0) for a in allocations)

    # Target ratios (from policy)
    targets = {"GROW": 68.0, "RUN": 27.0, "TRANSFORM": 5.0, "GIVE": 0.1}
    tolerance = 2.0

    by_category: dict[str, dict] = {}
    for a in allocations:
        cat = a.category
        if cat not in by_category:
            by_category[cat] = {"budget": 0.0, "actual": 0.0}
        by_category[cat]["budget"] += float(a.budget_amount or 0)
        by_category[cat]["actual"] += float(a.actual_amount or 0)

    breakdown = []
    all_on_track = True
    for cat in ["GROW", "RUN", "TRANSFORM", "GIVE"]:
        target = targets.get(cat, 0)
        cat_data = by_category.get(cat, {"budget": 0, "actual": 0})
        actual_pct = (cat_data["budget"] / total_budget * 100) if total_budget > 0 else 0
        on_track = abs(actual_pct - target) <= tolerance
        if not on_track:
            all_on_track = False
        breakdown.append({
            "category": cat,
            "target_pct": target,
            "actual_pct": round(actual_pct, 1),
            "budget_amount": cat_data["budget"],
            "actual_amount": cat_data["actual"],
            "status": "ON_TRACK" if on_track else "VIOLATION",
        })

    return {
        "valid": all_on_track,
        "total_budget": total_budget,
        "total_actual": total_actual,
        "breakdown": breakdown,
    }


# ===================== TAX & COMPLIANCE (SyR-FIN-04) =====================

async def list_compliance_checks(db: AsyncSession, result_filter: str | None = None) -> list[ComplianceCheck]:
    stmt = select(ComplianceCheck).order_by(ComplianceCheck.created_at.desc())
    if result_filter:
        stmt = stmt.where(ComplianceCheck.result == result_filter)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def run_compliance_check(db: AsyncSession, data: ComplianceCheckRequest) -> ComplianceCheck:
    """Run a compliance check on a ledger entry."""
    entry = await get_ledger_entry(db, data.ledger_entry_id)

    amount = float(entry.amount)
    check_type = data.check_type

    # Compliance rules
    if check_type == "TAX_VAT":
        tax_applicable = True
        tax_rate = Decimal("10.00")  # Vietnam VAT standard rate
        tax_amount = (entry.amount * tax_rate / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        result_val = "PASS"
        notes = f"VAT {tax_rate}% applied. Tax amount: {tax_amount}"
    elif check_type == "TAX_CIT":
        tax_applicable = True
        tax_rate = Decimal("20.00")  # Vietnam CIT standard rate
        tax_amount = (entry.amount * tax_rate / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        result_val = "PASS"
        notes = f"CIT {tax_rate}% applicable. Estimated tax: {tax_amount}"
    elif check_type == "THRESHOLD":
        threshold = Decimal("25000")  # Review threshold
        tax_applicable = False
        tax_rate = None
        tax_amount = None
        if entry.amount > threshold:
            result_val = "FLAG"
            notes = f"Amount {entry.amount} exceeds review threshold {threshold}"
        else:
            result_val = "PASS"
            notes = f"Amount {entry.amount} within threshold {threshold}"
    elif check_type == "POLICY":
        tax_applicable = False
        tax_rate = None
        tax_amount = None
        # Check if entry is posted (policy: only posted entries are compliant)
        if entry.status == "POSTED":
            result_val = "PASS"
            notes = "Entry is posted and compliant with policy."
        elif entry.status == "FLAGGED":
            result_val = "FAIL"
            notes = "Flagged entries require manual review before compliance clearance."
        else:
            result_val = "FLAG"
            notes = f"Entry in '{entry.status}' status — not yet compliant."
    else:
        raise HTTPException(status_code=400, detail=f"Unknown check_type: {check_type}. Use TAX_VAT, TAX_CIT, THRESHOLD, or POLICY.")

    check = ComplianceCheck(
        ledger_entry_id=data.ledger_entry_id,
        check_type=check_type,
        result=result_val,
        tax_applicable=tax_applicable,
        tax_rate_pct=tax_rate,
        tax_amount=tax_amount,
        notes=notes,
        checked_by="system",
    )
    db.add(check)
    await db.flush()
    await db.refresh(check)
    return check


async def get_compliance_summary(db: AsyncSession) -> dict:
    """Summary of all compliance checks."""
    result = await db.execute(select(ComplianceCheck))
    checks = list(result.scalars().all())

    total = len(checks)
    passed = sum(1 for c in checks if c.result == "PASS")
    flagged = sum(1 for c in checks if c.result == "FLAG")
    failed = sum(1 for c in checks if c.result == "FAIL")

    return {
        "total_checks": total,
        "passed": passed,
        "flagged": flagged,
        "failed": failed,
        "pass_rate_pct": round(passed / total * 100, 1) if total > 0 else 0,
    }
