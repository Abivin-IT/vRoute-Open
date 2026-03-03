# =============================================================
# vFinacc — Reconciliation Business Logic Service
# GovernanceID: vfinacc.1.0
# =============================================================
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reconciliation.models.entity import ReconciliationMatch
from app.reconciliation.models.schema import ReconciliationRunRequest


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
