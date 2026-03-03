# =============================================================
# vStrategy — Sample / Demo Data (no database required)
# Provides hardcoded sample data for all API endpoints so the
# UI renders correctly in development without PostgreSQL.
#
# @GovernanceID vstrategy.0.0-SAMPLE
# =============================================================
"""
Sample data aligned with the PRD (vstrategy-prd.md):
  - FR-STR-00: Alignment Tree (Vision → BSC → OKR → Initiative → Task)
  - FR-STR-01: Contextual Baseline & Objectives
  - FR-STR-02: Strategic Analysis (MECE options)
  - FR-STR-03: S&OP 68/27/5 resource allocation
  - FR-STR-04: BSC Scorecard + Pivot Signals
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

# ── Fixed UUIDs for deterministic data ──────────────────────
PLAN_Q1 = "a0000001-0001-4000-8000-000000000001"
PLAN_Q2 = "a0000001-0002-4000-8000-000000000002"
PLAN_ANNUAL = "a0000001-0003-4000-8000-000000000003"

NODE_VISION    = "b0000001-0001-4000-8000-000000000001"
NODE_BSC_FIN   = "b0000001-0002-4000-8000-000000000002"
NODE_BSC_CUS   = "b0000001-0003-4000-8000-000000000003"
NODE_BSC_PROC  = "b0000001-0004-4000-8000-000000000004"
NODE_BSC_LEARN = "b0000001-0005-4000-8000-000000000005"
NODE_OKR1      = "b0000001-0006-4000-8000-000000000006"
NODE_OKR2      = "b0000001-0007-4000-8000-000000000007"
NODE_INIT1     = "b0000001-0008-4000-8000-000000000008"
NODE_INIT2     = "b0000001-0009-4000-8000-000000000009"
NODE_TASK1     = "b0000001-000a-4000-8000-00000000000a"
NODE_TASK2     = "b0000001-000b-4000-8000-00000000000b"
NODE_TASK3     = "b0000001-000c-4000-8000-00000000000c"

SIGNAL_1 = "c0000001-0001-4000-8000-000000000001"
SIGNAL_2 = "c0000001-0002-4000-8000-000000000002"

NOW = datetime(2026, 3, 1, 8, 0, 0, tzinfo=timezone.utc).isoformat()

# ═════════════════════════════════════════════════════════════
# FR-STR-01  —  Plans (Baseline & Objectives)
# ═════════════════════════════════════════════════════════════
SAMPLE_PLANS = [
    {
        "id": PLAN_Q1,
        "tenant_id": "00000000-0000-0000-0000-000000000001",
        "period_type": "QUARTERLY",
        "period_label": "Q1-2026",
        "status": "ACTIVE",
        "baseline_json": {
            "fiscal": {
                "cash_balance": 2400000,
                "runway_months": 8,
                "monthly_burn": 300000,
                "hard_cap": 5000000,
            },
            "market": {
                "tam": 500000000,
                "sam": 75000000,
                "som": 12000000,
            },
        },
        "objectives_json": {
            "growth_targets": {
                "arr_target": 3600000,
                "arr_current": 2800000,
                "net_new_arr": 800000,
            },
            "icp": "Mid-market logistics, 200+ employees, SEA region",
            "usp": "AI-powered route optimisation with 15% fuel savings",
        },
        "gap_analysis_json": {
            "gaps": {
                "arr_gap": 800000,
                "pipeline_gap": 2400000,
                "headcount_gap": 12,
            },
            "pestle": {
                "political": "Stable — ASEAN digital economy push",
                "economic": "Inflation cooling, FDI rising in Vietnam",
                "social": "Remote-hybrid demand growing logistics SaaS",
                "tech": "LLM integration opportunity for scheduling",
                "legal": "PDPA compliance needed for Thai expansion",
                "environmental": "Carbon offset tracking = upsell opportunity",
            },
        },
        "mece_options_json": [
            {
                "code": "GROWTH",
                "name": "Aggressive Growth",
                "description": "Triple pipeline, expand SEA, hire 15 AEs",
                "risk": "HIGH",
                "reward": "HIGH",
                "burn_qtr": 900000,
            },
            {
                "code": "PROFIT",
                "name": "Profit Optimisation",
                "description": "Focus NRR >120%, reduce CAC, automate onboarding",
                "risk": "LOW",
                "reward": "MEDIUM",
                "burn_qtr": 450000,
            },
            {
                "code": "PIVOT",
                "name": "Market Pivot",
                "description": "Enter cold-chain vertical, partner w/ pharma distributors",
                "risk": "MEDIUM",
                "reward": "HIGH",
                "burn_qtr": 600000,
            },
            {
                "code": "SURVIVAL",
                "name": "Cash Preservation",
                "description": "Freeze hiring, cut non-core spend, extend runway to 14 months",
                "risk": "LOW",
                "reward": "LOW",
                "burn_qtr": 250000,
            },
        ],
        "selected_option": "GROWTH",
        "decision_log_json": {
            "ceo_comment": "Go aggressive on SEA expansion — revenue momentum critical before Series B",
            "decided_by": "CEO — Pham Nguyen",
            "decided_at": "2026-01-15",
        },
        "sop_config_json": {
            "grow_pct": 68,
            "run_pct": 27,
            "transform_pct": 5,
            "give_pct": 0.1,
            "tolerance_pct": 2,
        },
        "created_by": "CEO — Pham Nguyen",
        "created_at": NOW,
        "updated_at": NOW,
    },
    {
        "id": PLAN_Q2,
        "tenant_id": "00000000-0000-0000-0000-000000000001",
        "period_type": "QUARTERLY",
        "period_label": "Q2-2026",
        "status": "DRAFT",
        "baseline_json": {"fiscal": {"cash_balance": 1800000, "runway_months": 6, "monthly_burn": 300000}},
        "objectives_json": {"growth_targets": {"arr_target": 4200000, "arr_current": 3200000, "net_new_arr": 1000000}},
        "gap_analysis_json": {"gaps": {"arr_gap": 1000000, "pipeline_gap": 3000000}},
        "mece_options_json": [],
        "selected_option": None,
        "decision_log_json": {},
        "sop_config_json": {},
        "created_by": "CAO — Le Thi Minh",
        "created_at": NOW,
        "updated_at": NOW,
    },
    {
        "id": PLAN_ANNUAL,
        "tenant_id": "00000000-0000-0000-0000-000000000001",
        "period_type": "ANNUAL",
        "period_label": "FY-2026",
        "status": "CLOSED",
        "baseline_json": {"fiscal": {"cash_balance": 3200000, "runway_months": 11, "monthly_burn": 290000}},
        "objectives_json": {"growth_targets": {"arr_target": 5000000, "arr_current": 2200000, "net_new_arr": 2800000}},
        "gap_analysis_json": {"gaps": {"arr_gap": 2800000}},
        "mece_options_json": [],
        "selected_option": "PROFIT",
        "decision_log_json": {"ceo_comment": "Conservative approach for annual plan", "decided_by": "CEO — Pham Nguyen", "decided_at": "2025-12-20"},
        "sop_config_json": {},
        "created_by": "CEO — Pham Nguyen",
        "created_at": NOW,
        "updated_at": NOW,
    },
]

# ═════════════════════════════════════════════════════════════
# FR-STR-00  —  Alignment Tree
# ═════════════════════════════════════════════════════════════
SAMPLE_TREE_NODES = [
    # Vision (root)
    {"id": NODE_VISION, "plan_id": PLAN_Q1, "parent_id": None, "node_level": "VISION", "code": "V-001", "title": "Become #1 Logistics SaaS in SEA by 2027", "owner": "CEO — Pham Nguyen", "bsc_perspective": None, "progress_pct": 72.5, "status": "YELLOW", "budget_amount": 0, "headcount_fte": 0, "resource_category": None, "priority": "P0", "sort_order": 0, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    # BSC Perspectives
    {"id": NODE_BSC_FIN,  "plan_id": PLAN_Q1, "parent_id": NODE_VISION, "node_level": "BSC_PERSPECTIVE", "code": "BSC-FIN", "title": "Financial Growth & Sustainability", "owner": "CFO — Tran Van Duc", "bsc_perspective": "FINANCE", "progress_pct": 85.0, "status": "YELLOW", "budget_amount": 680000, "headcount_fte": 5, "resource_category": "GROW", "priority": "P0", "sort_order": 1, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_BSC_CUS,  "plan_id": PLAN_Q1, "parent_id": NODE_VISION, "node_level": "BSC_PERSPECTIVE", "code": "BSC-CUS", "title": "Customer Acquisition & NRR", "owner": "CMO — Nguyen Thi Lan", "bsc_perspective": "CUSTOMER", "progress_pct": 68.0, "status": "RED", "budget_amount": 340000, "headcount_fte": 8, "resource_category": "GROW", "priority": "P0", "sort_order": 2, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_BSC_PROC, "plan_id": PLAN_Q1, "parent_id": NODE_VISION, "node_level": "BSC_PERSPECTIVE", "code": "BSC-PROC", "title": "Operational Excellence", "owner": "CAO — Le Thi Minh", "bsc_perspective": "PROCESS", "progress_pct": 91.0, "status": "GREEN", "budget_amount": 270000, "headcount_fte": 3, "resource_category": "RUN", "priority": "P1", "sort_order": 3, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_BSC_LEARN,"plan_id": PLAN_Q1, "parent_id": NODE_VISION, "node_level": "BSC_PERSPECTIVE", "code": "BSC-LEARN", "title": "Organisation Capability & Learning", "owner": "CPO — Vo Quoc Bao", "bsc_perspective": "LEARNING", "progress_pct": 46.0, "status": "RED", "budget_amount": 50000, "headcount_fte": 2, "resource_category": "TRANSFORM", "priority": "P1", "sort_order": 4, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    # OKRs under Finance
    {"id": NODE_OKR1, "plan_id": PLAN_Q1, "parent_id": NODE_BSC_FIN, "node_level": "OKR", "code": "OKR-001", "title": "Achieve $3.6M ARR by Q1 end", "owner": "VP Sales — Hoang Anh", "bsc_perspective": "FINANCE", "progress_pct": 78.0, "status": "YELLOW", "budget_amount": 400000, "headcount_fte": 3, "resource_category": "GROW", "priority": "P0", "sort_order": 5, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    # OKR under Customer
    {"id": NODE_OKR2, "plan_id": PLAN_Q1, "parent_id": NODE_BSC_CUS, "node_level": "OKR", "code": "OKR-002", "title": "Win 15 new enterprise logos in SEA", "owner": "CMO — Nguyen Thi Lan", "bsc_perspective": "CUSTOMER", "progress_pct": 53.0, "status": "RED", "budget_amount": 250000, "headcount_fte": 5, "resource_category": "GROW", "priority": "P0", "sort_order": 6, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    # Initiatives
    {"id": NODE_INIT1, "plan_id": PLAN_Q1, "parent_id": NODE_OKR1, "node_level": "INITIATIVE", "code": "INIT-01", "title": "Launch Thailand Go-To-Market", "owner": "BD Lead — Somchai", "bsc_perspective": "FINANCE", "progress_pct": 92.0, "status": "GREEN", "budget_amount": 200000, "headcount_fte": 2, "resource_category": "GROW", "priority": "P0", "sort_order": 7, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_INIT2, "plan_id": PLAN_Q1, "parent_id": NODE_OKR2, "node_level": "INITIATIVE", "code": "INIT-02", "title": "Run ABM campaign for top 50 accounts", "owner": "Mkt Lead — Linh", "bsc_perspective": "CUSTOMER", "progress_pct": 45.0, "status": "RED", "budget_amount": 120000, "headcount_fte": 3, "resource_category": "GROW", "priority": "P0", "sort_order": 8, "metadata_json": {"alert": "Behind schedule — awaiting creative assets"}, "created_at": NOW, "updated_at": NOW},
    # Tasks
    {"id": NODE_TASK1, "plan_id": PLAN_Q1, "parent_id": NODE_INIT1, "node_level": "TASK", "code": "TASK-001", "title": "Sign 3 Thai distribution partners", "owner": "BD Lead — Somchai", "bsc_perspective": "FINANCE", "progress_pct": 100.0, "status": "GREEN", "budget_amount": 50000, "headcount_fte": 1, "resource_category": "GROW", "priority": "P0", "sort_order": 9, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_TASK2, "plan_id": PLAN_Q1, "parent_id": NODE_INIT1, "node_level": "TASK", "code": "TASK-002", "title": "Localise product for Thai market", "owner": "PM — Thanh", "bsc_perspective": "FINANCE", "progress_pct": 65.0, "status": "RED", "budget_amount": 80000, "headcount_fte": 1, "resource_category": "GROW", "priority": "P1", "sort_order": 10, "metadata_json": {"alert": "Revenue drop 22% — pivot signal may trigger"}, "created_at": NOW, "updated_at": NOW},
    {"id": NODE_TASK3, "plan_id": PLAN_Q1, "parent_id": NODE_INIT2, "node_level": "TASK", "code": "TASK-003", "title": "Produce 10 personalised ABM landing pages", "owner": "Content — Mai", "bsc_perspective": "CUSTOMER", "progress_pct": 30.0, "status": "RED", "budget_amount": 40000, "headcount_fte": 1, "resource_category": "GROW", "priority": "P1", "sort_order": 11, "metadata_json": {}, "created_at": NOW, "updated_at": NOW},
]

# ═════════════════════════════════════════════════════════════
# FR-STR-04  —  BSC Scorecard (computed from tree)
# ═════════════════════════════════════════════════════════════
SAMPLE_SCORECARD = {
    "plan_id": PLAN_Q1,
    "overall_progress_pct": 72.5,
    "overall_status": "YELLOW",
    "perspectives": [
        {"perspective": "FINANCE",  "title": "Financial Growth & Sustainability", "progress_pct": 85.0, "status": "YELLOW"},
        {"perspective": "CUSTOMER", "title": "Customer Acquisition & NRR",        "progress_pct": 68.0, "status": "RED"},
        {"perspective": "PROCESS",  "title": "Operational Excellence",            "progress_pct": 91.0, "status": "GREEN"},
        {"perspective": "LEARNING", "title": "Organisation Capability & Learning","progress_pct": 46.0, "status": "RED"},
    ],
}

# ═════════════════════════════════════════════════════════════
# FR-STR-03  —  S&OP 68/27/5 Validation
# ═════════════════════════════════════════════════════════════
SAMPLE_SOP = {
    "valid": True,
    "total_budget": 1000000,
    "total_headcount": 18,
    "breakdown": [
        {"category": "GROW",      "owner": "CMO", "target_pct": 68, "actual_pct": 69.0, "status": "ON_TRACK", "amount": 690000},
        {"category": "RUN",       "owner": "CAO", "target_pct": 27, "actual_pct": 27.0, "status": "ON_TRACK", "amount": 270000},
        {"category": "TRANSFORM", "owner": "CPO", "target_pct": 5,  "actual_pct": 4.0,  "status": "ON_TRACK", "amount": 40000},
        {"category": "GIVE",      "owner": "CEO", "target_pct": 0.1,"actual_pct": 0.0,  "status": "ON_TRACK", "amount": 0},
    ],
}

# ═════════════════════════════════════════════════════════════
# FR-STR-04  —  Pivot Signals
# ═════════════════════════════════════════════════════════════
SAMPLE_SIGNALS = [
    {
        "id": SIGNAL_1,
        "plan_id": PLAN_Q1,
        "rule_code": "RUNWAY_SECURITY",
        "rule_description": "Cash runway drops below 6-month threshold",
        "threshold_value": 6.0,
        "actual_value": 8.0,
        "variance_pct": 33.33,
        "triggered": False,
        "severity": "INFO",
        "recommendation": "SAFE ZONE — Runway at 8.0 months (threshold: 6)",
        "resolution": None,
        "resolved_by": None,
        "created_at": NOW,
        "resolved_at": None,
    },
    {
        "id": SIGNAL_2,
        "plan_id": PLAN_Q1,
        "rule_code": "GROWTH_MOMENTUM",
        "rule_description": "Revenue drop exceeds 20% quarter-over-quarter",
        "threshold_value": 20.0,
        "actual_value": 22.0,
        "variance_pct": 10.0,
        "triggered": True,
        "severity": "CRITICAL",
        "recommendation": "PIVOT REQUIRED — Revenue drop 22.0% exceeds 20% threshold. CEO notified: Critical Pivot Trigger.",
        "resolution": None,
        "resolved_by": None,
        "created_at": NOW,
        "resolved_at": None,
    },
]


# ═════════════════════════════════════════════════════════════
# Public functions used by the routes module
# ═════════════════════════════════════════════════════════════

def get_sample_plans(status: str | None = None) -> dict:
    plans = SAMPLE_PLANS
    if status:
        plans = [p for p in plans if p["status"] == status]
    return {"count": len(plans), "plans": plans}


def get_sample_plan(plan_id: str) -> dict | None:
    for p in SAMPLE_PLANS:
        if p["id"] == plan_id:
            return p
    return None


def get_sample_tree(plan_id: str) -> dict:
    nodes = [n for n in SAMPLE_TREE_NODES if n["plan_id"] == plan_id]
    return {"plan_id": plan_id, "count": len(nodes), "nodes": nodes}


def get_sample_scorecard(plan_id: str) -> dict:
    if plan_id == PLAN_Q1:
        return SAMPLE_SCORECARD
    return {"plan_id": plan_id, "overall_progress_pct": 0, "overall_status": "RED", "perspectives": []}


def get_sample_sop(plan_id: str) -> dict:
    if plan_id == PLAN_Q1:
        return SAMPLE_SOP
    return {"valid": False, "total_budget": 0, "total_headcount": 0, "breakdown": []}


def get_sample_signals(plan_id: str) -> dict:
    signals = [s for s in SAMPLE_SIGNALS if s["plan_id"] == plan_id]
    return {"count": len(signals), "signals": signals}
