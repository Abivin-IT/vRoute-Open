# =============================================================
# vMarketing Org — Non-Functional Tests (ISO/IEC 25010:2023)
#
# Coverage mapping:
#   NFR-PERF   → ISO §5.2  Performance Efficiency (time behaviour)
#   NFR-REL    → ISO §5.5  Reliability (availability, faultlessness)
#   NFR-COMPAT → ISO §5.3  Compatibility (interoperability)
#   NFR-SAFE   → ISO §5.9  Safety (operational constraint, fail safe)
#
# @GovernanceID TEST-NFR-ISO-25010-VMARKETING-ORG
# =============================================================
from __future__ import annotations

import time

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

HEALTH_URL    = "/health"
CAMPAIGNS_URL = "/api/v1/vmarketing-org/campaigns"
EVENTS_URL    = "/api/v1/vmarketing-org/tracking-events"
SEGMENTS_URL  = "/api/v1/vmarketing-org/segments"
ASSETS_URL    = "/api/v1/vmarketing-org/assets"

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


async def test_perf_02_list_campaigns_response_time(client: AsyncClient):
    """NFR-PERF-02 — GET /campaigns responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(CAMPAIGNS_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-campaigns latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


async def test_perf_03_create_campaign_response_time(client: AsyncClient):
    """NFR-PERF-03 — POST /campaigns responds in < 400 ms."""
    start = time.perf_counter()
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-PERF-01",
        "name": "NFT Perf Campaign",
        "stage": "AWARENESS",
    })
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 201
    assert elapsed_ms < 400, f"Create-campaign latency {elapsed_ms:.1f} ms exceeds 400 ms threshold"


async def test_perf_04_list_tracking_events_response_time(client: AsyncClient):
    """NFR-PERF-04 — GET /tracking-events responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(EVENTS_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-events latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


# ════════════════════════════════════════════════════════════════
# Reliability  (ISO/IEC 25010:2023 §5.5)
# Sub-characteristics: availability, faultlessness
# ════════════════════════════════════════════════════════════════

async def test_rel_01_health_consistently_up(client: AsyncClient):
    """NFR-REL-01 — Health endpoint returns {app, status:UP/ok} across 5 calls."""
    for _ in range(5):
        r = await client.get(HEALTH_URL)
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") in ("UP", "ok")
        assert data.get("app") == "vmarketing-org"


async def test_rel_02_malformed_json_returns_4xx(client: AsyncClient):
    """NFR-REL-02 — Malformed JSON body → 4xx (service must not crash with 500)."""
    r = await client.post(
        CAMPAIGNS_URL,
        content=b"{ bad json !! }",
        headers={"Content-Type": "application/json"},
    )
    assert 400 <= r.status_code <= 499, (
        f"Malformed JSON must yield 4xx, got {r.status_code}"
    )


async def test_rel_03_nonexistent_campaign_returns_404(client: AsyncClient):
    """NFR-REL-03 — GET /campaigns/{unknown} → 404 (not 500)."""
    r = await client.get(f"{CAMPAIGNS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404, (
        f"Non-existent campaign must return 404, got {r.status_code}"
    )


async def test_rel_04_error_response_has_structured_body(client: AsyncClient):
    """NFR-REL-04 — Error responses carry a parseable JSON body."""
    r = await client.get(f"{CAMPAIGNS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    body = r.json()
    assert isinstance(body, dict), "Error response body must be a JSON object"
    has_detail = "detail" in body or "error" in body or "message" in body
    assert has_detail, f"Error body must contain 'detail', 'error', or 'message'. Got: {body}"


async def test_rel_05_double_launch_is_rejected(client: AsyncClient):
    """NFR-REL-05 — Launching an already-active campaign → 409 (idempotency guard)."""
    create = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-REL-IDEM",
        "name": "Idempotency Test Campaign",
    })
    assert create.status_code == 201
    cid = create.json()["id"]

    await client.post(f"{CAMPAIGNS_URL}/{cid}/launch")
    r = await client.post(f"{CAMPAIGNS_URL}/{cid}/launch")
    assert r.status_code == 409, (
        f"Double-launch must yield 409 Conflict, got {r.status_code}"
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


async def test_compat_02_list_campaigns_content_type_json(client: AsyncClient):
    """NFR-COMPAT-02 — GET /campaigns response Content-Type includes application/json."""
    r = await client.get(CAMPAIGNS_URL)
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_03_create_campaign_content_type_json(client: AsyncClient):
    """NFR-COMPAT-03 — POST /campaigns success response Content-Type includes application/json."""
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-COMPAT-01",
        "name": "NFT Compat Campaign",
    })
    assert r.status_code == 201
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_04_error_content_type_json(client: AsyncClient):
    """NFR-COMPAT-04 — Error response Content-Type includes application/json."""
    r = await client.get(f"{CAMPAIGNS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Error response must use JSON, got Content-Type: {ct}"


# ════════════════════════════════════════════════════════════════
# Safety  (ISO/IEC 25010:2023 §5.9)
# Sub-characteristics: operational constraint, fail safe
# ════════════════════════════════════════════════════════════════

async def test_safe_01_missing_required_campaign_code_rejected(client: AsyncClient):
    """NFR-SAFE-01 — POST /campaigns without required campaign_code → 422 (not 500)."""
    r = await client.post(CAMPAIGNS_URL, json={"name": "No Code Campaign"})
    assert r.status_code == 422, (
        f"Missing required 'campaign_code' must yield 422, got {r.status_code}"
    )


async def test_safe_02_invalid_action_type_on_tracking_event_rejected(client: AsyncClient):
    """NFR-SAFE-02 — POST /tracking-events with invalid action_type → 422 (not 500)."""
    r = await client.post(EVENTS_URL, json={
        "event_code": "EVT-NFT-SAFE-01",
        "organization": "Test Org",
        "action_type": "COMPLETELY_INVALID_ACTION",
    })
    assert r.status_code == 422, (
        f"Invalid action_type must yield 422, got {r.status_code}"
    )


async def test_safe_03_oversized_campaign_name_does_not_crash(client: AsyncClient):
    """NFR-SAFE-03 — POST /campaigns with 10 000-char name → must not cause 500."""
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-SAFE-BIG",
        "name": "N" * 10_000,
    })
    assert r.status_code != 500, (
        f"Oversized campaign name must not cause server error (got {r.status_code})"
    )


async def test_safe_04_negative_budget_rejected_or_accepted(client: AsyncClient):
    """NFR-SAFE-04 — POST /campaigns with negative budget → must not cause 500."""
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-SAFE-NEG",
        "name": "Negative Budget",
        "budget_amount": "-999999",
    })
    assert r.status_code != 500, (
        f"Negative budget amount must not cause server error (got {r.status_code})"
    )


async def test_safe_05_script_injection_does_not_crash(client: AsyncClient):
    """NFR-SAFE-05 — Script-injection content in name field → must not cause 500."""
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-SAFE-XSS",
        "name": "<script>alert('xss')</script>",
    })
    assert r.status_code != 500, (
        f"Script-injection content must not cause server error (got {r.status_code})"
    )


async def test_safe_06_sql_injection_content_does_not_crash(client: AsyncClient):
    """NFR-SAFE-06 — SQL-injection-like content in fields → must not cause 500."""
    r = await client.post(CAMPAIGNS_URL, json={
        "campaign_code": "CAMP-NFT-SAFE-SQL",
        "name": "'; DROP TABLE campaigns; --",
    })
    assert r.status_code != 500, (
        f"SQL-injection-like content must not cause server error (got {r.status_code})"
    )
