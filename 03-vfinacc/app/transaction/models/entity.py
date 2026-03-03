# =============================================================
# vFinacc — Transaction ORM Entity
# GovernanceID: vfinacc.0.1
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.ledger.models._types import FlexibleJSON


class Transaction(Base):
    __tablename__ = "vfinacc_transactions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    external_id = Column(String(255), nullable=True)
    source = Column(String(50), nullable=False)  # BANK_WEBHOOK | STRIPE | MANUAL | ERP
    amount = Column(Numeric(15, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="VND")
    counterparty = Column(String(255), nullable=True)
    transaction_date = Column(Date, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="RAW")  # RAW | MATCHED | RECONCILED | REJECTED
    ledger_entry_id = Column(Uuid, ForeignKey("vfinacc_ledger_entries.id", ondelete="SET NULL"), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    ledger_entry = relationship("LedgerEntry", back_populates="transactions")

    __table_args__ = (
        Index("idx_vfinacc_txn_source", "source"),
        Index("idx_vfinacc_txn_status", "status"),
        Index("idx_vfinacc_txn_date", "transaction_date"),
    )
