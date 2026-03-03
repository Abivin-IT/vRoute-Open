# =============================================================
# vFinacc — Ledger Pydantic Schemas (DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


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
