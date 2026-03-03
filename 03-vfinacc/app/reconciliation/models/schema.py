# =============================================================
# vFinacc — Reconciliation Pydantic Schemas (DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


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
