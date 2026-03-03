# =============================================================
# vFinacc — CostAllocation ORM Entity
# GovernanceID: vfinacc.0.3
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, Numeric, String, Uuid

from app.database import Base
from app.ledger.models._types import FlexibleJSON


class CostAllocation(Base):
    __tablename__ = "vfinacc_cost_allocations"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    cost_center_code = Column(String(50), nullable=False)
    cost_center_name = Column(String(255), nullable=False)
    category = Column(String(20), nullable=False)  # GROW | RUN | TRANSFORM | GIVE
    budget_amount = Column(Numeric(15, 2), nullable=False, default=0)
    actual_amount = Column(Numeric(15, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="VND")
    period_label = Column(String(50), nullable=False)
    owner = Column(String(255), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vfinacc_cost_category", "category"),
        Index("idx_vfinacc_cost_period", "period_label"),
    )
