# =============================================================
# vMarketing Org — AudienceSegment Entity (Target Groups)
# GovernanceID: vmarketing-org.0.2
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, String, Text, Uuid,
)

from app.database import Base
from app.campaign.models._types import FlexibleJSON


class AudienceSegment(Base):
    __tablename__ = "audience_segments"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    segment_code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    criteria_json = Column(FlexibleJSON, default={})  # e.g. {"industry": "Banking", "revenue_min": 10000000}
    account_count = Column(Integer, nullable=False, default=0)
    tier = Column(String(20), nullable=False, default="TIER_3")  # TIER_1 | TIER_2 | TIER_3
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE | ARCHIVED
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vmkt_seg_tier", "tier"),
        Index("idx_vmkt_seg_status", "status"),
    )
