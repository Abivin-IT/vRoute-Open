# =============================================================
# plan/models/entity.py — Strategic Plan (SQLAlchemy ORM)
# @GovernanceID vstrategy.0.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.plan.models._types import FlexibleJSON


# ---------- Strategic Plan ----------
class Plan(Base):
    __tablename__ = "vstrategy_plans"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    period_type = Column(String(20), nullable=False, default="QUARTERLY")
    period_label = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")
    baseline_json = Column(FlexibleJSON, default={})
    objectives_json = Column(FlexibleJSON, default={})
    gap_analysis_json = Column(FlexibleJSON, default={})
    mece_options_json = Column(FlexibleJSON, default=[])
    selected_option = Column(String(20), nullable=True)
    decision_log_json = Column(FlexibleJSON, default={})
    sop_config_json = Column(FlexibleJSON, default={})
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    nodes = relationship("AlignmentNode", back_populates="plan", cascade="all, delete-orphan")
    signals = relationship("PivotSignal", back_populates="plan", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_vstrategy_plan_status", "status"),)
