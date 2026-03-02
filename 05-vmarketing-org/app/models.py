# =============================================================
# vMarketing Org — SQLAlchemy ORM Models
# GovernanceID: vmarketing-org.0.0 (Campaign),
#   vmarketing-org.0.1 (TrackingEvent),
#   vmarketing-org.0.2 (AudienceSegment),
#   vmarketing-org.0.3 (ContentAsset),
#   vmarketing-org.0.4 (LeadScore)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, Numeric, String, Text,
    JSON, Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator

from app.database import Base


class FlexibleJSON(TypeDecorator):
    """Use JSONB on PostgreSQL, plain JSON on SQLite/other dialects."""
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())


# ---------- Campaign (Campaign Orchestrator — ABM) ----------
# @GovernanceID vmarketing-org.0.0
class Campaign(Base):
    __tablename__ = "vmkt_campaigns"

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


# ---------- Tracking Event (Tracking Pixel — Behavioral Data) ----------
# @GovernanceID vmarketing-org.0.1
class TrackingEvent(Base):
    __tablename__ = "vmkt_tracking_events"

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


# ---------- Audience Segment (Target Groups) ----------
# @GovernanceID vmarketing-org.0.2
class AudienceSegment(Base):
    __tablename__ = "vmkt_audience_segments"

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


# ---------- Content Asset (Media Management) ----------
# @GovernanceID vmarketing-org.0.3
class ContentAsset(Base):
    __tablename__ = "vmkt_content_assets"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    asset_code = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    asset_type = Column(String(50), nullable=False)   # WHITEPAPER | CASE_STUDY | VIDEO | INFOGRAPHIC | BLOG
    format_type = Column(String(20), nullable=True)    # PDF | MP4 | PNG | HTML
    url = Column(String(500), nullable=True)
    target_stage = Column(String(30), nullable=True)   # AWARENESS | CONSIDERATION | CLOSING
    downloads = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT | PUBLISHED | ARCHIVED
    created_by = Column(String(255), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vmkt_asset_type", "asset_type"),
        Index("idx_vmkt_asset_status", "status"),
    )


# ---------- Lead Score (AI Qualification) ----------
# @GovernanceID vmarketing-org.0.4
class LeadScore(Base):
    __tablename__ = "vmkt_lead_scores"

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
