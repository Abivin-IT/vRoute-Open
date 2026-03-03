# =============================================================
# vFinacc — ReconciliationMatch ORM Entity
# GovernanceID: vfinacc.0.2
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, Numeric, String, Text, Uuid

from app.database import Base


class ReconciliationMatch(Base):
    __tablename__ = "vfinacc_reconciliation_matches"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    po_reference = Column(String(100), nullable=True)
    grn_reference = Column(String(100), nullable=True)
    invoice_reference = Column(String(100), nullable=True)
    match_type = Column(String(20), nullable=False)  # FULL_MATCH | PARTIAL_MATCH | NO_MATCH
    confidence_pct = Column(Numeric(5, 2), nullable=False, default=0)
    discrepancy_amount = Column(Numeric(15, 2), nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING | APPROVED | REJECTED
    notes = Column(Text, nullable=True)
    reviewed_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vfinacc_recon_type", "match_type"),
        Index("idx_vfinacc_recon_status", "status"),
    )
