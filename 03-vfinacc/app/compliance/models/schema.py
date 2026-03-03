# =============================================================
# vFinacc — Compliance Pydantic Schemas (DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


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
