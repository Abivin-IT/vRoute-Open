# =============================================================
# vStrategy — Pydantic Schemas (Request / Response DTOs)
# GovernanceID: vstrategy.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ---- Plan ----

class PlanCreate(BaseModel):
    period_label: str = Field(..., min_length=1, max_length=100)
    period_type: Literal["MONTHLY", "QUARTERLY", "HALF_YEARLY", "ANNUAL"] = "QUARTERLY"
    created_by: Optional[str] = None


class PlanUpdate(BaseModel):
    status: Optional[str] = None
    baseline_json: Optional[Any] = None
    objectives_json: Optional[Any] = None
    gap_analysis_json: Optional[Any] = None
    mece_options_json: Optional[Any] = None
    selected_option: Optional[str] = None
    decision_log_json: Optional[Any] = None
    sop_config_json: Optional[Any] = None


class PlanOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    period_type: str
    period_label: str
    status: str
    baseline_json: Any = {}
    objectives_json: Any = {}
    gap_analysis_json: Any = {}
    mece_options_json: Any = []
    selected_option: Optional[str] = None
    decision_log_json: Any = {}
    sop_config_json: Any = {}
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Alignment Node ----

class NodeCreate(BaseModel):
    node_level: str
    code: Optional[str] = None
    title: str
    owner: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    bsc_perspective: Optional[str] = None
    progress_pct: Decimal = Decimal("0")
    resource_category: Optional[str] = None
    budget_amount: Decimal = Decimal("0")
    headcount_fte: Decimal = Decimal("0")
    priority: Optional[str] = None
    sort_order: int = 0


class NodeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    resource_category: Optional[str] = None
    progress_pct: Optional[Decimal] = None
    budget_amount: Optional[Decimal] = None
    headcount_fte: Optional[Decimal] = None


class NodeOut(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    parent_id: Optional[uuid.UUID] = None
    node_level: str
    code: Optional[str] = None
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    bsc_perspective: Optional[str] = None
    progress_pct: Decimal
    status: str
    budget_amount: Decimal = Decimal("0")
    headcount_fte: Decimal = Decimal("0")
    resource_category: Optional[str] = None
    priority: Optional[str] = None
    timeline_start: Optional[date] = None
    timeline_end: Optional[date] = None
    metadata_json: Any = {}
    sort_order: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Pivot Signal ----

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
