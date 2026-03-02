"""vstrategy_init — Schema + Seed Data

Revision ID: 0001
Revises: None
Create Date: 2026-03-02
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
    # ---- Strategic Plans ----
    op.create_table(
        "vstrategy_plans",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("period_type", sa.String(20), nullable=False, server_default="QUARTERLY"),
        sa.Column("period_label", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("baseline_json", JSONB, server_default="{}"),
        sa.Column("objectives_json", JSONB, server_default="{}"),
        sa.Column("gap_analysis_json", JSONB, server_default="{}"),
        sa.Column("mece_options_json", JSONB, server_default="[]"),
        sa.Column("selected_option", sa.String(20), nullable=True),
        sa.Column("decision_log_json", JSONB, server_default="{}"),
        sa.Column("sop_config_json", JSONB, server_default="{}"),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vstrategy_plan_status", "vstrategy_plans", ["status"])

    # ---- Alignment Tree Nodes ----
    op.create_table(
        "vstrategy_alignment_nodes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plan_id", UUID(as_uuid=True), sa.ForeignKey("vstrategy_plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_id", UUID(as_uuid=True), sa.ForeignKey("vstrategy_alignment_nodes.id", ondelete="CASCADE"), nullable=True),
        sa.Column("node_level", sa.String(20), nullable=False),
        sa.Column("code", sa.String(50), nullable=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("bsc_perspective", sa.String(20), nullable=True),
        sa.Column("progress_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(10), nullable=False, server_default="GREEN"),
        sa.Column("budget_amount", sa.Numeric(15, 2), server_default="0"),
        sa.Column("headcount_fte", sa.Numeric(5, 1), server_default="0"),
        sa.Column("resource_category", sa.String(20), nullable=True),
        sa.Column("priority", sa.String(10), nullable=True),
        sa.Column("timeline_start", sa.Date, nullable=True),
        sa.Column("timeline_end", sa.Date, nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vstrategy_node_plan", "vstrategy_alignment_nodes", ["plan_id"])
    op.create_index("idx_vstrategy_node_parent", "vstrategy_alignment_nodes", ["parent_id"])
    op.create_index("idx_vstrategy_node_level", "vstrategy_alignment_nodes", ["node_level"])

    # ---- Pivot Signals ----
    op.create_table(
        "vstrategy_pivot_signals",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plan_id", UUID(as_uuid=True), sa.ForeignKey("vstrategy_plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_code", sa.String(50), nullable=False),
        sa.Column("rule_description", sa.String(500), nullable=True),
        sa.Column("threshold_value", sa.Numeric(15, 2), nullable=False),
        sa.Column("actual_value", sa.Numeric(15, 2), nullable=False),
        sa.Column("variance_pct", sa.Numeric(5, 2), nullable=True),
        sa.Column("triggered", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("severity", sa.String(20), nullable=False, server_default="INFO"),
        sa.Column("recommendation", sa.String(500), nullable=True),
        sa.Column("resolution", sa.String(20), nullable=True),
        sa.Column("resolved_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_vstrategy_signal_plan", "vstrategy_pivot_signals", ["plan_id"])
    op.create_index("idx_vstrategy_signal_trig", "vstrategy_pivot_signals", ["triggered"])

    # ---- Seed Data: Demo Q1-2026 Plan ----
    # Use exec_driver_sql to bypass SQLAlchemy text() parsing (avoids ':' in JSON being treated as bindparams)
    op.get_bind().exec_driver_sql("""
INSERT INTO vstrategy_plans (id, period_label, status, baseline_json, objectives_json,
    gap_analysis_json, mece_options_json, selected_option, decision_log_json, sop_config_json, created_by)
VALUES (
    '10000000-0000-0000-0000-000000000001', 'Q1-2026', 'ACTIVE',
    '{"fiscal":{"runway_months":12.5,"cash_balance":2500000,"burn_rate":200000},"market":{"market_share_pct":15,"competitor_moves":"New feature X launched by Competitor A. Price war in Logistics sector."}}',
    '{"market_hypothesis":{"icp":"Target SMEs 50-200 employees in Logistics & Last-mile Delivery","usp":"Real-time Dynamic Route Optimization powered by vKernel AI Agent"},"growth_targets":{"arr_target":500000000,"customer_target":500}}',
    '{"current":{"arr":300000000,"market_share":15,"runway":12.5},"target":{"arr":500000000,"market_share":25,"runway":18},"gaps":{"arr_gap":200000000,"market_gap":10,"runway_gap":5.5}}',
    '[{"code":"GROWTH","name":"Aggressive Expansion","description":"Hire 50%% more sales, double marketing budget","risk":"HIGH","reward":"HIGH","burn_qtr":2000000},{"code":"PROFIT","name":"Optimize Margins","description":"Cut marketing 30%%, focus high-margin clients","risk":"LOW","reward":"MEDIUM","burn_qtr":1000000},{"code":"PIVOT","name":"New Market Shift","description":"Strategic partnership, develop new product line","risk":"HIGH","reward":"HIGH","burn_qtr":1500000},{"code":"SURVIVAL","name":"Cut Costs","description":"Lay off 30%% staff, exit non-core markets","risk":"LOW","reward":"LOW","burn_qtr":200000}]',
    'GROWTH',
    '{"ceo_comment":"We have enough runway for growth. Let''s capture the market share now.","decided_by":"CEO","decided_at":"2025-12-20T10:30:00Z"}',
    '{"grow_pct":68,"run_pct":27,"transform_pct":5,"give_pct":0.1,"total_budget":1000000,"tolerance_pct":2}',
    'system'
);

INSERT INTO vstrategy_alignment_nodes (id, plan_id, node_level, code, title, owner, progress_pct, status, sort_order) VALUES
('20000000-0000-0000-0000-000000000001','10000000-0000-0000-0000-000000000001','VISION','V-001','Become Top 1 Logistics SaaS in Vietnam by 2028','CEO',82,'YELLOW',0);

INSERT INTO vstrategy_alignment_nodes (id, plan_id, parent_id, node_level, code, title, owner, bsc_perspective, progress_pct, status, sort_order) VALUES
('20000000-0000-0000-0000-000000000010','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000001','BSC_PERSPECTIVE','BSC-FIN','Financial Health','CFO','FINANCE',65,'RED',0),
('20000000-0000-0000-0000-000000000020','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000001','BSC_PERSPECTIVE','BSC-CUS','Customer Success','CCO','CUSTOMER',92,'GREEN',1),
('20000000-0000-0000-0000-000000000030','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000001','BSC_PERSPECTIVE','BSC-PRC','Internal Process','COO','PROCESS',78,'YELLOW',2),
('20000000-0000-0000-0000-000000000040','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000001','BSC_PERSPECTIVE','BSC-LRN','Learning & Org Capacity','CHRO','LEARNING',88,'GREEN',3);

INSERT INTO vstrategy_alignment_nodes (id, plan_id, parent_id, node_level, code, title, owner, bsc_perspective, progress_pct, status, sort_order) VALUES
('20000000-0000-0000-0000-000000000011','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000010','OKR','OKR-001','Reach $500M Annual Recurring Revenue (ARR)','CRO','FINANCE',65,'RED',0),
('20000000-0000-0000-0000-000000000021','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000020','OKR','OKR-002','Maintain Net Promoter Score (NPS) > 50','CCO','CUSTOMER',94,'GREEN',0);

INSERT INTO vstrategy_alignment_nodes (id, plan_id, parent_id, node_level, code, title, owner, progress_pct, status, budget_amount, headcount_fte, resource_category, priority, sort_order) VALUES
('20000000-0000-0000-0000-000000000100','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000011','INITIATIVE','P-01','vSales v2 Enterprise Launch','CMO',100,'GREEN',400000,12,'GROW','P1',0),
('20000000-0000-0000-0000-000000000101','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000011','INITIATIVE','P-02','Payment Infrastructure Upgrade','CTO',40,'RED',275000,5,'GROW','P2',1),
('20000000-0000-0000-0000-000000000102','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000030','INITIATIVE','P-03','Cloud Infra Optimization (AWS)','CAO',60,'YELLOW',200000,2,'RUN','P2',0),
('20000000-0000-0000-0000-000000000103','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000030','INITIATIVE','P-04','Office Expansion Hanoi','CAO',80,'GREEN',72000,0,'RUN','P3',1),
('20000000-0000-0000-0000-000000000104','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000040','INITIATIVE','P-05','AI Route Agent R&D (Generative AI)','CPO',45,'YELLOW',52000,3,'TRANSFORM','P1',0),
('20000000-0000-0000-0000-000000000105','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000040','INITIATIVE','P-06','Community Tree Planting (CSR)','CEO',90,'GREEN',1000,0,'GIVE','P3',1);

INSERT INTO vstrategy_alignment_nodes (id, plan_id, parent_id, node_level, code, title, owner, progress_pct, status, sort_order, metadata_json) VALUES
('20000000-0000-0000-0000-001000000000','10000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000101','TASK','TASK-002','Integrate Global Payment Gateway (Stripe/PayPal)','DevLead',35,'RED',0,'{"alert":"API Integration Failed. Blocked by Compliance. (Propagated Risk)"}');

INSERT INTO vstrategy_pivot_signals (plan_id, rule_code, rule_description, threshold_value, actual_value, variance_pct, triggered, severity, recommendation) VALUES
('10000000-0000-0000-0000-000000000001','RUNWAY_SECURITY','Runway < 6 months triggers survival mode',6,12.7,0,false,'INFO','SAFE ZONE — Runway at 12.7 months'),
('10000000-0000-0000-0000-000000000001','GROWTH_MOMENTUM','Revenue drop > 20%% triggers pivot signal',20,5.2,-5.2,false,'INFO','SAFE ZONE — Variance at -5.2%%');
    """)


def downgrade() -> None:
    op.drop_table("vstrategy_pivot_signals")
    op.drop_table("vstrategy_alignment_nodes")
    op.drop_table("vstrategy_plans")
