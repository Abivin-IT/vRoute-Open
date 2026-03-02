# =============================================================
# vDesign Physical — Integration Tests
# Covers SyR-PHY-00 through SyR-PHY-04 (25+ test cases).
# =============================================================
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# Shared state between ordered tests
_state: dict = {}


# =========== GOLDEN SAMPLES (SyR-PHY-00) ===========

async def test_01_create_golden_sample(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/golden-samples", json={
        "sample_code": "GS-TEST-001",
        "product_name": "Test Watch Case",
        "material": "Ti-6Al-4V",
        "weight_actual": 152.05,
        "weight_spec": 152.00,
        "dimension_x_mm": 44.02,
        "convergence_pct": 98.5,
        "storage_zone": "Vault A",
        "storage_shelf": "Shelf-04",
        "custodian": "test_user",
        "seal_tag_id": "TAG-TEST-001",
        "linked_spec_id": "SPC-DIG-V1.0",
        "created_by": "test",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["sample_code"] == "GS-TEST-001"
    assert data["status"] == "SEALED"
    assert float(data["convergence_pct"]) == 98.5
    _state["sample_id"] = data["id"]


async def test_02_list_golden_samples(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/golden-samples")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_03_get_golden_sample(client: AsyncClient):
    r = await client.get(f"/api/v1/vdesign-physical/golden-samples/{_state['sample_id']}")
    assert r.status_code == 200
    assert r.json()["sample_code"] == "GS-TEST-001"


async def test_04_create_active_sample_and_update(client: AsyncClient):
    """Create an ACTIVE sample to test update and seal."""
    r = await client.post("/api/v1/vdesign-physical/golden-samples", json={
        "sample_code": "GS-TEST-002",
        "product_name": "Test Speaker Housing",
        "material": "Aluminum 6061",
        "convergence_pct": 95.0,
        "created_by": "test",
    })
    assert r.status_code == 201
    _state["active_sample_id"] = r.json()["id"]

    # Update it
    r2 = await client.put(f"/api/v1/vdesign-physical/golden-samples/{_state['active_sample_id']}", json={
        "convergence_pct": 99.0,
        "notes": "Updated after CMM re-scan",
    })
    assert r2.status_code == 200
    assert float(r2.json()["convergence_pct"]) == 99.0


async def test_05_compromise_sample(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/golden-samples/{_state['sample_id']}/compromise")
    assert r.status_code == 200
    assert r.json()["status"] == "COMPROMISED"


async def test_06_cannot_update_compromised(client: AsyncClient):
    r = await client.put(f"/api/v1/vdesign-physical/golden-samples/{_state['sample_id']}", json={
        "notes": "Should fail",
    })
    assert r.status_code == 400
    assert "COMPROMISED" in r.json()["detail"]


async def test_07_cannot_compromise_again(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/golden-samples/{_state['sample_id']}/compromise")
    assert r.status_code == 400


# =========== MATERIAL INBOX (SyR-PHY-01) ===========

async def test_10_ingest_material(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/materials", json={
        "item_code": "RAW-TEST-001",
        "source_type": "SUPPLIER",
        "supplier_name": "Toray Industries",
        "description": "Carbon Fiber Sheet 2mm",
        "material_type": "Carbon Fiber",
        "initial_assessment": "Weave: 3K Twill",
        "received_by": "lab_tech_01",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["source_type"] == "SUPPLIER"
    assert data["status"] == "PENDING"
    _state["material_id"] = data["id"]


async def test_11_invalid_source_type(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/materials", json={
        "item_code": "RAW-BAD-001",
        "source_type": "INVALID",
        "description": "Bad source",
    })
    assert r.status_code == 400
    assert "Invalid source_type" in r.json()["detail"]


async def test_12_list_materials(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/materials")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_13_get_material(client: AsyncClient):
    r = await client.get(f"/api/v1/vdesign-physical/materials/{_state['material_id']}")
    assert r.status_code == 200
    assert r.json()["item_code"] == "RAW-TEST-001"


async def test_14_scrap_material(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/materials/{_state['material_id']}/scrap")
    assert r.status_code == 200
    assert r.json()["status"] == "SCRAPPED"


async def test_15_cannot_scrap_again(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/materials/{_state['material_id']}/scrap")
    assert r.status_code == 400


# =========== PROTOTYPES (SyR-PHY-02) ===========

async def test_20_create_prototype(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/prototypes", json={
        "proto_code": "PROTO-TEST-001",
        "product_name": "VK-Watch",
        "version_label": "V1",
        "fabrication_method": "3D_PRINT",
        "rfid_tag_id": "RFID-TEST-001",
        "location": "Lab Room 3A",
        "created_by": "test",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "ACTIVE"
    assert data["version_label"] == "V1"
    _state["proto_id"] = data["id"]


async def test_21_list_prototypes(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/prototypes")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_22_get_prototype(client: AsyncClient):
    r = await client.get(f"/api/v1/vdesign-physical/prototypes/{_state['proto_id']}")
    assert r.status_code == 200
    assert r.json()["proto_code"] == "PROTO-TEST-001"


async def test_23_retire_prototype(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/prototypes/{_state['proto_id']}/retire")
    assert r.status_code == 200
    assert r.json()["status"] == "OBSOLETE"


async def test_24_cannot_retire_again(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/prototypes/{_state['proto_id']}/retire")
    assert r.status_code == 400


# =========== LAB TESTS (SyR-PHY-03) ===========

async def test_30_create_lab_test(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/lab-tests", json={
        "test_code": "LT-TEST-001",
        "test_type": "STRESS",
        "measured_value": "450 MPa",
        "threshold_value": ">400 MPa",
        "notes": "Tensile test on titanium sample",
        "tested_by": "lab_eng_01",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["result"] == "RUNNING"
    assert data["test_type"] == "STRESS"
    _state["test_id"] = data["id"]


async def test_31_invalid_test_type(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/lab-tests", json={
        "test_code": "LT-BAD-001",
        "test_type": "UNKNOWN",
    })
    assert r.status_code == 400
    assert "Invalid test_type" in r.json()["detail"]


async def test_32_list_lab_tests(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/lab-tests")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_33_get_lab_test(client: AsyncClient):
    r = await client.get(f"/api/v1/vdesign-physical/lab-tests/{_state['test_id']}")
    assert r.status_code == 200
    assert r.json()["test_code"] == "LT-TEST-001"


async def test_34_complete_lab_test_passed(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/lab-tests/{_state['test_id']}/complete?result=PASSED")
    assert r.status_code == 200
    assert r.json()["result"] == "PASSED"


async def test_35_cannot_complete_again(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/lab-tests/{_state['test_id']}/complete?result=FAILED")
    assert r.status_code == 400
    assert "already completed" in r.json()["detail"]


async def test_36_complete_with_invalid_result(client: AsyncClient):
    # Create another test to test invalid result
    r1 = await client.post("/api/v1/vdesign-physical/lab-tests", json={
        "test_code": "LT-TEST-002",
        "test_type": "DROP",
        "tested_by": "lab_eng_02",
    })
    assert r1.status_code == 201
    test_id = r1.json()["id"]

    r = await client.post(f"/api/v1/vdesign-physical/lab-tests/{test_id}/complete?result=BAD")
    assert r.status_code == 400
    assert "Invalid result" in r.json()["detail"]


async def test_37_lab_test_summary(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/lab-tests/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["total_tests"] >= 2
    assert data["passed"] >= 1
    assert "pass_rate_pct" in data


# =========== HANDOVER KITS (SyR-PHY-04) ===========

async def test_40_create_handover_kit(client: AsyncClient):
    r = await client.post("/api/v1/vdesign-physical/handover-kits", json={
        "kit_code": "HK-TEST-001",
        "product_name": "VK-Watch Production Kit",
        "contents_summary": "1x Mold, 2x Jig, 1x Color Card",
        "destination": "Factory Binh Duong",
        "packed_by": "logistics_01",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "PACKING"
    _state["kit_id"] = data["id"]


async def test_41_list_handover_kits(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/handover-kits")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_42_get_handover_kit(client: AsyncClient):
    r = await client.get(f"/api/v1/vdesign-physical/handover-kits/{_state['kit_id']}")
    assert r.status_code == 200
    assert r.json()["kit_code"] == "HK-TEST-001"


async def test_43_advance_packing_to_ready(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/handover-kits/{_state['kit_id']}/advance")
    assert r.status_code == 200
    assert r.json()["status"] == "READY"


async def test_44_advance_ready_to_dispatched(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/handover-kits/{_state['kit_id']}/advance")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "DISPATCHED"
    assert data["dispatched_at"] is not None


async def test_45_cannot_advance_dispatched(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/handover-kits/{_state['kit_id']}/advance")
    assert r.status_code == 400


async def test_46_receive_dispatched_kit(client: AsyncClient):
    r = await client.post(f"/api/v1/vdesign-physical/handover-kits/{_state['kit_id']}/receive")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "RECEIVED"
    assert data["received_at"] is not None


async def test_47_cannot_receive_non_dispatched(client: AsyncClient):
    # Create a new kit that is still PACKING
    r1 = await client.post("/api/v1/vdesign-physical/handover-kits", json={
        "kit_code": "HK-TEST-002",
        "product_name": "Another Kit",
        "contents_summary": "Various items",
    })
    assert r1.status_code == 201
    kit_id = r1.json()["id"]

    r = await client.post(f"/api/v1/vdesign-physical/handover-kits/{kit_id}/receive")
    assert r.status_code == 400
    assert "DISPATCHED" in r.json()["detail"]


# =========== HEALTH ===========

async def test_99_health_endpoint(client: AsyncClient):
    r = await client.get("/api/v1/vdesign-physical/health")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "vDesign Physical"
    assert data["status"] == "UP"
