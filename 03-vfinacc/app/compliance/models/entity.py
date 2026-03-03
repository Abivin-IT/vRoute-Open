# =============================================================
# vFinacc — ComplianceCheck ORM Entity
# GovernanceID: vfinacc.0.4
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Numeric, String, Text, Uuid
from sqlalchemy.orm import relationship

from app.database import Base


class ComplianceCheck(Base):
    __tablename__ = "vfinacc_compliance_checks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    ledger_entry_id = Column(Uuid, ForeignKey("vfinacc_ledger_entries.id", ondelete="SET NULL"), nullable=True)
    check_type = Column(String(50), nullable=False)  # TAX_VAT | TAX_CIT | THRESHOLD | POLICY
    result = Column(String(20), nullable=False)  # PASS | FLAG | FAIL
    tax_applicable = Column(Boolean, nullable=False, default=False)
    tax_rate_pct = Column(Numeric(5, 2), nullable=True)
    tax_amount = Column(Numeric(15, 2), nullable=True)
    notes = Column(Text, nullable=True)
    checked_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    ledger_entry = relationship("LedgerEntry", back_populates="compliance_checks")

    __table_args__ = (
        Index("idx_vfinacc_compl_type", "check_type"),
        Index("idx_vfinacc_compl_result", "result"),
    )
