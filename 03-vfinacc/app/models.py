# =============================================================
# vFinacc — SQLAlchemy ORM Models
# GovernanceID: vfinacc.0.0 (LedgerEntry), vfinacc.0.1 (Transaction),
#   vfinacc.0.2 (ReconciliationMatch), vfinacc.0.3 (CostAllocation),
#   vfinacc.0.4 (ComplianceCheck)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, Date, DateTime, ForeignKey, Index, Numeric, String, Text,
    JSON, Uuid,
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


# ---------- Ledger Entry (Journal Entry → General Ledger) ----------
# @GovernanceID vfinacc.0.0
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


# ---------- Raw Transaction (Ingested from external sources) ----------
# @GovernanceID vfinacc.0.1
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


# ---------- Reconciliation Match (3-Way: PO ↔ GRN ↔ Invoice) ----------
# @GovernanceID vfinacc.0.2
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


# ---------- Cost Allocation (GROW / RUN / TRANSFORM / GIVE) ----------
# @GovernanceID vfinacc.0.3
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


# ---------- Tax & Compliance Check ----------
# @GovernanceID vfinacc.0.4
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
