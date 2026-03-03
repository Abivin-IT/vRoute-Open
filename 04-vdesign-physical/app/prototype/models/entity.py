# =============================================================
# vDesign Physical — Prototype ORM Entity
# GovernanceID: vdesign-physical.0.2
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, String, Text, Uuid,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.golden_sample.models._types import FlexibleJSON


class Prototype(Base):
    __tablename__ = "vdesign_prototypes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    proto_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    version_label = Column(String(50), nullable=False)  # V1, V2, V3...
    fabrication_method = Column(String(100), nullable=True)  # 3D_PRINT | CNC | INJECTION | HANDMADE
    rfid_tag_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE | IN_TRANSIT | OBSOLETE | DESTROYED
    location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lab_tests = relationship("LabTest", back_populates="prototype", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vdesign_proto_status", "status"),
        Index("idx_vdesign_proto_code", "proto_code"),
    )
