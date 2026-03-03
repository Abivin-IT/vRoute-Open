# =============================================================
# vMarketing Org — AudienceSegment Schemas (DTOs)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class AudienceSegmentCreate(BaseModel):
    segment_code: str
    name: str
    description: Optional[str] = None
    criteria_json: Optional[Any] = None
    account_count: int = 0
    tier: str = "TIER_3"
    created_by: Optional[str] = None


class AudienceSegmentOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    segment_code: str
    name: str
    description: Optional[str] = None
    criteria_json: Any = {}
    account_count: int
    tier: str
    status: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
