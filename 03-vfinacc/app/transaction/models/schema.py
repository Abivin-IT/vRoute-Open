# =============================================================
# vFinacc — Transaction Pydantic Schemas (DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


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
