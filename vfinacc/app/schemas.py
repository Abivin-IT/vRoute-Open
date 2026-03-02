# =============================================================
# vFinacc — Pydantic Schemas (Request / Response DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---- Ledger Entry ----

class LedgerEntryCreate(BaseModel):
    entry_number: str
    entry_date: date
    description: str
    debit_account: str
    credit_account: str
    amount: Decimal = Decimal("0")
    currency: str = "VND"
    cost_center: Optional[str] = None
    created_by: Optional[str] = None


class LedgerEntryUpdate(BaseModel):
    description: Optional[str] = None
    debit_account: Optional[str] = None
    credit_account: Optional[str] = None
    amount: Optional[Decimal] = None
    cost_center: Optional[str] = None
    metadata_json: Optional[Any] = None


class LedgerEntryOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    entry_number: str
    entry_date: date
    description: str
    debit_account: str
    credit_account: str
    amount: Decimal
    currency: str
    status: str
    cost_center: Optional[str] = None
    metadata_json: Any = {}
    posted_by: Optional[str] = None
    posted_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Transaction ----

class TransactionCreate(BaseModel):
    source: str
    amount: Decimal = Decimal("0")
    currency: str = "VND"
    counterparty: Optional[str] = None
    transaction_date: date
    description: Optional[str] = None
    external_id: Optional[str] = None
    metadata_json: Optional[Any] = None


class TransactionOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    external_id: Optional[str] = None
    source: str
    amount: Decimal
    currency: str
    counterparty: Optional[str] = None
    transaction_date: date
    description: Optional[str] = None
    status: str
    ledger_entry_id: Optional[uuid.UUID] = None
    metadata_json: Any = {}
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- Reconciliation ----

class ReconciliationRunRequest(BaseModel):
    po_reference: Optional[str] = None
    grn_reference: Optional[str] = None
    invoice_reference: Optional[str] = None
    po_amount: Optional[Decimal] = None
    grn_amount: Optional[Decimal] = None
    invoice_amount: Optional[Decimal] = None


class ReconciliationOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    po_reference: Optional[str] = None
    grn_reference: Optional[str] = None
    invoice_reference: Optional[str] = None
    match_type: str
    confidence_pct: Decimal
    discrepancy_amount: Optional[Decimal] = None
    status: str
    notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Cost Allocation ----

class CostAllocationCreate(BaseModel):
    cost_center_code: str
    cost_center_name: str
    category: str  # GROW | RUN | TRANSFORM | GIVE
    budget_amount: Decimal = Decimal("0")
    actual_amount: Decimal = Decimal("0")
    currency: str = "VND"
    period_label: str
    owner: Optional[str] = None


class CostAllocationOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    cost_center_code: str
    cost_center_name: str
    category: str
    budget_amount: Decimal
    actual_amount: Decimal
    currency: str
    period_label: str
    owner: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Compliance Check ----

class ComplianceCheckRequest(BaseModel):
    ledger_entry_id: uuid.UUID
    check_type: str = "TAX_VAT"


class ComplianceCheckOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    ledger_entry_id: Optional[uuid.UUID] = None
    check_type: str
    result: str
    tax_applicable: bool
    tax_rate_pct: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    notes: Optional[str] = None
    checked_by: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
