# =============================================================
# vDesign Physical — Lab Test Pydantic Schemas
# GovernanceID: vdesign-physical.0.5
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


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
