# =============================================================
# vDesign Physical — Non-Functional Tests (ISO/IEC 25010:2023)
#
# Coverage mapping:
#   NFR-PERF   → ISO §5.2  Performance Efficiency (time behaviour)
#   NFR-REL    → ISO §5.5  Reliability (availability, faultlessness)
#   NFR-COMPAT → ISO §5.3  Compatibility (interoperability)
#   NFR-SAFE   → ISO §5.9  Safety (operational constraint, fail safe)
#
# @GovernanceID TEST-NFR-ISO-25010-VDESIGN-PHYSICAL
# =============================================================
from __future__ import annotations

import time

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

HEALTH_URL   = "/api/v1/vdesign-physical/health"
SAMPLES_URL  = "/api/v1/vdesign-physical/golden-samples"
MATERIALS_URL = "/api/v1/vdesign-physical/materials"
PROTOS_URL   = "/api/v1/vdesign-physical/prototypes"

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


async def test_perf_02_list_samples_response_time(client: AsyncClient):
    """NFR-PERF-02 — GET /golden-samples responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(SAMPLES_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-samples latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


async def test_perf_03_create_sample_response_time(client: AsyncClient):
    """NFR-PERF-03 — POST /golden-samples responds in < 400 ms."""
    start = time.perf_counter()
    r = await client.post(SAMPLES_URL, json={
        "sample_code": "GS-NFT-PERF-001",
        "product_name": "NFT Perf Sample",
        "material": "Ti-6Al-4V",
        "convergence_pct": 99.0,
        "created_by": "nft_test",
    })
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 201
    assert elapsed_ms < 400, f"Create-sample latency {elapsed_ms:.1f} ms exceeds 400 ms threshold"


async def test_perf_04_list_materials_response_time(client: AsyncClient):
    """NFR-PERF-04 — GET /materials responds in < 300 ms."""
    start = time.perf_counter()
    r = await client.get(MATERIALS_URL)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert r.status_code == 200
    assert elapsed_ms < 300, f"List-materials latency {elapsed_ms:.1f} ms exceeds 300 ms threshold"


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
        assert data.get("app") == "vDesign Physical"


async def test_rel_02_malformed_json_returns_4xx(client: AsyncClient):
    """NFR-REL-02 — Malformed JSON body → 4xx (service must not crash with 500)."""
    r = await client.post(
        SAMPLES_URL,
        content=b"{ bad json !! }",
        headers={"Content-Type": "application/json"},
    )
    assert 400 <= r.status_code <= 499, (
        f"Malformed JSON must yield 4xx, got {r.status_code}"
    )


async def test_rel_03_nonexistent_sample_returns_404(client: AsyncClient):
    """NFR-REL-03 — Request for non-existent golden sample ID → 404 (not 500)."""
    r = await client.get(f"{SAMPLES_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404, (
        f"Non-existent resource must return 404, got {r.status_code}"
    )


async def test_rel_04_error_response_has_structured_body(client: AsyncClient):
    """NFR-REL-04 — Error responses carry a parseable JSON body."""
    r = await client.get(f"{SAMPLES_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    body = r.json()
    assert isinstance(body, dict), "Error response body must be a JSON object"
    has_detail = "detail" in body or "error" in body or "message" in body
    assert has_detail, f"Error body must contain 'detail', 'error', or 'message'. Got: {body}"


async def test_rel_05_nonexistent_material_returns_404(client: AsyncClient):
    """NFR-REL-05 — Request for non-existent material ID → 404 (not 500)."""
    r = await client.get(f"{MATERIALS_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404, (
        f"Non-existent material must return 404, got {r.status_code}"
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


async def test_compat_02_list_samples_content_type_json(client: AsyncClient):
    """NFR-COMPAT-02 — GET /golden-samples response Content-Type includes application/json."""
    r = await client.get(SAMPLES_URL)
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_03_create_sample_content_type_json(client: AsyncClient):
    """NFR-COMPAT-03 — POST /golden-samples success response Content-Type includes application/json."""
    r = await client.post(SAMPLES_URL, json={
        "sample_code": "GS-NFT-COMPAT-001",
        "product_name": "NFT Compat Sample",
        "material": "Steel 316L",
        "convergence_pct": 97.0,
        "created_by": "nft_test",
    })
    assert r.status_code == 201
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Expected application/json Content-Type, got: {ct}"


async def test_compat_04_error_content_type_json(client: AsyncClient):
    """NFR-COMPAT-04 — Error response Content-Type includes application/json."""
    r = await client.get(f"{SAMPLES_URL}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    ct = r.headers.get("content-type", "")
    assert "application/json" in ct, f"Error response must use JSON, got Content-Type: {ct}"


# ════════════════════════════════════════════════════════════════
# Safety  (ISO/IEC 25010:2023 §5.9)
# Sub-characteristics: operational constraint, fail safe
# ════════════════════════════════════════════════════════════════

async def test_safe_01_missing_required_field_rejected(client: AsyncClient):
    """NFR-SAFE-01 — POST /golden-samples missing required sample_code → 422 (not 500)."""
    r = await client.post(SAMPLES_URL, json={
        "product_name": "Missing code sample",
        "material": "Ti-6Al-4V",
        "convergence_pct": 99.0,
        "created_by": "nft_test",
    })
    assert r.status_code == 422, (
        f"Missing required 'sample_code' must yield 422, got {r.status_code}"
    )


async def test_safe_02_invalid_source_type_on_material_rejected(client: AsyncClient):
    """NFR-SAFE-02 — POST /materials with invalid source_type → 4xx (not 500)."""
    r = await client.post(MATERIALS_URL, json={
        "item_code": "RAW-NFT-SAFE-001",
        "source_type": "COMPLETELY_INVALID",
        "description": "Invalid source type test",
    })
    assert 400 <= r.status_code <= 499, (
        f"Invalid source_type must yield 4xx, got {r.status_code}"
    )


async def test_safe_03_oversized_product_name_does_not_crash(client: AsyncClient):
    """NFR-SAFE-03 — POST /golden-samples with 10 000-char product_name → must not cause 500."""
    r = await client.post(SAMPLES_URL, json={
        "sample_code": "GS-NFT-SAFE-BIG",
        "product_name": "P" * 10_000,
        "material": "Ti-6Al-4V",
        "convergence_pct": 99.0,
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Oversized product_name must not cause server error (got {r.status_code})"
    )


async def test_safe_04_malformed_convergence_pct_rejected(client: AsyncClient):
    """NFR-SAFE-04 — POST /golden-samples with non-numeric convergence_pct → 4xx (not 500)."""
    r = await client.post(SAMPLES_URL, json={
        "sample_code": "GS-NFT-SAFE-TYPE",
        "product_name": "Bad type test",
        "material": "Ti-6Al-4V",
        "convergence_pct": "NOT_A_NUMBER",
        "created_by": "nft_test",
    })
    assert 400 <= r.status_code <= 499, (
        f"Non-numeric convergence_pct must yield 4xx, got {r.status_code}"
    )


async def test_safe_05_script_injection_does_not_crash(client: AsyncClient):
    """NFR-SAFE-05 — Script-injection content in text fields → must not cause 500."""
    r = await client.post(SAMPLES_URL, json={
        "sample_code": "GS-NFT-SAFE-XSS",
        "product_name": "<script>alert('xss')</script>",
        "material": "Ti-6Al-4V",
        "convergence_pct": 99.0,
        "created_by": "nft_test",
    })
    assert r.status_code != 500, (
        f"Script-injection content must not cause server error (got {r.status_code})"
    )


async def test_safe_06_compromise_nonexistent_sample_returns_4xx(client: AsyncClient):
    """NFR-SAFE-06 — POST /golden-samples/{unknown}/compromise → 4xx (not 500)."""
    r = await client.post(
        f"{SAMPLES_URL}/00000000-0000-0000-0000-000000000000/compromise"
    )
    assert 400 <= r.status_code <= 499, (
        f"Compromising non-existent sample must yield 4xx, got {r.status_code}"
    )
