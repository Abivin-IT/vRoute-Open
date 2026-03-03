# =============================================================
# vDesign Physical — Handover Kit ORM Entity
# GovernanceID: vdesign-physical.0.4
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, String, Text, Uuid,
)

from app.database import Base
from app.golden_sample.models._types import FlexibleJSON


class HandoverKit(Base):
    __tablename__ = "vdesign_handover_kits"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    kit_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    contents_summary = Column(Text, nullable=False)   # e.g. "1x Mold, 2x Jig, 1x Color Sample"
    destination = Column(String(255), nullable=True)   # Factory name / vBuild target
    status = Column(String(20), nullable=False, default="PACKING")  # PACKING | READY | DISPATCHED | RECEIVED
    dispatched_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    packed_by = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vdesign_hk_status", "status"),
        Index("idx_vdesign_hk_code", "kit_code"),
    )
