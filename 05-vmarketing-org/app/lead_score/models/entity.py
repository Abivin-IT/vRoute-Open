# =============================================================
# vMarketing Org — LeadScore Entity (AI Qualification)
# GovernanceID: vmarketing-org.0.4
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, String, Text, Uuid,
)

from app.database import Base
from app.campaign.models._types import FlexibleJSON


class LeadScore(Base):
    __tablename__ = "lead_scores"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    organization = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=True)
    contact_title = Column(String(255), nullable=True)
    score = Column(Integer, nullable=False, default=0)         # 0-100
    grade = Column(String(10), nullable=False, default="COLD")  # HOT | WARM | COLD
    scoring_factors = Column(FlexibleJSON, default={})         # e.g. {"downloads": 3, "dwell_time": 900, "pricing_view": true}
    status = Column(String(20), nullable=False, default="NEW")  # NEW | QUALIFIED | HANDED_OFF | DISQUALIFIED
    handed_off_to = Column(String(255), nullable=True)         # Sales rep
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vmkt_lead_grade", "grade"),
        Index("idx_vmkt_lead_status", "status"),
        Index("idx_vmkt_lead_org", "organization"),
    )
