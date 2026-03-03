# =============================================================
# vMarketing Org — ContentAsset Entity (Media Management)
# GovernanceID: vmarketing-org.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, Index, Integer, String, Uuid,
)

from app.database import Base
from app.campaign.models._types import FlexibleJSON


class ContentAsset(Base):
    __tablename__ = "content_assets"

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
