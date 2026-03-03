# =============================================================
# vDesign Physical — Handover Kit Pydantic Schemas
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class HandoverKitCreate(BaseModel):
    kit_code: str
    product_name: str
    contents_summary: str
    destination: Optional[str] = None
    packed_by: Optional[str] = None
    notes: Optional[str] = None


class HandoverKitOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    kit_code: str
    product_name: str
    contents_summary: str
    destination: Optional[str] = None
    status: str
    dispatched_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    packed_by: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
