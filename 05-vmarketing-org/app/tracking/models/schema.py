# =============================================================
# vMarketing Org — TrackingEvent Schemas (DTOs)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class TrackingEventCreate(BaseModel):
    event_code: str
    organization: str
    action_type: str   # PAGE_VIEW | DOWNLOAD_PDF | PRICING_COMPARE | VIDEO_WATCH | EXIT_INTENT
    page_resource: Optional[str] = None
    dwell_seconds: int = 0
    intent_score: int = 0
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class TrackingEventOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    event_code: str
    organization: str
    action_type: str
    page_resource: Optional[str] = None
    dwell_seconds: int
    intent_score: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime

    model_config = {"from_attributes": True}
