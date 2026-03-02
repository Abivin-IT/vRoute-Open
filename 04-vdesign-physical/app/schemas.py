# =============================================================
# vDesign Physical — Pydantic Schemas (Request / Response DTOs)
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel


# ---- Golden Sample ----

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


# ---- Material Inbox ----

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


# ---- Prototype ----

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


# ---- Lab Test ----

class LabTestCreate(BaseModel):
    test_code: str
    test_type: str  # STRESS | DROP | THERMAL | CHEMICAL | HARDNESS
    golden_sample_id: Optional[uuid.UUID] = None
    prototype_id: Optional[uuid.UUID] = None
    measured_value: Optional[str] = None
    threshold_value: Optional[str] = None
    notes: Optional[str] = None
    tested_by: Optional[str] = None


class LabTestOut(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    test_code: str
    test_type: str
    golden_sample_id: Optional[uuid.UUID] = None
    prototype_id: Optional[uuid.UUID] = None
    result: str
    measured_value: Optional[str] = None
    threshold_value: Optional[str] = None
    notes: Optional[str] = None
    tested_by: Optional[str] = None
    metadata_json: Any = {}
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- Handover Kit ----

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
