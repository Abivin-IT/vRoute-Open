# =============================================================
# vMarketing Org — LeadScore Schemas (DTOs)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class LeadScoreCreate(BaseModel):
    organization: str
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    score: int = 0
    scoring_factors: Optional[Any] = None
    notes: Optional[str] = None


class LeadScoreOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    organization: str
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    score: int
    grade: str
    scoring_factors: Any = {}
    status: str
    handed_off_to: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
