# =============================================================
# vDesign Physical — Lab Test ORM Entity
# GovernanceID: vdesign-physical.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, ForeignKey, Index, String, Text, Uuid,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.golden_sample.models._types import FlexibleJSON


class LabTest(Base):
    __tablename__ = "vdesign_lab_tests"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    test_code = Column(String(50), nullable=False)
    test_type = Column(String(50), nullable=False)  # STRESS | DROP | THERMAL | CHEMICAL | HARDNESS
    golden_sample_id = Column(Uuid, ForeignKey("vdesign_golden_samples.id", ondelete="SET NULL"), nullable=True)
    prototype_id = Column(Uuid, ForeignKey("vdesign_prototypes.id", ondelete="SET NULL"), nullable=True)
    result = Column(String(20), nullable=False, default="RUNNING")  # RUNNING | PASSED | FAILED | CONDITIONAL
    measured_value = Column(String(255), nullable=True)
    threshold_value = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    tested_by = Column(String(255), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    golden_sample = relationship("GoldenSample", back_populates="lab_tests")
    prototype = relationship("Prototype", back_populates="lab_tests")

    __table_args__ = (
        Index("idx_vdesign_lab_type", "test_type"),
        Index("idx_vdesign_lab_result", "result"),
    )
