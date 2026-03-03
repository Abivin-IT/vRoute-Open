# =============================================================
# vMarketing Org — TrackingEvent Entity (Behavioral Data)
# GovernanceID: vmarketing-org.0.1
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, String, Uuid,
)

from app.database import Base
from app.campaign.models._types import FlexibleJSON


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    event_code = Column(String(50), nullable=False)
    organization = Column(String(255), nullable=False)
    action_type = Column(String(50), nullable=False)  # PAGE_VIEW | DOWNLOAD_PDF | PRICING_COMPARE | VIDEO_WATCH | EXIT_INTENT
    page_resource = Column(String(500), nullable=True)
    dwell_seconds = Column(Integer, nullable=False, default=0)
    intent_score = Column(Integer, nullable=False, default=0)   # 0-100
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vmkt_track_org", "organization"),
        Index("idx_vmkt_track_action", "action_type"),
    )
