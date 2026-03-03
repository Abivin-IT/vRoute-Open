# =============================================================
# alignment/models/entity.py — Alignment Tree Node (SQLAlchemy ORM)
# @GovernanceID vstrategy.0.1
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Column, DateTime, Date, ForeignKey, Index, Integer, Numeric, String, Text, Uuid,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.plan.models._types import FlexibleJSON


# ---------- Alignment Tree Node ----------
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
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

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
