# vMarketing Org · M2L ABM Engine

> **GovernanceID:** `vmarketing-org.0.5`
> **Port:** `8084` · **gRPC:** `9090`

## Overview

Account-Based Marketing engine for the vRoute platform — campaigns,
tracking pixels, audience segments, content assets, AI lead scoring & sales handoff.

## Domain Models

| Model | Table | FSM States |
|-------|-------|------------|
| Campaign | `campaigns` | DRAFT → ACTIVE → PAUSED → COMPLETED |
| TrackingEvent | `tracking_events` | (append-only) |
| AudienceSegment | `audience_segments` | ACTIVE → ARCHIVED |
| ContentAsset | `content_assets` | DRAFT → PUBLISHED → ARCHIVED |
| LeadScore | `lead_scores` | NEW → QUALIFIED → HANDED_OFF / DISQUALIFIED |

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Health check |
| GET | `/api/v1/vmarketing-org/campaigns` | List campaigns |
| POST | `/api/v1/vmarketing-org/campaigns` | Create campaign |
| GET | `/api/v1/vmarketing-org/campaigns/{id}` | Get campaign |
| PATCH | `/api/v1/vmarketing-org/campaigns/{id}` | Update campaign |
| POST | `/api/v1/vmarketing-org/campaigns/{id}/launch` | Launch (DRAFT→ACTIVE) |
| POST | `/api/v1/vmarketing-org/campaigns/{id}/pause` | Pause (ACTIVE→PAUSED) |
| POST | `/api/v1/vmarketing-org/campaigns/{id}/complete` | Complete campaign |
| GET | `/api/v1/vmarketing-org/tracking-events` | List events |
| POST | `/api/v1/vmarketing-org/tracking-events` | Ingest event |
| GET | `/api/v1/vmarketing-org/tracking-events/{id}` | Get event |
| GET | `/api/v1/vmarketing-org/tracking-events/intent-summary/{org}` | Intent aggregation |
| GET | `/api/v1/vmarketing-org/segments` | List segments |
| POST | `/api/v1/vmarketing-org/segments` | Create segment |
| GET | `/api/v1/vmarketing-org/segments/{id}` | Get segment |
| POST | `/api/v1/vmarketing-org/segments/{id}/archive` | Archive segment |
| GET | `/api/v1/vmarketing-org/assets` | List content assets |
| POST | `/api/v1/vmarketing-org/assets` | Create asset |
| GET | `/api/v1/vmarketing-org/assets/{id}` | Get asset |
| POST | `/api/v1/vmarketing-org/assets/{id}/publish` | Publish (DRAFT→PUBLISHED) |
| POST | `/api/v1/vmarketing-org/assets/{id}/archive` | Archive asset |
| GET | `/api/v1/vmarketing-org/leads` | List leads |
| POST | `/api/v1/vmarketing-org/leads` | Score / upsert lead |
| GET | `/api/v1/vmarketing-org/leads/{id}` | Get lead |
| POST | `/api/v1/vmarketing-org/leads/{id}/qualify` | Qualify (NEW→QUALIFIED) |
| POST | `/api/v1/vmarketing-org/leads/{id}/handoff` | Hand off to sales |
| POST | `/api/v1/vmarketing-org/leads/{id}/disqualify` | Disqualify lead |

## Tech Stack

- Python 3.12 · FastAPI · SQLAlchemy 2 (async) · PostgreSQL 16 · Redis 7
- gRPC client → vKernel:9090
- Alembic migrations (version table: `alembic_version_vmarketing_org`)

## Running

```bash
cd 05-vmarketing-org
pip install -r requirements.txt
uvicorn app.main:app --port 8084
```

## Tests

```bash
cd 05-vmarketing-org
pytest -v
```

## Integration Points

- **vKernel:** gRPC events (campaign.launched, lead.qualified, lead.handed_off)
- **vStrategy:** Subscribes to `strategy.kpi.updated` for campaign alignment
- **vFinAcc:** Budget tracking events may feed into finance module
- **vDesign Physical:** Content assets may reference physical design specs

## Cross-references

- PRD: `00-design/vmarketing-org-prd.md`
- Gateway routes: `01-vkernel/src/main/resources/application.yml`
- Flyway: `01-vkernel/.../V10__register_vmarketing_org.sql`
