# =============================================================
# vFinacc — Integration Tests
# Covers SyR-FIN-00 through SyR-FIN-04 (20+ test cases).
# =============================================================
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# Shared state between ordered tests
_state: dict = {}


# =========== LEDGER ENTRIES (SyR-FIN-00) ===========

async def test_01_create_ledger_entry_draft(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/ledger", json={
        "entry_number": "JE-TEST-0001",
        "entry_date": "2026-03-01",
        "description": "AWS Infrastructure Payment",
        "debit_account": "6110-R&D-Infra",
        "credit_account": "2100-Accounts-Payable",
        "amount": 2400.00,
        "currency": "USD",
        "cost_center": "R&D - Infrastructure",
        "created_by": "test",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["entry_number"] == "JE-TEST-0001"
    assert data["status"] == "DRAFT"
    assert float(data["amount"]) == 2400.00
    _state["ledger_id"] = data["id"]


async def test_02_list_ledger_entries(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/ledger")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_03_get_ledger_entry(client: AsyncClient):
    r = await client.get(f"/api/v1/vfinacc/ledger/{_state['ledger_id']}")
    assert r.status_code == 200
    assert r.json()["entry_number"] == "JE-TEST-0001"


async def test_04_update_draft_entry(client: AsyncClient):
    r = await client.put(f"/api/v1/vfinacc/ledger/{_state['ledger_id']}", json={
        "description": "AWS Infrastructure Payment - Updated",
        "amount": 2500.00,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["description"] == "AWS Infrastructure Payment - Updated"
    assert float(data["amount"]) == 2500.00
    assert data["status"] == "DRAFT"


async def test_05_post_ledger_entry(client: AsyncClient):
    r = await client.post(f"/api/v1/vfinacc/ledger/{_state['ledger_id']}/post")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "POSTED"
    assert data["posted_by"] == "system"
    assert data["posted_at"] is not None


async def test_06_cannot_update_posted_entry(client: AsyncClient):
    r = await client.put(f"/api/v1/vfinacc/ledger/{_state['ledger_id']}", json={
        "description": "Should fail",
    })
    assert r.status_code == 400
    assert "DRAFT" in r.json()["detail"]


async def test_07_cannot_post_already_posted(client: AsyncClient):
    r = await client.post(f"/api/v1/vfinacc/ledger/{_state['ledger_id']}/post")
    assert r.status_code == 400
    assert "DRAFT" in r.json()["detail"]


# =========== TRANSACTIONS (SyR-FIN-01) ===========

async def test_10_ingest_transaction(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/transactions", json={
        "source": "BANK_WEBHOOK",
        "amount": 2400.00,
        "currency": "USD",
        "counterparty": "Amazon Web Services",
        "transaction_date": "2026-03-01",
        "description": "AWS monthly invoice",
        "external_id": "BANK-TXN-TEST-001",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["source"] == "BANK_WEBHOOK"
    assert data["status"] == "RAW"
    _state["txn_id"] = data["id"]


async def test_11_list_transactions(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/transactions")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


async def test_12_get_transaction(client: AsyncClient):
    r = await client.get(f"/api/v1/vfinacc/transactions/{_state['txn_id']}")
    assert r.status_code == 200
    assert r.json()["external_id"] == "BANK-TXN-TEST-001"


# =========== RECONCILIATION (SyR-FIN-02) ===========

async def test_20_run_reconciliation_full_match(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/reconciliation/run", json={
        "po_reference": "PO-TEST-001",
        "grn_reference": "GRN-TEST-001",
        "invoice_reference": "INV-TEST-001",
        "po_amount": 2400.00,
        "grn_amount": 2400.00,
        "invoice_amount": 2400.00,
    })
    assert r.status_code == 201
    data = r.json()
    assert data["match_type"] == "FULL_MATCH"
    assert float(data["confidence_pct"]) == 100.00
    assert data["discrepancy_amount"] is None
    _state["recon_full_id"] = data["id"]


async def test_21_run_reconciliation_partial_match(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/reconciliation/run", json={
        "po_reference": "PO-TEST-002",
        "grn_reference": None,
        "invoice_reference": "INV-TEST-002",
        "po_amount": 2400.00,
        "invoice_amount": 2600.00,
    })
    assert r.status_code == 201
    data = r.json()
    assert data["match_type"] == "PARTIAL_MATCH"
    assert float(data["confidence_pct"]) < 100


async def test_22_run_reconciliation_no_match(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/reconciliation/run", json={
        "po_reference": "PO-TEST-003",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["match_type"] == "NO_MATCH"
    assert float(data["confidence_pct"]) == 0


async def test_23_list_reconciliation(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/reconciliation")
    assert r.status_code == 200
    assert r.json()["count"] >= 3


async def test_24_reconciliation_summary(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/reconciliation/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["total_matches"] >= 3
    assert data["full_matches"] >= 1
    assert "auto_match_rate_pct" in data


# =========== COST CENTERS (SyR-FIN-03) ===========

async def test_30_create_cost_allocation_grow(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/cost-centers", json={
        "cost_center_code": "CC-SALES-TEST",
        "cost_center_name": "Sales Team",
        "category": "GROW",
        "budget_amount": 680000.00,
        "actual_amount": 520000.00,
        "currency": "USD",
        "period_label": "Q1-2026",
        "owner": "CMO",
    })
    assert r.status_code == 201
    assert r.json()["category"] == "GROW"
    _state["cost_id"] = r.json()["id"]


async def test_31_create_cost_allocation_run(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/cost-centers", json={
        "cost_center_code": "CC-INFRA-TEST",
        "cost_center_name": "Infrastructure",
        "category": "RUN",
        "budget_amount": 270000.00,
        "actual_amount": 195000.00,
        "currency": "USD",
        "period_label": "Q1-2026",
        "owner": "CAO",
    })
    assert r.status_code == 201


async def test_32_create_cost_allocation_transform_and_give(client: AsyncClient):
    r1 = await client.post("/api/v1/vfinacc/cost-centers", json={
        "cost_center_code": "CC-RND-TEST",
        "cost_center_name": "R&D",
        "category": "TRANSFORM",
        "budget_amount": 50000.00,
        "actual_amount": 32000.00,
        "currency": "USD",
        "period_label": "Q1-2026",
        "owner": "CPO",
    })
    assert r1.status_code == 201

    r2 = await client.post("/api/v1/vfinacc/cost-centers", json={
        "cost_center_code": "CC-CSR-TEST",
        "cost_center_name": "CSR",
        "category": "GIVE",
        "budget_amount": 1000.00,
        "actual_amount": 800.00,
        "currency": "USD",
        "period_label": "Q1-2026",
        "owner": "CEO",
    })
    assert r2.status_code == 201


async def test_33_invalid_category_rejected(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/cost-centers", json={
        "cost_center_code": "CC-BAD",
        "cost_center_name": "Bad Category",
        "category": "INVALID",
        "budget_amount": 100.00,
        "period_label": "Q1-2026",
    })
    assert r.status_code == 400
    assert "Invalid category" in r.json()["detail"]


async def test_34_list_cost_centers(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/cost-centers")
    assert r.status_code == 200
    assert r.json()["count"] >= 4


async def test_35_cost_center_summary(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/cost-centers/summary")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["valid"], bool)
    assert len(data["breakdown"]) == 4
    categories = [row["category"] for row in data["breakdown"]]
    assert "GROW" in categories
    assert "RUN" in categories
    assert "TRANSFORM" in categories
    assert "GIVE" in categories


# =========== COMPLIANCE (SyR-FIN-04) ===========

async def test_40_compliance_check_vat(client: AsyncClient):
    # Create a fresh draft entry for compliance testing
    r1 = await client.post("/api/v1/vfinacc/ledger", json={
        "entry_number": "JE-TEST-COMPL-001",
        "entry_date": "2026-03-10",
        "description": "Domestic service payment",
        "debit_account": "6100-Services",
        "credit_account": "2100-AP",
        "amount": 2400.00,
        "currency": "USD",
    })
    assert r1.status_code == 201
    compl_entry_id = r1.json()["id"]
    _state["compl_entry_id"] = compl_entry_id

    r = await client.post("/api/v1/vfinacc/compliance/check", json={
        "ledger_entry_id": compl_entry_id,
        "check_type": "TAX_VAT",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["result"] == "PASS"
    assert data["tax_applicable"] is True
    assert float(data["tax_rate_pct"]) == 10.00
    assert float(data["tax_amount"]) == 240.00


async def test_41_compliance_check_threshold_pass(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/compliance/check", json={
        "ledger_entry_id": _state["compl_entry_id"],
        "check_type": "THRESHOLD",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["result"] == "PASS"
    assert data["tax_applicable"] is False


async def test_42_compliance_check_threshold_flag(client: AsyncClient):
    # Create a large entry that exceeds threshold
    r1 = await client.post("/api/v1/vfinacc/ledger", json={
        "entry_number": "JE-TEST-COMPL-002",
        "entry_date": "2026-03-10",
        "description": "Large equipment purchase",
        "debit_account": "1500-Equipment",
        "credit_account": "2100-AP",
        "amount": 50000.00,
        "currency": "USD",
    })
    assert r1.status_code == 201
    large_entry_id = r1.json()["id"]

    r = await client.post("/api/v1/vfinacc/compliance/check", json={
        "ledger_entry_id": large_entry_id,
        "check_type": "THRESHOLD",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["result"] == "FLAG"
    assert "exceeds review threshold" in data["notes"]


async def test_43_compliance_check_unknown_type(client: AsyncClient):
    r = await client.post("/api/v1/vfinacc/compliance/check", json={
        "ledger_entry_id": _state["compl_entry_id"],
        "check_type": "UNKNOWN",
    })
    assert r.status_code == 400
    assert "Unknown check_type" in r.json()["detail"]


async def test_44_list_compliance_checks(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/compliance")
    assert r.status_code == 200
    assert r.json()["count"] >= 3


async def test_45_compliance_summary(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/compliance/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["total_checks"] >= 3
    assert data["passed"] >= 2
    assert data["flagged"] >= 1
    assert "pass_rate_pct" in data


# =========== HEALTH ===========

async def test_99_health_endpoint(client: AsyncClient):
    r = await client.get("/api/v1/vfinacc/health")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "vFinacc"
    assert data["status"] == "UP"
