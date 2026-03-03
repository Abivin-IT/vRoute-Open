# =============================================================
# pivot_signal/models/schema.py — Pivot Signal Pydantic DTOs
# @GovernanceID vstrategy.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SignalCheck(BaseModel):
    rule_code: str
    actual_value: float
    description: Optional[str] = None


class SignalOut(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    rule_code: str
    rule_description: Optional[str] = None
    threshold_value: Decimal
    actual_value: Decimal
    variance_pct: Optional[Decimal] = None
    triggered: bool
    severity: str
    recommendation: Optional[str] = None
    resolution: Optional[str] = None
    resolved_by: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
