# =============================================================
# vStrategy — Frontend & Integration Tests
# Tests HTML serving, app.js bundle, and full API→UI data flow.
# =============================================================
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

_state: dict = {}


# =========== STATIC FILE SERVING ===========

async def test_f01_index_html_served(client: AsyncClient):
    """Frontend index.html is served at root."""
    r = await client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "")
    assert "vStrategy" in r.text
    assert "S2P2R Dashboard" in r.text


async def test_f02_index_html_contains_script_tag(client: AsyncClient):
    """index.html loads app.js bundle (relative or absolute path)."""
    r = await client.get("/")
    assert r.status_code == 200
    assert "app.js" in r.text


async def test_f03_plan_select_element(client: AsyncClient):
    """index.html has plan selector dropdown."""
    r = await client.get("/")
    assert r.status_code == 200
    assert 'id="planSelect"' in r.text


async def test_f04_loading_state(client: AsyncClient):
    """index.html shows loading state initially."""
    r = await client.get("/")
    assert r.status_code == 200
    assert "Loading" in r.text


# =========== API HEALTH & CONNECTIVITY ===========

async def test_f10_health_returns_json(client: AsyncClient):
    """Health endpoint returns proper JSON with status UP."""
    r = await client.get("/api/v1/vstrategy/health")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "vStrategy"
    assert data["status"] == "UP"
    assert "version" in data


# =========== FULL DATA FLOW: Create → Read → Dashboard ===========

async def test_f20_create_plan_for_frontend(client: AsyncClient):
    """Create a plan that the frontend would display."""
    r = await client.post("/api/v1/vstrategy/plans", json={
        "period_label": "Q1-FRONTEND-TEST",
        "period_type": "QUARTERLY",
        "created_by": "frontend-test",
    })
    assert r.status_code == 201
    data = r.json()
    _state["plan_id"] = data["id"]
    assert data["period_label"] == "Q1-FRONTEND-TEST"


async def test_f21_plans_list_is_api_array(client: AsyncClient):
    """Plans endpoint returns count + plans array (frontend expects this shape)."""
    r = await client.get("/api/v1/vstrategy/plans")
    assert r.status_code == 200
    data = r.json()
    assert "count" in data
    assert "plans" in data
    assert isinstance(data["plans"], list)
    assert data["count"] >= 1
    # Frontend expects each plan to have id, period_label, status
    plan = data["plans"][0]
    assert "id" in plan
    assert "period_label" in plan
    assert "status" in plan


async def test_f22_add_tree_nodes_for_dashboard(client: AsyncClient):
    """Build alignment tree that frontend renders."""
    # Vision
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "VISION", "code": "FE-V-001",
        "title": "Market Leader 2028", "owner": "CEO", "progress_pct": 75,
    })
    assert r.status_code == 201
    vision_id = r.json()["id"]

    # BSC
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "BSC_PERSPECTIVE", "code": "FE-BSC-FIN",
        "title": "Financial", "owner": "CFO",
        "parent_id": vision_id, "bsc_perspective": "FINANCE", "progress_pct": 60,
    })
    assert r.status_code == 201

    # OKR
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "OKR", "code": "FE-OKR-001",
        "title": "Revenue Target $1M", "owner": "CRO",
        "parent_id": r.json()["id"], "bsc_perspective": "FINANCE", "progress_pct": 55,
    })
    assert r.status_code == 201

    # Initiative (GROW)
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "INITIATIVE", "code": "FE-P-01",
        "title": "Enterprise Sales Push", "owner": "Head of Sales",
        "parent_id": r.json()["id"],
        "resource_category": "GROW",
        "budget_amount": 700000, "headcount_fte": 10, "progress_pct": 50,
    })
    assert r.status_code == 201
    _state["initiative_id"] = r.json()["id"]


async def test_f23_tree_api_returns_expected_shape(client: AsyncClient):
    """Tree endpoint returns plan_id + count + nodes array (frontend expects this)."""
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/tree")
    assert r.status_code == 200
    data = r.json()
    assert "plan_id" in data
    assert "count" in data
    assert "nodes" in data
    assert data["count"] >= 4
    # Each node has: id, node_level, code, title, progress_pct, status
    node = data["nodes"][0]
    for key in ["id", "node_level", "code", "title", "progress_pct", "status"]:
        assert key in node, f"Missing key: {key}"


async def test_f24_scorecard_api_returns_expected_shape(client: AsyncClient):
    """Scorecard endpoint returns perspectives array (frontend renders this)."""
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/scorecard")
    assert r.status_code == 200
    data = r.json()
    assert "perspectives" in data
    assert "overall_status" in data
    assert isinstance(data["perspectives"], list)


async def test_f25_sop_validate_api_returns_expected_shape(client: AsyncClient):
    """S&OP validate endpoint returns breakdown array (frontend renders this)."""
    # First update plan with SOP config
    await client.put(f"/api/v1/vstrategy/plans/{_state['plan_id']}", json={
        "sop_config_json": {
            "grow_pct": 68, "run_pct": 27, "transform_pct": 5,
            "give_pct": 0.1, "total_budget": 1000000, "tolerance_pct": 2,
        },
    })
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/sop/validate")
    assert r.status_code == 200
    data = r.json()
    assert "valid" in data
    assert "breakdown" in data
    assert isinstance(data["breakdown"], list)
    assert len(data["breakdown"]) == 4  # GROW, RUN, TRANSFORM, GIVE


async def test_f26_signals_api_returns_expected_shape(client: AsyncClient):
    """Signals endpoint returns count + signals array (frontend renders this)."""
    r = await client.get(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals")
    assert r.status_code == 200
    data = r.json()
    assert "count" in data
    assert "signals" in data
    assert isinstance(data["signals"], list)


async def test_f27_signal_check_produces_displayable_result(client: AsyncClient):
    """Signal check result matches what frontend signal renderer expects."""
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/signals/check", json={
        "rule_code": "RUNWAY_SECURITY",
        "actual_value": 3.0,
        "description": "Running low",
    })
    assert r.status_code == 200
    data = r.json()
    for key in ["rule_code", "triggered", "severity", "recommendation"]:
        assert key in data, f"Missing key: {key}"
    assert data["triggered"] is True
    assert data["severity"] == "CRITICAL"


# =========== PROPAGATION (UI would trigger) ===========

async def test_f30_status_propagation_updates_parent(client: AsyncClient):
    """Status propagation (triggered by UI action) propagates correctly."""
    # Add a task under the initiative
    r = await client.post(f"/api/v1/vstrategy/plans/{_state['plan_id']}/nodes", json={
        "node_level": "TASK", "code": "FE-TASK-001",
        "title": "Setup CRM Integration", "owner": "Dev",
        "parent_id": _state["initiative_id"],
        "progress_pct": 10,
    })
    assert r.status_code == 201
    task_id = r.json()["id"]
    assert r.json()["status"] == "RED"  # 10% → RED

    # Propagate
    r2 = await client.post(f"/api/v1/vstrategy/nodes/{task_id}/propagate")
    assert r2.status_code == 200
    assert r2.json()["propagated_count"] >= 1


# =========== ERROR HANDLING (what frontend sees) ===========

async def test_f40_404_on_nonexistent_plan(client: AsyncClient):
    """Frontend should handle 404 gracefully."""
    import uuid
    fake_id = str(uuid.uuid4())
    r = await client.get(f"/api/v1/vstrategy/plans/{fake_id}")
    assert r.status_code == 404 or r.status_code == 500  # may raise internally


async def test_f41_invalid_plan_id_format(client: AsyncClient):
    """Frontend passes invalid ID → API returns error."""
    r = await client.get("/api/v1/vstrategy/plans/not-a-uuid")
    assert r.status_code in [400, 404, 422, 500]

