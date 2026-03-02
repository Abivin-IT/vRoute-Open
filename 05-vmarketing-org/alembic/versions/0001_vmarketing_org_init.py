"""vMarketing Org — initial schema (5 tables + seed data)

Revision ID: 0001
Create Date: 2025-01-01 00:00:00.000000
"""

# Alembic standard naming-convention globals  # noqa: F841
revision = "0001"  # noqa: F841
down_revision = None  # noqa: F841
branch_labels = None  # noqa: F841
depends_on = None  # noqa: F841

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


def upgrade() -> None:
    # ---- campaigns ----
    op.create_table(
        "campaigns",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("campaign_code", sa.String(64), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("target_segment", sa.String(128)),
        sa.Column("stage", sa.String(32), server_default="AWARENESS"),
        sa.Column("channel", sa.String(64)),
        sa.Column("budget_amount", sa.Numeric(18, 2), server_default="0"),
        sa.Column("spent_amount", sa.Numeric(18, 2), server_default="0"),
        sa.Column("currency", sa.String(8), server_default="USD"),
        sa.Column("target_accounts", sa.Integer, server_default="0"),
        sa.Column("engaged_accounts", sa.Integer, server_default="0"),
        sa.Column("mqls_generated", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(32), server_default="DRAFT"),
        sa.Column("owner", sa.String(128)),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_campaigns_tenant_status", "campaigns", ["tenant_id", "status"])

    # ---- tracking_events ----
    op.create_table(
        "tracking_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("event_code", sa.String(64), unique=True, nullable=False),
        sa.Column("organization", sa.String(256), nullable=False),
        sa.Column("action_type", sa.String(32), nullable=False),
        sa.Column("page_resource", sa.String(512)),
        sa.Column("dwell_seconds", sa.Integer, server_default="0"),
        sa.Column("intent_score", sa.Integer, server_default="0"),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("user_agent", sa.Text),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_tracking_events_org", "tracking_events", ["tenant_id", "organization"])

    # ---- audience_segments ----
    op.create_table(
        "audience_segments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("segment_code", sa.String(64), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("criteria_json", JSONB, server_default="{}"),
        sa.Column("account_count", sa.Integer, server_default="0"),
        sa.Column("tier", sa.String(16), server_default="TIER_3"),
        sa.Column("status", sa.String(32), server_default="ACTIVE"),
        sa.Column("created_by", sa.String(128)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audience_segments_tenant_tier", "audience_segments", ["tenant_id", "tier"])

    # ---- content_assets ----
    op.create_table(
        "content_assets",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("asset_code", sa.String(64), unique=True, nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("asset_type", sa.String(32), nullable=False),
        sa.Column("format_type", sa.String(32)),
        sa.Column("url", sa.String(512)),
        sa.Column("target_stage", sa.String(32)),
        sa.Column("downloads", sa.Integer, server_default="0"),
        sa.Column("views", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(32), server_default="DRAFT"),
        sa.Column("created_by", sa.String(128)),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_content_assets_tenant_type", "content_assets", ["tenant_id", "asset_type"])

    # ---- lead_scores ----
    op.create_table(
        "lead_scores",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("organization", sa.String(256), nullable=False),
        sa.Column("contact_name", sa.String(128)),
        sa.Column("contact_title", sa.String(128)),
        sa.Column("score", sa.Integer, server_default="0"),
        sa.Column("grade", sa.String(16), server_default="COLD"),
        sa.Column("scoring_factors", JSONB, server_default="{}"),
        sa.Column("status", sa.String(32), server_default="NEW"),
        sa.Column("handed_off_to", sa.String(128)),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_lead_scores_tenant_grade", "lead_scores", ["tenant_id", "grade"])

    # ---- seed data ----
    tenant = "00000000-0000-0000-0000-000000000001"

    op.execute(f"""
        INSERT INTO campaigns (tenant_id, campaign_code, name, target_segment, stage, channel, budget_amount, status, owner)
        VALUES
          ('{tenant}', 'CAMP-2025-Q1', 'Q1 ABM Outreach', 'Enterprise Logistics', 'AWARENESS', 'LinkedIn', 50000, 'DRAFT', 'marketing-team'),
          ('{tenant}', 'CAMP-2025-Q2', 'Q2 Content Push',  'Mid-Market Supply Chain', 'CONSIDERATION', 'Email', 30000, 'DRAFT', 'marketing-team');
    """)

    op.execute(f"""
        INSERT INTO audience_segments (tenant_id, segment_code, name, tier, account_count, created_by)
        VALUES
          ('{tenant}', 'SEG-ENTERPRISE', 'Enterprise Tier 1', 'TIER_1', 120, 'system'),
          ('{tenant}', 'SEG-MIDMARKET',  'Mid-Market Tier 2', 'TIER_2', 350, 'system');
    """)

    op.execute(f"""
        INSERT INTO content_assets (tenant_id, asset_code, title, asset_type, target_stage, status, created_by)
        VALUES
          ('{tenant}', 'ASSET-WP-001', 'Supply Chain Optimization Whitepaper', 'WHITEPAPER', 'AWARENESS', 'PUBLISHED', 'content-team'),
          ('{tenant}', 'ASSET-CS-001', 'Abivin Customer Success Story',        'CASE_STUDY', 'CONSIDERATION', 'DRAFT', 'content-team');
    """)


def downgrade() -> None:
    op.drop_table("lead_scores")
    op.drop_table("content_assets")
    op.drop_table("audience_segments")
    op.drop_table("tracking_events")
    op.drop_table("campaigns")
