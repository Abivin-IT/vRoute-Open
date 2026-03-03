# =============================================================
# vDesign Physical — Golden Sample ORM Entity
# GovernanceID: vdesign-physical.0.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Numeric, String, Text, Uuid,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.golden_sample.models._types import FlexibleJSON


class GoldenSample(Base):
    __tablename__ = "vdesign_golden_samples"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    sample_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    material = Column(String(255), nullable=True)
    weight_actual = Column(Numeric(10, 3), nullable=True)
    weight_spec = Column(Numeric(10, 3), nullable=True)
    dimension_x_mm = Column(Numeric(10, 3), nullable=True)
    dimension_y_mm = Column(Numeric(10, 3), nullable=True)
    dimension_z_mm = Column(Numeric(10, 3), nullable=True)
    convergence_pct = Column(Numeric(5, 2), nullable=False, default=0)
    status = Column(String(20), nullable=False, default="SEALED")  # SEALED | ACTIVE | COMPROMISED | EXPIRED
    storage_zone = Column(String(100), nullable=True)
    storage_shelf = Column(String(50), nullable=True)
    custodian = Column(String(255), nullable=True)
    seal_tag_id = Column(String(100), nullable=True)
    linked_spec_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lab_tests = relationship("LabTest", back_populates="golden_sample", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vdesign_gs_status", "status"),
        Index("idx_vdesign_gs_code", "sample_code"),
    )
