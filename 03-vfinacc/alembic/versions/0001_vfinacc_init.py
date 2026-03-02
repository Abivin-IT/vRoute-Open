"""vfinacc_init — Schema + Seed Data

Revision ID: 0001
Revises: None
Create Date: 2026-03-12
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- Ledger Entries (Journal Entry → General Ledger) ----
    op.create_table(
        "vfinacc_ledger_entries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("entry_number", sa.String(50), nullable=False),
        sa.Column("entry_date", sa.Date, nullable=False),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("debit_account", sa.String(100), nullable=False),
        sa.Column("credit_account", sa.String(100), nullable=False),
        sa.Column("amount", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="VND"),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("cost_center", sa.String(100), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("posted_by", sa.String(255), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vfinacc_ledger_status", "vfinacc_ledger_entries", ["status"])
    op.create_index("idx_vfinacc_ledger_date", "vfinacc_ledger_entries", ["entry_date"])

    # ---- Transactions (Raw ingested from external sources) ----
    op.create_table(
        "vfinacc_transactions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("amount", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="VND"),
        sa.Column("counterparty", sa.String(255), nullable=True),
        sa.Column("transaction_date", sa.Date, nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="RAW"),
        sa.Column("ledger_entry_id", UUID(as_uuid=True), sa.ForeignKey("vfinacc_ledger_entries.id", ondelete="SET NULL"), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vfinacc_txn_source", "vfinacc_transactions", ["source"])
    op.create_index("idx_vfinacc_txn_status", "vfinacc_transactions", ["status"])
    op.create_index("idx_vfinacc_txn_date", "vfinacc_transactions", ["transaction_date"])

    # ---- Reconciliation Matches (3-Way: PO ↔ GRN ↔ Invoice) ----
    op.create_table(
        "vfinacc_reconciliation_matches",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("po_reference", sa.String(100), nullable=True),
        sa.Column("grn_reference", sa.String(100), nullable=True),
        sa.Column("invoice_reference", sa.String(100), nullable=True),
        sa.Column("match_type", sa.String(20), nullable=False),
        sa.Column("confidence_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("discrepancy_amount", sa.Numeric(15, 2), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("reviewed_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vfinacc_recon_type", "vfinacc_reconciliation_matches", ["match_type"])
    op.create_index("idx_vfinacc_recon_status", "vfinacc_reconciliation_matches", ["status"])

    # ---- Cost Allocations (GROW / RUN / TRANSFORM / GIVE) ----
    op.create_table(
        "vfinacc_cost_allocations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("cost_center_code", sa.String(50), nullable=False),
        sa.Column("cost_center_name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(20), nullable=False),
        sa.Column("budget_amount", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("actual_amount", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="VND"),
        sa.Column("period_label", sa.String(50), nullable=False),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vfinacc_cost_category", "vfinacc_cost_allocations", ["category"])
    op.create_index("idx_vfinacc_cost_period", "vfinacc_cost_allocations", ["period_label"])

    # ---- Compliance Checks (Tax & Compliance Guard) ----
    op.create_table(
        "vfinacc_compliance_checks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("ledger_entry_id", UUID(as_uuid=True), sa.ForeignKey("vfinacc_ledger_entries.id", ondelete="SET NULL"), nullable=True),
        sa.Column("check_type", sa.String(50), nullable=False),
        sa.Column("result", sa.String(20), nullable=False),
        sa.Column("tax_applicable", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("tax_rate_pct", sa.Numeric(5, 2), nullable=True),
        sa.Column("tax_amount", sa.Numeric(15, 2), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("checked_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vfinacc_compl_type", "vfinacc_compliance_checks", ["check_type"])
    op.create_index("idx_vfinacc_compl_result", "vfinacc_compliance_checks", ["result"])

    # ---- Seed Data: Demo ledger entries ----
    op.execute(sa.text("""
INSERT INTO vfinacc_ledger_entries (id, entry_number, entry_date, description, debit_account, credit_account, amount, currency, status, cost_center, posted_by, posted_at, created_by)
VALUES
    ('30000000-0000-0000-0000-000000000001', 'JE-2026-0001', '2026-01-15', 'AWS Infrastructure Payment Q1', '6110-R&D-Infra', '2100-Accounts-Payable', 2400.00, 'USD', 'POSTED', 'R&D - Infrastructure', 'system', now(), 'system'),
    ('30000000-0000-0000-0000-000000000002', 'JE-2026-0002', '2026-01-20', 'Office Rent Hanoi HQ', '6200-Office-Rent', '1100-Cash', 5000.00, 'USD', 'POSTED', 'Admin - Office', 'system', now(), 'system'),
    ('30000000-0000-0000-0000-000000000003', 'JE-2026-0003', '2026-02-01', 'Marketing Campaign Q1 - Google Ads', '6300-Marketing', '2100-Accounts-Payable', 8500.00, 'USD', 'DRAFT', 'Marketing - Digital', NULL, NULL, 'system'),
    ('30000000-0000-0000-0000-000000000004', 'JE-2026-0004', '2026-02-10', 'Salary Payroll Feb 2026', '6400-Salaries', '1100-Cash', 85000.00, 'USD', 'POSTED', 'HR - Payroll', 'system', now(), 'system')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vfinacc_transactions (id, external_id, source, amount, currency, counterparty, transaction_date, description, status, ledger_entry_id)
VALUES
    ('31000000-0000-0000-0000-000000000001', 'BANK-TXN-20260115-001', 'BANK_WEBHOOK', 2400.00, 'USD', 'Amazon Web Services', '2026-01-15', 'AWS monthly invoice', 'RECONCILED', '30000000-0000-0000-0000-000000000001'),
    ('31000000-0000-0000-0000-000000000002', 'STRIPE-CHG-20260120', 'STRIPE', 5000.00, 'USD', 'Landlord Corp', '2026-01-20', 'Office rent auto-debit', 'MATCHED', '30000000-0000-0000-0000-000000000002'),
    ('31000000-0000-0000-0000-000000000003', NULL, 'MANUAL', 8500.00, 'USD', 'Google LLC', '2026-02-01', 'Google Ads payment pending', 'RAW', NULL)
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vfinacc_reconciliation_matches (id, po_reference, grn_reference, invoice_reference, match_type, confidence_pct, discrepancy_amount, status, notes)
VALUES
    ('32000000-0000-0000-0000-000000000001', 'PO-2026-001', 'GRN-2026-001', 'INV-AWS-2026-01', 'FULL_MATCH', 100.00, NULL, 'APPROVED', '3-way match: PO, GRN, and Invoice amounts match exactly.'),
    ('32000000-0000-0000-0000-000000000002', 'PO-2026-002', NULL, 'INV-GOOGLE-2026-01', 'PARTIAL_MATCH', 66.67, 500.00, 'PENDING', 'Partial match: 2/3 legs present. GRN missing.')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vfinacc_cost_allocations (id, cost_center_code, cost_center_name, category, budget_amount, actual_amount, currency, period_label, owner)
VALUES
    ('33000000-0000-0000-0000-000000000001', 'CC-SALES', 'Sales & Business Development', 'GROW', 680000.00, 520000.00, 'USD', 'Q1-2026', 'CMO'),
    ('33000000-0000-0000-0000-000000000002', 'CC-INFRA', 'Cloud Infrastructure & IT Ops', 'RUN', 270000.00, 195000.00, 'USD', 'Q1-2026', 'CAO'),
    ('33000000-0000-0000-0000-000000000003', 'CC-RND', 'AI Research & Development', 'TRANSFORM', 50000.00, 32000.00, 'USD', 'Q1-2026', 'CPO'),
    ('33000000-0000-0000-0000-000000000004', 'CC-CSR', 'Community & CSR Programs', 'GIVE', 1000.00, 800.00, 'USD', 'Q1-2026', 'CEO')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vfinacc_compliance_checks (id, ledger_entry_id, check_type, result, tax_applicable, tax_rate_pct, tax_amount, notes, checked_by)
VALUES
    ('34000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'TAX_VAT', 'PASS', true, 10.00, 240.00, 'VAT 10% applied. Tax amount: 240.00', 'system'),
    ('34000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000004', 'THRESHOLD', 'FLAG', false, NULL, NULL, 'Amount 85000.00 exceeds review threshold 25000', 'system')
ON CONFLICT (id) DO NOTHING
"""))


def downgrade() -> None:
    op.drop_table("vfinacc_compliance_checks")
    op.drop_table("vfinacc_cost_allocations")
    op.drop_table("vfinacc_reconciliation_matches")
    op.drop_table("vfinacc_transactions")
    op.drop_table("vfinacc_ledger_entries")
