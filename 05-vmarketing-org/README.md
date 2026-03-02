# vMarketing Org · M2L ABM Engine

> **GovernanceID:** `vmarketing-org.0.5`
> **Port:** `8084` · **gRPC:** `9090`

## Overview

Account-Based Marketing engine for the vRoute platform — campaigns,
tracking pixels, audience segments, content assets, AI lead scoring & sales handoff.

## Domain Models

| Model           | Table               | FSM States                                  |
| --------------- | ------------------- | ------------------------------------------- |
| Campaign        | `campaigns`         | DRAFT → ACTIVE → PAUSED → COMPLETED         |
| TrackingEvent   | `tracking_events`   | (append-only)                               |
| AudienceSegment | `audience_segments` | ACTIVE → ARCHIVED                           |
| ContentAsset    | `content_assets`    | DRAFT → PUBLISHED → ARCHIVED                |
| LeadScore       | `lead_scores`       | NEW → QUALIFIED → HANDED_OFF / DISQUALIFIED |

## Dashboard

Live data-fetching dashboard served from `/` and `/vmarketing-org/` with 5 sections:

- **[SyR-MKT-00] ABM Campaigns** — Table: code (monospace), name, stage, channel, budget w/ % bar, target accounts, engaged (green), MQLs (purple), status pill. Metrics: Total, Active, Draft, Paused, Completed, Total MQLs
- **[SyR-MKT-02] Audience Segments** — Table: code, name, tier pill (TIER_1 purple, TIER_2 blue, TIER_3 gray), account count, status pill. Metrics: Total segments, Tier 1, Tier 2, Tier 3, Total accounts
- **[SyR-MKT-03] Content Assets** — Table: code, title (truncated 180px), type, stage, downloads, views, status pill. Metrics: Total, Published (green), Draft (orange), Total downloads
- **[SyR-MKT-04] Lead Scoring** — Table (full width): org, contact, title, score (0-100 bar with HOT/WARM/COLD colour), grade pill, status, handed_off_to. Metrics: Total leads, HOT (red), WARM (orange), COLD (blue), Qualified, Avg score
- **[SyR-MKT-01] Tracking Events** — Table (full width): code, org, action_type, page_resource, dwell_seconds, intent_score (≥70 red / ≥40 orange / <40 gray), created_at (formatted). Metrics: Total events + dynamic metric pills per action type

Dark GitHub theme (#0d1117 bg, #161b22 cards, #30363d borders). 5 async `fetch()` calls to `/api/v1/vmarketing-org/*` on page load. Status pills with semantic colours. Responsive grid layout.

## API Endpoints

| Method | Path                                                          | Purpose                   |
| ------ | ------------------------------------------------------------- | ------------------------- |
| GET    | `/health`                                                     | Health check              |
| GET    | `/api/v1/vmarketing-org/campaigns`                            | List campaigns            |
| POST   | `/api/v1/vmarketing-org/campaigns`                            | Create campaign           |
| GET    | `/api/v1/vmarketing-org/campaigns/{id}`                       | Get campaign              |
| PATCH  | `/api/v1/vmarketing-org/campaigns/{id}`                       | Update campaign           |
| POST   | `/api/v1/vmarketing-org/campaigns/{id}/launch`                | Launch (DRAFT→ACTIVE)     |
| POST   | `/api/v1/vmarketing-org/campaigns/{id}/pause`                 | Pause (ACTIVE→PAUSED)     |
| POST   | `/api/v1/vmarketing-org/campaigns/{id}/complete`              | Complete campaign         |
| GET    | `/api/v1/vmarketing-org/tracking-events`                      | List events               |
| POST   | `/api/v1/vmarketing-org/tracking-events`                      | Ingest event              |
| GET    | `/api/v1/vmarketing-org/tracking-events/{id}`                 | Get event                 |
| GET    | `/api/v1/vmarketing-org/tracking-events/intent-summary/{org}` | Intent aggregation        |
| GET    | `/api/v1/vmarketing-org/segments`                             | List segments             |
| POST   | `/api/v1/vmarketing-org/segments`                             | Create segment            |
| GET    | `/api/v1/vmarketing-org/segments/{id}`                        | Get segment               |
| POST   | `/api/v1/vmarketing-org/segments/{id}/archive`                | Archive segment           |
| GET    | `/api/v1/vmarketing-org/assets`                               | List content assets       |
| POST   | `/api/v1/vmarketing-org/assets`                               | Create asset              |
| GET    | `/api/v1/vmarketing-org/assets/{id}`                          | Get asset                 |
| POST   | `/api/v1/vmarketing-org/assets/{id}/publish`                  | Publish (DRAFT→PUBLISHED) |
| POST   | `/api/v1/vmarketing-org/assets/{id}/archive`                  | Archive asset             |
| GET    | `/api/v1/vmarketing-org/leads`                                | List leads                |
| POST   | `/api/v1/vmarketing-org/leads`                                | Score / upsert lead       |
| GET    | `/api/v1/vmarketing-org/leads/{id}`                           | Get lead                  |
| POST   | `/api/v1/vmarketing-org/leads/{id}/qualify`                   | Qualify (NEW→QUALIFIED)   |
| POST   | `/api/v1/vmarketing-org/leads/{id}/handoff`                   | Hand off to sales         |
| POST   | `/api/v1/vmarketing-org/leads/{id}/disqualify`                | Disqualify lead           |

## Tech Stack

- Python 3.12 · FastAPI · SQLAlchemy 2 (async) · PostgreSQL 16 · Redis 7
- gRPC client → vKernel:9090
- Alembic migrations (version table: `alembic_version_vmarketing_org`)

## Running

```bash
# Via Docker Compose (recommended)
make up

# Or standalone
cd 05-vmarketing-org
pip install -r requirements.txt
uvicorn app.main:app --port 8084
```

## Tests

All tests assume PostgreSQL is running (via `make up` or manual `docker-compose up postgres`).

```bash
# Run vMarketing-Org tests only
make test-marketing-org

# Or manually
cd 05-vmarketing-org
pytest -v
```

**Note:** Tests integrate with live database (seed data: 2 campaigns, 2 segments, 2 assets, 0 leads, 0 events). Alembic auto-migrates on app startup.

## Recent Changes (v1.7.1)

**Fixed:** Critical table name mismatch in models.py. ORM declared `vmkt_campaigns`, `vmkt_tracking_events`, etc. but alembic created `campaigns`, `tracking_events` (no `vmkt_` prefix). Result: all 5 APIs returned HTTP 500. Fixed all 5 tablenames to match actual DB schema.

**Rebuilt:** `static/index.html` from static 5-card placeholder to live 270-line data-fetching dashboard with real API integration, 5 sections, metric counters, status pills, colour-coded indicators.

**Added:** Shared UI topbar to vmarketing-org (matching vStrategy, vFinacc, vDesign). All 4 vApps now reference `/ui/app-layout.{css,js}` from vKernel. Iframe detection prevents duplicate topbar inside shell.

## Integration Points

- **vKernel:** gRPC events (campaign.launched, lead.qualified, lead.handed_off); shared UI topbar at `/ui/**`
- **vStrategy:** Subscribes to `strategy.kpi.updated` for campaign alignment
- **vFinAcc:** Budget tracking events may feed into finance module; shared UI topbar
- **vDesign Physical:** Content assets may reference physical design specs; shared UI topbar

## Cross-references

- PRD: `00-design/vmarketing-org-prd.md`
- Gateway routes: `01-vkernel/src/main/resources/application.yml`
- Flyway: `01-vkernel/.../V10__register_vmarketing_org.sql`
