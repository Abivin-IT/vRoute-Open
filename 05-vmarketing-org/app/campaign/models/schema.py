# =============================================================
# vMarketing Org — Campaign Schemas (DTOs)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


class CampaignCreate(BaseModel):
    campaign_code: str
    name: str
    target_segment: Optional[str] = None
    stage: str = "AWARENESS"
    channel: Optional[str] = None
    budget_amount: Decimal = Decimal("0")
    currency: str = "USD"
    target_accounts: int = 0
    owner: Optional[str] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    target_segment: Optional[str] = None
    stage: Optional[str] = None
    channel: Optional[str] = None
    budget_amount: Optional[Decimal] = None
    spent_amount: Optional[Decimal] = None
    engaged_accounts: Optional[int] = None
    mqls_generated: Optional[int] = None
    metadata_json: Optional[Any] = None


class CampaignOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    campaign_code: str
    name: str
    target_segment: Optional[str] = None
    stage: str
    channel: Optional[str] = None
    budget_amount: Decimal
    spent_amount: Decimal
    currency: str
    target_accounts: int
    engaged_accounts: int
    mqls_generated: int
    status: str
    owner: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
