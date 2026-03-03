# =============================================================
# alignment/models/schema.py — Alignment Node Pydantic DTOs
# @GovernanceID vstrategy.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


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
