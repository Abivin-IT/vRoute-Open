# =============================================================
# vStrategy — SQLAlchemy ORM Models
# GovernanceID: vstrategy.0.0 (Plan), vstrategy.0.1 (AlignmentNode), vstrategy.0.2 (PivotSignal)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text,
    text, Date, JSON, Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
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


# ---------- Strategic Plan ----------
# @GovernanceID vstrategy.0.0
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
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nodes = relationship("AlignmentNode", back_populates="plan", cascade="all, delete-orphan")
    signals = relationship("PivotSignal", back_populates="plan", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_vstrategy_plan_status", "status"),)


# ---------- Alignment Tree Node ----------
# @GovernanceID vstrategy.0.1
class AlignmentNode(Base):
    __tablename__ = "vstrategy_alignment_nodes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    plan_id = Column(Uuid, ForeignKey("vstrategy_plans.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Uuid, ForeignKey("vstrategy_alignment_nodes.id", ondelete="CASCADE"), nullable=True)
    node_level = Column(String(20), nullable=False)  # VISION | BSC_PERSPECTIVE | OKR | INITIATIVE | TASK
    code = Column(String(50), nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(255), nullable=True)
    bsc_perspective = Column(String(20), nullable=True)  # FINANCE | CUSTOMER | PROCESS | LEARNING
    progress_pct = Column(Numeric(5, 2), nullable=False, default=0)
    status = Column(String(10), nullable=False, default="GREEN")  # GREEN | YELLOW | RED
    budget_amount = Column(Numeric(15, 2), default=0)
    headcount_fte = Column(Numeric(5, 1), default=0)
    resource_category = Column(String(20), nullable=True)  # GROW | RUN | TRANSFORM | GIVE
    priority = Column(String(10), nullable=True)
    timeline_start = Column(Date, nullable=True)
    timeline_end = Column(Date, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    plan = relationship("Plan", back_populates="nodes")
    parent = relationship("AlignmentNode", remote_side=[id], backref="children")

    __table_args__ = (
        Index("idx_vstrategy_node_plan", "plan_id"),
        Index("idx_vstrategy_node_parent", "parent_id"),
        Index("idx_vstrategy_node_level", "node_level"),
    )

    @staticmethod
    def traffic_light(pct: Decimal | float | None) -> str:
        """Compute traffic-light status from progress percentage."""
        if pct is None:
            return "RED"
        v = float(pct)
        if v >= 90:
            return "GREEN"
        if v >= 70:
            return "YELLOW"
        return "RED"


# ---------- Pivot Signal ----------
# @GovernanceID vstrategy.0.2
class PivotSignal(Base):
    __tablename__ = "vstrategy_pivot_signals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    plan_id = Column(Uuid, ForeignKey("vstrategy_plans.id", ondelete="CASCADE"), nullable=False)
    rule_code = Column(String(50), nullable=False)
    rule_description = Column(String(500), nullable=True)
    threshold_value = Column(Numeric(15, 2), nullable=False)
    actual_value = Column(Numeric(15, 2), nullable=False)
    variance_pct = Column(Numeric(5, 2), nullable=True)
    triggered = Column(Boolean, nullable=False, default=False)
    severity = Column(String(20), nullable=False, default="INFO")
    recommendation = Column(String(500), nullable=True)
    resolution = Column(String(20), nullable=True)
    resolved_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    plan = relationship("Plan", back_populates="signals")

    __table_args__ = (
        Index("idx_vstrategy_signal_plan", "plan_id"),
        Index("idx_vstrategy_signal_trig", "triggered"),
    )
