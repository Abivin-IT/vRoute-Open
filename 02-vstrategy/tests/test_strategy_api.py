# =============================================================
# vStrategy — Integration Tests
# Covers SyR-STR-00 through SyR-STR-04 (20 test cases).
# =============================================================
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# Shared state between ordered tests
_state: dict = {}


# =========== PLAN CRUD ===========

async def test_01_create_plan(client: AsyncClient):
    r = await client.post("/api/v1/vstrategy/plans", json={
        "period_label": "Q1-TEST",
        "period_type": "QUARTERLY",
        "created_by": "test",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["period_label"] == "Q1-TEST"
    assert data["status"] == "DRAFT"
    _state["plan_id"] = data["id"]


async def test_02_list_plans(client: AsyncClient):
    r = await client.get("/api/v1/vstrategy/plans")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_03_update_plan_baseline_and_mece(client: AsyncClient):
    r = await client.put(f"/api/v1/vstrategy/plans/{_state['plan_id']}", json={
        "status": "ACTIVE",
        "baseline_json": {"fiscal": {"runway_months": 12.5, "burn_rate": 200000}},
        "selected_option": "GROWTH",
        "sop_config_json": {
            "grow_pct": 68, "run_pct": 27, "transform_pct": 5,
            "give_pct": 0.1, "total_budget": 1000000, "tolerance_pct": 2,
        },
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ACTIVE"
    assert data["selected_option"] == "GROWTH"


# =========== ALIGNMENT TREE ===========

async def test_10_add_vision_node(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "VISION", "code": "V-001",
        "title": "Top 1 Logistics SaaS by 2028",
        "owner": "CEO", "progress_pct": 80,
    })
    assert r.status_code == 201
    assert r.json()["node_level"] == "VISION"
    _state["vision_id"] = r.json()["id"]


async def test_11_add_bsc_perspective(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "BSC_PERSPECTIVE", "code": "BSC-FIN",
        "title": "Financial Health", "owner": "CFO",
        "parent_id": _state["vision_id"],
        "bsc_perspective": "FINANCE", "progress_pct": 65,
    })
    assert r.status_code == 201
    _state["bsc_fin_id"] = r.json()["id"]


async def test_12_add_okr(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "OKR", "code": "OKR-001",
        "title": "Reach $500M ARR", "owner": "CRO",
        "parent_id": _state["bsc_fin_id"],
        "bsc_perspective": "FINANCE", "progress_pct": 60,
    })
    assert r.status_code == 201
    _state["okr_id"] = r.json()["id"]


async def test_13_add_initiative_with_budget(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "INITIATIVE", "code": "P-01",
        "title": "Enterprise Launch", "owner": "CMO",
        "parent_id": _state["okr_id"],
        "resource_category": "GROW",
        "budget_amount": 680000, "headcount_fte": 12,
        "priority": "P1", "progress_pct": 50,
    })
    assert r.status_code == 201
    _state["initiative_id"] = r.json()["id"]


async def test_14_add_run_initiative(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "INITIATIVE", "code": "P-03",
        "title": "Cloud Infra Optimization", "owner": "CAO",
        "parent_id": _state["okr_id"],
        "resource_category": "RUN",
        "budget_amount": 270000, "headcount_fte": 2, "progress_pct": 60,
    })
    assert r.status_code == 201


async def test_15_add_transform_and_give_initiatives(client: AsyncClient):
    r1 = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "INITIATIVE", "code": "P-05",
        "title": "AI R&D", "owner": "CPO",
        "parent_id": _state["okr_id"],
        "resource_category": "TRANSFORM",
        "budget_amount": 50000, "headcount_fte": 3, "progress_pct": 40,
    })
    assert r1.status_code == 201

    r2 = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "INITIATIVE", "code": "P-06",
        "title": "CSR Tree Planting", "owner": "CEO",
        "parent_id": _state["okr_id"],
        "resource_category": "GIVE",
        "budget_amount": 1000, "progress_pct": 90,
    })
    assert r2.status_code == 201


async def test_16_add_task(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "TASK", "code": "TASK-001",
        "title": "Integrate Payment Gateway", "owner": "DevLead",
        "parent_id": _state["initiative_id"],
        "progress_pct": 30,
    })
    assert r.status_code == 201
    _state["task_id"] = r.json()["id"]


async def test_17_get_tree_returns_all_nodes(client: AsyncClient):
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/tree")
    assert r.status_code == 200
    assert r.json()["count"] >= 7


# =========== STATUS PROPAGATION (SyR-STR-00) ===========

async def test_20_update_task_to_red_then_propagate(client: AsyncClient):
    # Update task progress to 20% (RED)
    r = await client.put(f"/api/v1/vstrategy/nodes/{_state['task_id']}", json={"progress_pct": 20})
    assert r.status_code == 200
    assert r.json()["status"] == "RED"

    # Propagate upward
    r2 = await client.post(f"/api/v1/vstrategy/nodes/{_state['task_id']}/propagate")
    assert r2.status_code == 200
    assert r2.json()["propagated_count"] >= 1

    # Verify initiative recalculated
    r3 = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/tree")
    nodes = r3.json()["nodes"]
    p01 = next((n for n in nodes if n["code"] == "P-01"), None)
    assert p01 is not None
    assert p01["status"] == "RED"


# =========== SCORECARD (SyR-STR-04) ===========

async def test_30_scorecard_returns_bsc_perspectives(client: AsyncClient):
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/scorecard")
    assert r.status_code == 200
    data = r.json()
    assert len(data["perspectives"]) >= 1
    assert "overall_status" in data


# =========== S&OP 68/27/5 VALIDATION (SyR-STR-03) ===========

async def test_40_sop_validation_checks_allocation(client: AsyncClient):
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/sop/validate")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["valid"], bool)
    assert isinstance(data["total_budget"], (int, float))
    assert len(data["breakdown"]) == 4
    categories = [row["category"] for row in data["breakdown"]]
    assert "GROW" in categories
    assert "RUN" in categories
    assert "TRANSFORM" in categories
    assert "GIVE" in categories


# =========== PIVOT SIGNALS (SyR-STR-04) ===========

async def test_50_pivot_signal_safe_zone(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals/check", json={
        "rule_code": "RUNWAY_SECURITY",
        "actual_value": 12.5,
        "description": "Monthly check",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["triggered"] is False
    assert data["severity"] == "INFO"
    assert "SAFE ZONE" in data["recommendation"]


async def test_51_pivot_signal_runway_breached_critical(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals/check", json={
        "rule_code": "RUNWAY_SECURITY",
        "actual_value": 4.5,
        "description": "Runway < 6 months!",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["triggered"] is True
    assert data["severity"] == "CRITICAL"
    assert "PIVOT REQUIRED" in data["recommendation"]


async def test_52_pivot_signal_revenue_drop_critical(client: AsyncClient):
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals/check", json={
        "rule_code": "GROWTH_MOMENTUM",
        "actual_value": 22,
        "description": "Revenue drop > 20%",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["triggered"] is True
    assert data["severity"] == "CRITICAL"


async def test_53_get_signals_returns_all(client: AsyncClient):
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals")
    assert r.status_code == 200
    assert r.json()["count"] >= 3


# =========== HEALTH ===========

async def test_99_health_endpoint(client: AsyncClient):
    r = await client.get("/api/v1/vstrategy/health")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "vStrategy"
    assert data["status"] == "UP"
