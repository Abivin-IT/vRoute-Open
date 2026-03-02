# =============================================================
# vMarketing Org — API Tests  (≥ 25 cases)
# =============================================================
from __future__ import annotations

import pytest

BASE = "/api/v1/vmarketing-org"


# ===== Health ======================================================

@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["app"] == "vmarketing-org"


# ===== Campaigns ===================================================

@pytest.mark.asyncio
async def test_create_campaign(client):
    r = await client.post(f"{BASE}/campaigns", json={
        "campaign_code": "CAMP-T01",
        "name": "Test Campaign Alpha",
        "target_segment": "Enterprise",
        "stage": "AWARENESS",
        "channel": "LinkedIn",
        "budget_amount": "50000",
    })
    assert r.status_code == 201
    assert r.json()["campaign_code"] == "CAMP-T01"
    assert r.json()["status"] == "DRAFT"


@pytest.mark.asyncio
async def test_list_campaigns(client):
    r = await client.get(f"{BASE}/campaigns")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_get_campaign(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T02", "name": "Test Beta"})
    cid = create.json()["id"]
    r = await client.get(f"{BASE}/campaigns/{cid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Test Beta"


@pytest.mark.asyncio
async def test_update_campaign(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T03", "name": "Old Name"})
    cid = create.json()["id"]
    r = await client.patch(f"{BASE}/campaigns/{cid}", json={"name": "New Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_launch_campaign(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T04", "name": "Launch Me"})
    cid = create.json()["id"]
    r = await client.post(f"{BASE}/campaigns/{cid}/launch")
    assert r.status_code == 200
    assert r.json()["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_launch_non_draft_fails(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T05", "name": "Already Active"})
    cid = create.json()["id"]
    await client.post(f"{BASE}/campaigns/{cid}/launch")
    r = await client.post(f"{BASE}/campaigns/{cid}/launch")
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_pause_campaign(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T06", "name": "Pause Me"})
    cid = create.json()["id"]
    await client.post(f"{BASE}/campaigns/{cid}/launch")
    r = await client.post(f"{BASE}/campaigns/{cid}/pause")
    assert r.status_code == 200
    assert r.json()["status"] == "PAUSED"


@pytest.mark.asyncio
async def test_complete_campaign(client):
    create = await client.post(f"{BASE}/campaigns", json={"campaign_code": "CAMP-T07", "name": "Complete Me"})
    cid = create.json()["id"]
    await client.post(f"{BASE}/campaigns/{cid}/launch")
    r = await client.post(f"{BASE}/campaigns/{cid}/complete")
    assert r.status_code == 200
    assert r.json()["status"] == "COMPLETED"


# ===== Tracking Events =============================================

@pytest.mark.asyncio
async def test_ingest_tracking_event(client):
    r = await client.post(f"{BASE}/tracking-events", json={
        "event_code": "EVT-T01",
        "organization": "Acme Corp",
        "action_type": "PAGE_VIEW",
        "page_resource": "/pricing",
        "dwell_seconds": 45,
        "intent_score": 72,
    })
    assert r.status_code == 201
    assert r.json()["action_type"] == "PAGE_VIEW"


@pytest.mark.asyncio
async def test_ingest_invalid_action_type(client):
    r = await client.post(f"{BASE}/tracking-events", json={
        "event_code": "EVT-BAD",
        "organization": "Bad Corp",
        "action_type": "INVALID_TYPE",
    })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_list_tracking_events(client):
    r = await client.get(f"{BASE}/tracking-events")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_tracking_event(client):
    create = await client.post(f"{BASE}/tracking-events", json={
        "event_code": "EVT-T02", "organization": "Test Org", "action_type": "DOWNLOAD_PDF"
    })
    eid = create.json()["id"]
    r = await client.get(f"{BASE}/tracking-events/{eid}")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_intent_summary(client):
    await client.post(f"{BASE}/tracking-events", json={
        "event_code": "EVT-SUM1", "organization": "SumOrg", "action_type": "VIDEO_WATCH", "intent_score": 60
    })
    r = await client.get(f"{BASE}/tracking-events/intent-summary/SumOrg")
    assert r.status_code == 200
    assert r.json()["organization"] == "SumOrg"


# ===== Audience Segments ===========================================

@pytest.mark.asyncio
async def test_create_segment(client):
    r = await client.post(f"{BASE}/segments", json={
        "segment_code": "SEG-T01", "name": "Test Segment", "tier": "TIER_1", "account_count": 50
    })
    assert r.status_code == 201
    assert r.json()["tier"] == "TIER_1"


@pytest.mark.asyncio
async def test_list_segments(client):
    r = await client.get(f"{BASE}/segments")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_archive_segment(client):
    create = await client.post(f"{BASE}/segments", json={"segment_code": "SEG-T02", "name": "Archive Me"})
    sid = create.json()["id"]
    r = await client.post(f"{BASE}/segments/{sid}/archive")
    assert r.status_code == 200
    assert r.json()["status"] == "ARCHIVED"


# ===== Content Assets ==============================================

@pytest.mark.asyncio
async def test_create_asset(client):
    r = await client.post(f"{BASE}/assets", json={
        "asset_code": "AST-T01", "title": "Test Whitepaper", "asset_type": "WHITEPAPER"
    })
    assert r.status_code == 201
    assert r.json()["asset_type"] == "WHITEPAPER"


@pytest.mark.asyncio
async def test_create_asset_invalid_type(client):
    r = await client.post(f"{BASE}/assets", json={
        "asset_code": "AST-BAD", "title": "Bad Type", "asset_type": "PODCAST"
    })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_publish_asset(client):
    create = await client.post(f"{BASE}/assets", json={
        "asset_code": "AST-T02", "title": "Publish Me", "asset_type": "CASE_STUDY"
    })
    aid = create.json()["id"]
    r = await client.post(f"{BASE}/assets/{aid}/publish")
    assert r.status_code == 200
    assert r.json()["status"] == "PUBLISHED"


@pytest.mark.asyncio
async def test_archive_asset(client):
    create = await client.post(f"{BASE}/assets", json={
        "asset_code": "AST-T03", "title": "Archive Me", "asset_type": "VIDEO"
    })
    aid = create.json()["id"]
    r = await client.post(f"{BASE}/assets/{aid}/archive")
    assert r.status_code == 200
    assert r.json()["status"] == "ARCHIVED"


# ===== Lead Scores =================================================

@pytest.mark.asyncio
async def test_upsert_lead(client):
    r = await client.post(f"{BASE}/leads", json={
        "organization": "Hot Corp", "contact_name": "Jane Doe", "score": 85
    })
    assert r.status_code == 201
    assert r.json()["grade"] == "HOT"


@pytest.mark.asyncio
async def test_lead_grade_warm(client):
    r = await client.post(f"{BASE}/leads", json={"organization": "Warm Inc", "score": 55})
    assert r.json()["grade"] == "WARM"


@pytest.mark.asyncio
async def test_lead_grade_cold(client):
    r = await client.post(f"{BASE}/leads", json={"organization": "Cold LLC", "score": 20})
    assert r.json()["grade"] == "COLD"


@pytest.mark.asyncio
async def test_qualify_lead(client):
    create = await client.post(f"{BASE}/leads", json={"organization": "Qualify Me", "score": 70})
    lid = create.json()["id"]
    r = await client.post(f"{BASE}/leads/{lid}/qualify")
    assert r.status_code == 200
    assert r.json()["status"] == "QUALIFIED"


@pytest.mark.asyncio
async def test_handoff_lead(client):
    create = await client.post(f"{BASE}/leads", json={"organization": "Handoff Me", "score": 80})
    lid = create.json()["id"]
    await client.post(f"{BASE}/leads/{lid}/qualify")
    r = await client.post(f"{BASE}/leads/{lid}/handoff", params={"handed_off_to": "sales-team-1"})
    assert r.status_code == 200
    assert r.json()["status"] == "HANDED_OFF"
    assert r.json()["handed_off_to"] == "sales-team-1"


@pytest.mark.asyncio
async def test_disqualify_lead(client):
    create = await client.post(f"{BASE}/leads", json={"organization": "DQ Corp", "score": 10})
    lid = create.json()["id"]
    r = await client.post(f"{BASE}/leads/{lid}/disqualify")
    assert r.status_code == 200
    assert r.json()["status"] == "DISQUALIFIED"


@pytest.mark.asyncio
async def test_list_leads_by_grade(client):
    r = await client.get(f"{BASE}/leads", params={"grade": "HOT"})
    assert r.status_code == 200
    for lead in r.json():
        assert lead["grade"] == "HOT"
