# =============================================================
# vStrategy — Non-Functional Tests (ISO/IEC 25010:2023)
#
# Coverage mapping:
#   NFR-PERF   → ISO §5.2  Performance Efficiency (time behaviour)
#   NFR-REL    → ISO §5.5  Reliability (availability, faultlessness)
#   NFR-COMPAT → ISO §5.3  Compatibility (interoperability)
#   NFR-SAFE   → ISO §5.9  Safety (operational constraint, fail safe)
#
# @GovernanceID TEST-NFR-ISO-25010-VSTRATEGY
# =============================================================
from __future__ import annotations

import time

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

HEALTH_URL = "/api/v1/vstrategy/health"
PLANS_URL  = "/api/v1/vstrategy/plans"

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


async def test_perf_02_list_plans_response_time(client: AsyncClient):
    """NFR-PERF-02 — GET /plans responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(PLANS_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-plans latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


async def test_perf_03_create_plan_response_time(client: AsyncClient):
    """NFR-PERF-03 — POST /plans responds in < 400 ms."""
    start = time.perf_counter()
    r = await client.post(PLANS_URL, json={
        "period_label": "NFT-PERF-Q1",
        "period_type": "QUARTERLY",
        "created_by": "nft_test",
    })
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 201
    assert elapsed_ms < 400, f"Create-plan latency {elapsed_ms:.1f} ms exceeds 400 ms threshold"


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
        assert data.get("app") == "vStrategy"


async def test_rel_02_malformed_json_returns_4xx(client: AsyncClient):
    """NFR-REL-02 — Malformed JSON body → 4xx (service must not crash with 500)."""
    r = await client.post(
        PLANS_URL,
        content=b"{ invalid :: json !! }",
        headers={"Content-Type": "application/json"},
    )
    assert 400 <= r.status_code <= 499, (
        f"Malformed JSON must yield 4xx, got {r.status_code}"
    )


async def test_rel_03_nonexistent_resource_returns_404(client: AsyncClient):
    """NFR-REL-03 — Request for non-existent plan ID → 404 (not 500)."""
    r = await client.get(f"{PLANS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404, (
        f"Non-existent resource must return 404, got {r.status_code}"
    )


async def test_rel_04_error_response_has_structured_body(client: AsyncClient):
    """NFR-REL-04 — Error responses carry a parseable JSON body with detail/error field."""
    r = await client.get(f"{PLANS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    body = r.json()
    assert isinstance(body, dict), "Error response body must be a JSON object"
    has_detail = "detail" in body or "error" in body or "message" in body
    assert has_detail, f"Error body must contain 'detail', 'error', or 'message'. Got: {body}"


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


async def test_compat_02_list_plans_content_type_json(client: AsyncClient):
    """NFR-COMPAT-02 — GET /plans response Content-Type includes application/json."""
    r = await client.get(PLANS_URL)
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_03_create_plan_content_type_json(client: AsyncClient):
    """NFR-COMPAT-03 — POST /plans success response Content-Type includes application/json."""
    r = await client.post(PLANS_URL, json={
        "period_label": "NFT-COMPAT-Q2",
        "period_type": "QUARTERLY",
        "created_by": "nft_test",
    })
    assert r.status_code == 201
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_04_error_response_content_type_json(client: AsyncClient):
    """NFR-COMPAT-04 — Error responses include application/json Content-Type."""
    r = await client.get(f"{PLANS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Error response must use JSON, got Content-Type: {ct}"


# ════════════════════════════════════════════════════════════════
# Safety  (ISO/IEC 25010:2023 §5.9)
# Sub-characteristics: operational constraint, fail safe
# ════════════════════════════════════════════════════════════════

async def test_safe_01_missing_required_field_rejected(client: AsyncClient):
    """NFR-SAFE-01 — POST /plans without required period_label → 422 (not 500)."""
    r = await client.post(PLANS_URL, json={"period_type": "QUARTERLY"})
    assert r.status_code == 422, (
        f"Missing required field must yield 422 Unprocessable, got {r.status_code}"
    )


async def test_safe_02_empty_string_in_required_field(client: AsyncClient):
    """NFR-SAFE-02 — POST /plans with empty period_label string → 4xx (not 500)."""
    r = await client.post(PLANS_URL, json={"period_label": "", "period_type": "QUARTERLY"})
    assert 400 <= r.status_code <= 499, (
        f"Empty required field must yield 4xx, got {r.status_code}"
    )


async def test_safe_03_oversized_string_field_does_not_crash(client: AsyncClient):
    """NFR-SAFE-03 — POST /plans with 10 000-char period_label → must not cause 500."""
    r = await client.post(PLANS_URL, json={
        "period_label": "X" * 10_000,
        "period_type": "QUARTERLY",
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Oversized string input must not cause server error (got {r.status_code})"
    )


async def test_safe_04_invalid_enum_value_rejected(client: AsyncClient):
    """NFR-SAFE-04 — POST /plans with invalid period_type enum → 4xx (not 500)."""
    r = await client.post(PLANS_URL, json={
        "period_label": "NFT-BAD-ENUM",
        "period_type": "INVALID_TYPE",
        "created_by": "nft_test",
    })
    assert 400 <= r.status_code <= 499, (
        f"Invalid enum value must yield 4xx, got {r.status_code}"
    )


async def test_safe_05_script_injection_content_does_not_crash(client: AsyncClient):
    """NFR-SAFE-05 — Script-injection content in text fields → must not cause 500."""
    r = await client.post(PLANS_URL, json={
        "period_label": "<script>alert('xss')</script>",
        "period_type": "QUARTERLY",
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Script-injection content must not cause server error (got {r.status_code})"
    )
