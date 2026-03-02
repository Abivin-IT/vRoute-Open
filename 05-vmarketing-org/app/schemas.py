# =============================================================
# vMarketing Org — Pydantic Schemas (Request / Response DTOs)
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


# ---- Campaign ----

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


# ---- Tracking Event ----

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


# ---- Audience Segment ----

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


# ---- Content Asset ----

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


# ---- Lead Score ----

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
