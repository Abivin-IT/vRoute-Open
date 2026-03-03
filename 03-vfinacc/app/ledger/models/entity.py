# =============================================================
# vFinacc — LedgerEntry ORM Entity
# GovernanceID: vfinacc.0.0
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Index, Numeric, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.ledger.models._types import FlexibleJSON


class LedgerEntry(Base):
    __tablename__ = "vfinacc_ledger_entries"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    entry_number = Column(String(50), nullable=False)
    entry_date = Column(Date, nullable=False)
    description = Column(String(500), nullable=False)
    debit_account = Column(String(100), nullable=False)
    credit_account = Column(String(100), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="VND")
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT | POSTED | FLAGGED | REVERSED
    cost_center = Column(String(100), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    posted_by = Column(String(255), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    transactions = relationship("Transaction", back_populates="ledger_entry", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="ledger_entry", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vfinacc_ledger_status", "status"),
        Index("idx_vfinacc_ledger_date", "entry_date"),
    )
