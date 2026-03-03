# =============================================================
# vDesign Physical — Golden Sample Pydantic Schemas
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


class GoldenSampleCreate(BaseModel):
    sample_code: str
    product_name: str
    material: Optional[str] = None
    weight_actual: Optional[Decimal] = None
    weight_spec: Optional[Decimal] = None
    dimension_x_mm: Optional[Decimal] = None
    dimension_y_mm: Optional[Decimal] = None
    dimension_z_mm: Optional[Decimal] = None
    convergence_pct: Decimal = Decimal("0")
    storage_zone: Optional[str] = None
    storage_shelf: Optional[str] = None
    custodian: Optional[str] = None
    seal_tag_id: Optional[str] = None
    linked_spec_id: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None


class GoldenSampleUpdate(BaseModel):
    product_name: Optional[str] = None
    material: Optional[str] = None
    weight_actual: Optional[Decimal] = None
    convergence_pct: Optional[Decimal] = None
    storage_zone: Optional[str] = None
    storage_shelf: Optional[str] = None
    custodian: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: Optional[Any] = None


class GoldenSampleOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    sample_code: str
    product_name: str
    material: Optional[str] = None
    weight_actual: Optional[Decimal] = None
    weight_spec: Optional[Decimal] = None
    dimension_x_mm: Optional[Decimal] = None
    dimension_y_mm: Optional[Decimal] = None
    dimension_z_mm: Optional[Decimal] = None
    convergence_pct: Decimal
    status: str
    storage_zone: Optional[str] = None
    storage_shelf: Optional[str] = None
    custodian: Optional[str] = None
    seal_tag_id: Optional[str] = None
    linked_spec_id: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: Any = {}
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
