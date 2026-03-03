# =============================================================
# vDesign Physical — Material Inbox ORM Entity
# GovernanceID: vdesign-physical.0.1
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, String, Uuid,
)

from app.database import Base
from app.golden_sample.models._types import FlexibleJSON


class MaterialInbox(Base):
    __tablename__ = "vdesign_material_inbox"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    item_code = Column(String(50), nullable=False)
    source_type = Column(String(50), nullable=False)   # SUPPLIER | COMPETITOR | RND_HANDMADE | MARKET
    supplier_name = Column(String(255), nullable=True)
    description = Column(String(500), nullable=False)
    material_type = Column(String(100), nullable=True)  # e.g. Carbon Fiber, PC-ABS, Clay
    initial_assessment = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING | TESTED | ARCHIVED | SCRAPPED
    qr_tag_id = Column(String(100), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    received_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vdesign_mat_source", "source_type"),
        Index("idx_vdesign_mat_status", "status"),
    )
