# =============================================================
# pivot_signal/models/entity.py — Pivot Signal (SQLAlchemy ORM)
# @GovernanceID vstrategy.0.2
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base


# ---------- Pivot Signal ----------
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
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    plan = relationship("Plan", back_populates="signals")

    __table_args__ = (
        Index("idx_vstrategy_signal_plan", "plan_id"),
        Index("idx_vstrategy_signal_trig", "triggered"),
    )
