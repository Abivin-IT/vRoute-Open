# =============================================================
# vDesign Physical — Prototype Pydantic Schemas
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class PrototypeCreate(BaseModel):
    proto_code: str
    product_name: str
    version_label: str
    fabrication_method: Optional[str] = None  # 3D_PRINT | CNC | INJECTION | HANDMADE
    rfid_tag_id: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None


class PrototypeOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    proto_code: str
    product_name: str
    version_label: str
    fabrication_method: Optional[str] = None
    rfid_tag_id: Optional[str] = None
    status: str
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: Any = {}
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
