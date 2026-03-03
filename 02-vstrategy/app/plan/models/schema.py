# =============================================================
# plan/models/schema.py — Plan Pydantic DTOs
# @GovernanceID vstrategy.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


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
