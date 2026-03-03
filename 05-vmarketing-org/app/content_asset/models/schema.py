# =============================================================
# vMarketing Org — ContentAsset Schemas (DTOs)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ContentAssetCreate(BaseModel):
    asset_code: str
    title: str
    asset_type: str   # WHITEPAPER | CASE_STUDY | VIDEO | INFOGRAPHIC | BLOG
    format_type: Optional[str] = None
    url: Optional[str] = None
    target_stage: Optional[str] = None
    created_by: Optional[str] = None


class ContentAssetOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    asset_code: str
    title: str
    asset_type: str
    format_type: Optional[str] = None
    url: Optional[str] = None
    target_stage: Optional[str] = None
    downloads: int
    views: int
    status: str
    created_by: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
