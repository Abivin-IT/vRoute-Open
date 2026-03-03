# =============================================================
# vFinacc — Compliance Business Logic Service
# GovernanceID: vfinacc.1.0
# =============================================================
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.compliance.models.entity import ComplianceCheck
from app.compliance.models.schema import ComplianceCheckRequest
from app.ledger.controllers.service import get_ledger_entry


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
