# =============================================================
# vMarketing Org — Campaign Entity (Campaign Orchestrator — ABM)
# GovernanceID: vmarketing-org.0.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, Numeric, String, Uuid,
)

from app.database import Base
from app.campaign.models._types import FlexibleJSON


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    campaign_code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    target_segment = Column(String(255), nullable=True)
    stage = Column(String(30), nullable=False, default="AWARENESS")  # AWARENESS | CONSIDERATION | NURTURING | CLOSING
    channel = Column(String(100), nullable=True)   # LINKEDIN | EMAIL | WEBINAR | EVENT | MULTI
    budget_amount = Column(Numeric(15, 2), nullable=False, default=0)
    spent_amount = Column(Numeric(15, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="USD")
    target_accounts = Column(Integer, nullable=False, default=0)
    engaged_accounts = Column(Integer, nullable=False, default=0)
    mqls_generated = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT | ACTIVE | PAUSED | COMPLETED
    owner = Column(String(255), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vmkt_camp_status", "status"),
        Index("idx_vmkt_camp_stage", "stage"),
    )
