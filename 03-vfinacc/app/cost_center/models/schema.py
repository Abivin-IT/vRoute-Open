# =============================================================
# vFinacc — Cost Center Pydantic Schemas (DTOs)
# GovernanceID: vfinacc.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


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
