# =============================================================
# vFinacc — Non-Functional Tests (ISO/IEC 25010:2023)
#
# Coverage mapping:
#   NFR-PERF   → ISO §5.2  Performance Efficiency (time behaviour)
#   NFR-REL    → ISO §5.5  Reliability (availability, faultlessness)
#   NFR-COMPAT → ISO §5.3  Compatibility (interoperability)
#   NFR-SAFE   → ISO §5.9  Safety (operational constraint, fail safe)
#
# @GovernanceID TEST-NFR-ISO-25010-VFINACC
# =============================================================
from __future__ import annotations

import time

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

HEALTH_URL  = "/api/v1/vfinacc/health"
LEDGER_URL  = "/api/v1/vfinacc/ledger"
TXN_URL     = "/api/v1/vfinacc/transactions"

# ════════════════════════════════════════════════════════════════
# Performance Efficiency  (ISO/IEC 25010:2023 §5.2)
# Sub-characteristic: time behaviour
# ════════════════════════════════════════════════════════════════

async def test_perf_01_health_response_time(client: AsyncClient):
    """NFR-PERF-01 — Health endpoint responds in < 200 ms."""
    start = time.perf_counter()
    r = await client.get(HEALTH_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 200, f"Health latency {elapsed_ms:.1f} ms exceeds 200 ms threshold"


async def test_perf_02_list_ledger_entries_response_time(client: AsyncClient):
    """NFR-PERF-02 — GET /ledger responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(LEDGER_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-ledger latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


async def test_perf_03_create_ledger_entry_response_time(client: AsyncClient):
    """NFR-PERF-03 — POST /ledger responds in < 400 ms."""
    start = time.perf_counter()
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-PERF-001",
        "entry_date": "2026-01-01",
        "description": "NFT perf test entry",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 100.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 201
    assert elapsed_ms < 400, f"Create-ledger latency {elapsed_ms:.1f} ms exceeds 400 ms threshold"


async def test_perf_04_list_transactions_response_time(client: AsyncClient):
    """NFR-PERF-04 — GET /transactions responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(TXN_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-transactions latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


# ════════════════════════════════════════════════════════════════
# Reliability  (ISO/IEC 25010:2023 §5.5)
# Sub-characteristics: availability, faultlessness
# ════════════════════════════════════════════════════════════════

async def test_rel_01_health_consistently_up(client: AsyncClient):
    """NFR-REL-01 — Health endpoint returns {status: UP} across 5 calls."""
    for _ in range(5):
        r = await client.get(HEALTH_URL)
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "UP"
        assert data.get("app") == "vFinacc"


async def test_rel_02_malformed_json_returns_4xx(client: AsyncClient):
    """NFR-REL-02 — Malformed JSON body → 4xx (service must not crash with 500)."""
    r = await client.post(
        LEDGER_URL,
        content=b"{ not valid json }",
        headers={"Content-Type": "application/json"},
    )
    assert 400 <= r.status_code <= 499, (
        f"Malformed JSON must yield 4xx, got {r.status_code}"
    )


async def test_rel_03_nonexistent_ledger_entry_returns_404(client: AsyncClient):
    """NFR-REL-03 — Request for non-existent ledger entry ID → 404 (not 500)."""
    r = await client.get(f"{LEDGER_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404, (
        f"Non-existent resource must return 404, got {r.status_code}"
    )


async def test_rel_04_error_response_has_structured_body(client: AsyncClient):
    """NFR-REL-04 — Error responses carry a parseable JSON body with detail/error field."""
    r = await client.get(f"{LEDGER_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    body = r.json()
    assert isinstance(body, dict), "Error response body must be a JSON object"
    has_detail = "detail" in body or "error" in body or "message" in body
    assert has_detail, f"Error body must contain 'detail', 'error', or 'message'. Got: {body}"


async def test_rel_05_posting_unknown_entry_returns_4xx(client: AsyncClient):
    """NFR-REL-05 — POST /ledger/{unknown-id}/post → 4xx (not 500)."""
    r = await client.post(f"{LEDGER_URL}/00000000-0000-0000-0000-000000000000/post")
    assert 400 <= r.status_code <= 499, (
        f"Posting non-existent ledger entry must yield 4xx, got {r.status_code}"
    )


# ════════════════════════════════════════════════════════════════
# Compatibility  (ISO/IEC 25010:2023 §5.3)
# Sub-characteristic: interoperability (media type contract)
# ════════════════════════════════════════════════════════════════

async def test_compat_01_health_content_type_json(client: AsyncClient):
    """NFR-COMPAT-01 — /health response Content-Type includes application/json."""
    r = await client.get(HEALTH_URL)
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_02_list_ledger_content_type_json(client: AsyncClient):
    """NFR-COMPAT-02 — GET /ledger response Content-Type includes application/json."""
    r = await client.get(LEDGER_URL)
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_03_create_ledger_content_type_json(client: AsyncClient):
    """NFR-COMPAT-03 — POST /ledger success response Content-Type includes application/json."""
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-COMPAT-001",
        "entry_date": "2026-01-01",
        "description": "NFT compat test",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 50.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert r.status_code == 201
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_04_error_content_type_json(client: AsyncClient):
    """NFR-COMPAT-04 — Error response Content-Type includes application/json."""
    r = await client.get(f"{LEDGER_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Error response must use JSON, got Content-Type: {ct}"


# ════════════════════════════════════════════════════════════════
# Safety  (ISO/IEC 25010:2023 §5.9)
# Sub-characteristics: operational constraint, fail safe
# ════════════════════════════════════════════════════════════════

async def test_safe_01_missing_required_field_rejected(client: AsyncClient):
    """NFR-SAFE-01 — POST /ledger missing required entry_number → 422 (not 500)."""
    r = await client.post(LEDGER_URL, json={
        # entry_number intentionally omitted — it is required
        "entry_date": "2026-01-01",
        "description": "Missing entry_number",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 100.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert r.status_code == 422, (
        f"Missing required 'entry_number' field must yield 422, got {r.status_code}"
    )


async def test_safe_02_negative_amount_handled(client: AsyncClient):
    """NFR-SAFE-02 — POST /ledger with negative amount → 4xx or accepted; must not cause 500."""
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-SAFE-NEG",
        "entry_date": "2026-01-01",
        "description": "Negative amount test",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": -999.99,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Negative amount must not cause server error (got {r.status_code})"
    )


async def test_safe_03_oversized_description_does_not_crash(client: AsyncClient):
    """NFR-SAFE-03 — POST /ledger with 10 000-char description → must not cause 500."""
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-SAFE-BIG",
        "entry_date": "2026-01-01",
        "description": "D" * 10_000,
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 1.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Oversized description must not cause server error (got {r.status_code})"
    )


async def test_safe_04_invalid_date_format_rejected(client: AsyncClient):
    """NFR-SAFE-04 — POST /ledger with invalid date format → 4xx (not 500)."""
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-SAFE-DATE",
        "entry_date": "NOT-A-DATE",
        "description": "Bad date",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 1.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert 400 <= r.status_code <= 499, (
        f"Invalid date format must yield 4xx, got {r.status_code}"
    )


async def test_safe_05_script_injection_does_not_crash(client: AsyncClient):
    """NFR-SAFE-05 — Script-injection content in description → must not cause 500."""
    r = await client.post(LEDGER_URL, json={
        "entry_number": "JE-NFT-SAFE-XSS",
        "entry_date": "2026-01-01",
        "description": "<script>alert('xss')</script>",
        "debit_account": "6110-Test",
        "credit_account": "2100-Test",
        "amount": 1.00,
        "currency": "USD",
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Script-injection content must not cause server error (got {r.status_code})"
    )
