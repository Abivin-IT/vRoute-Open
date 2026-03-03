# =============================================================
# vDesign Physical — Material Inbox Pydantic Schemas
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class MaterialInboxCreate(BaseModel):
    item_code: str
    source_type: str   # SUPPLIER | COMPETITOR | RND_HANDMADE | MARKET
    supplier_name: Optional[str] = None
    description: str
    material_type: Optional[str] = None
    initial_assessment: Optional[str] = None
    qr_tag_id: Optional[str] = None
    received_by: Optional[str] = None


class MaterialInboxOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    item_code: str
    source_type: str
    supplier_name: Optional[str] = None
    description: str
    material_type: Optional[str] = None
    initial_assessment: Optional[str] = None
    status: str
    qr_tag_id: Optional[str] = None
    metadata_json: Any = {}
    received_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
