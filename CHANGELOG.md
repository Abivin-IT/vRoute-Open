# Changelog — vRoute-Open

Tất cả thay đổi đáng chú ý được ghi nhận tại đây. Format: [Keep a Changelog](https://keepachangelog.com/).

## [1.7.0] — 2026-03-02

### Added — vDesign Physical + vMarketing Org Full Implementation

**vDesign Physical (`04-vdesign-physical/`, port 8083)**

- 5 ORM models: `GoldenSample` (ACTIVE/SEALED/COMPROMISED/EXPIRED), `MaterialInbox` (PENDING/TESTED/ARCHIVED/SCRAPPED), `Prototype` (ACTIVE/IN_TRANSIT/OBSOLETE/DESTROYED), `LabTest` (RUNNING/PASSED/FAILED/CONDITIONAL), `HandoverKit` (PACKING/READY/DISPATCHED/RECEIVED)
- Business logic `service.py`: Spec Master Vault (seal/activation/convergence %), Material Ingestion (LIMS + sensor data), Prototype Version Control (RFID location tracking), Lab Feasibility Checker (stress-test execution + failure analysis), Handover Kit workflow (packing + dispatch)
- 26 REST endpoints at `/api/v1/vdesign-physical` — Golden Samples CRUD, Materials, Prototypes, Lab Tests with summary, Handover Kits, Health
- Alembic migration `0001_vdesign_physical_init.py` — 5 tables + indexes + seed data (demo golden samples, materials, prototypes, lab tests, handover kits)
- 35 integration tests (pytest-asyncio + httpx + aiosqlite) — all SyR-PHY-00→04 requirements covered
- Dark-themed HTML dashboard (`static/index.html`) — all 5 domain cards
- TypeScript frontend (`frontend/`): `types.ts`, `api.ts`, `renderers.ts`, `main.ts` + IIFE bundler
- `Dockerfile` — 2-stage: Node 20-alpine (TS build) + Python 3.12-slim (runtime), port 8083
- `manifest.json` — 3 permissions (`phys.spec.seal`, `phys.inventory.audit`, `phys.lab.execute`), 4 published events, 3 subscribed events
- `04-vdesign-physical/README.md` — tech stack, API table, cross-references

**vMarketing Org (`05-vmarketing-org/`, port 8084)**

- 5 ORM models: `Campaign` (DRAFT/ACTIVE/PAUSED/COMPLETED), `TrackingEvent` (intent signals + IP-to-company), `AudienceSegment` (firmographic rules, TIER_1/2/3), `ContentAsset` (5 asset types, GATED/PUBLISHED), `LeadScore` (HOT/WARM/COLD + account score formula)
- Business logic `service.py`: ABM Campaign Orchestrator, Tracking Pixel (collective behavior scoring, high-value action detection), Audience Segment engine (firmographic/technographic tiering), Content Asset Hub (gated content + compliance audit), Lead Scorer (ωf·Firmographics + ωi·ΣIntent, BANT mapping, auto-handover trigger)
- 27 REST endpoints at `/api/v1/vmarketing-org` — Campaigns CRUD, Tracking Events with intent summary, Segments, Content Assets, Lead Scores, Health
- Alembic migration `0001_vmarketing_org_init.py` — 5 tables + indexes + seed data (demo campaigns, events, segments, assets, lead scores)
- 28 integration tests (pytest-asyncio + httpx + aiosqlite) — all SyR-MKT-ORG-00→04 requirements covered
- Dark-themed HTML dashboard (`static/index.html`) — all 5 domain cards
- TypeScript frontend (`frontend/`): `types.ts`, `api.ts`, `renderers.ts`, `main.ts` + IIFE bundler
- `Dockerfile` — 2-stage: Node 20-alpine (TS build) + Python 3.12-slim (runtime), port 8084
- `manifest.json` — 3 permissions (`mkt.abm.orchestrate`, `mkt.pixel.configure`, `mkt.lead.handover`), 4 published events, 3 subscribed events
- `05-vmarketing-org/README.md` — tech stack, API table, cross-references

**Infrastructure Updates**

- `03-vfinacc/Dockerfile` — Upgraded to 2-stage build (Node 20-alpine + Python 3.12-slim); TypeScript frontend added
- `80-deploy/docker-compose.yml` — Added `vdesign-physical` and `vmarketing-org` services (port 8083, 8084)
- `01-vkernel` — Flyway `V9__register_vdesign_physical.sql` + `V10__register_vmarketing_org.sql` migrations; `SecurityConfig.java` permit-all for new vApp routes; `application.yml` gateway routes added
- `Makefile` — Added `test-design-physical` and `test-marketing-org` targets; `make test` runs all 5 suites
- `.github/workflows/ci.yml` — Added `test-vdesign-physical` and `test-vmarketing-org` jobs; vKernel Surefire upload `if: failure()` → `if: always()`; added `dorny/test-reporter@v1` to surface JUnit results as PR check annotations

---

## [1.6.0] — 2026-03-02

### Added — PRDs & Build Plan for 2 New vApps

- **vDesign Physical PRD** (`00-design/docs/vdesign-physical-prd.md`) — Physical Layer module for Idea-to-Spec: Spec Master (Golden Sample Vault), Idea Inbox (Material Ingestion), Version Control (Prototype Tracker), Feasibility Checker (Lab Stress Test), Handover Kit (Tooling Shipment). 5 SyRs (SyR-PHY-00 through SyR-PHY-04), 5 NFRs, manifest sample, 4 Gherkin acceptance criteria.
- **vMarketing Organization PRD** (`00-design/docs/vmarketing-org-prd.md`) — M2L ABM Engine: Campaign Orchestrator, Tracking Pixel (IP-to-Company Intent Sensing), Audience Segment (Firmographic/Technographic), Content Asset (Knowledge Hub), Lead Scorer (Account Qualification + Auto-Handover). 5 SyRs (SyR-MKT-ORG-00 through SyR-MKT-ORG-04), 5 NFRs, manifest sample, 3 Gherkin scenarios.
- **TODO Steps 10 & 11** — Detailed build plans: Step 10 = vDesign Physical (port 8083, `04-vdesign-physical/`), Step 11 = vMarketing Organization (port 8084, `05-vmarketing-org/`).

---

## [1.5.1] — 2026-03-02

### Fixed

- **vFinacc Alembic migration crash** — `op.get_bind().exec_driver_sql()` fails on SQLAlchemy 2.x (`TypeError: immutabledict`). Replaced with `op.execute(sa.text())` + `ON CONFLICT DO NOTHING` for each seed INSERT. (`e1aca63`)
- **Gateway UI routing 404** — `/vfinacc/**` and `/vstrategy/**` forwarded full path to backend but FastAPI static mount expected `/`. Added `RewritePath` filters in `application.yml` and explicit UI catch-all routes in both `main.py` files. (`90698c0`)
- **`/api/v1/` returning empty** — No handler existed for this path. Added `GET /api/v1{/}` in `DashboardController.java` redirecting to `/dashboard/api` + `permitAll` in `SecurityConfig`. (`46c8006`)

### Added

- **Single-port access** — All services now accessed exclusively through vKernel gateway `:8080`. Removed host port bindings for vstrategy (8081) and vfinacc (8082) in docker-compose. Added `permitAll` for all vApp proxy paths. Updated Makefile, README, user guide, developer guide. (`2df0e3e`)
- **Per-module READMEs with cross-references** — `01-vkernel/README.md`, `02-vstrategy/README.md`, `03-vfinacc/README.md` — each documents its tech stack, API endpoints, integration points, and bidirectional links to sibling modules.

---

## [1.5.0] — 2026-03-02

### Changed — Project Restructure: Numbered Folders + Guides

**Folder Restructure (numbered prefixes: lower = more important)**

- `vkernel/` → `01-vkernel/` — Core OS (highest priority)
- `vstrategy/` → `02-vstrategy/` — vApp #1
- `vfinacc/` → `03-vfinacc/` — vApp #2
- `docs/prd/` → `00-design/docs/` — PRD documents
- `sheets/` → `00-design/sheets/` — Data tables & contracts
- `helm/` + `docker-compose.yml` → `80-deploy/` — Deployment infrastructure grouped
- Created `90-guide/` — User + Developer documentation

**vKernel Awareness of vFinacc**

- `.github/workflows/ci.yml` — Added `test-vfinacc` job (Python 3.12, pytest), vfinacc image push to GHCR, updated all `working-directory` paths
- `Makefile` — Updated DIR vars (`VKERNEL_DIR`, `VSTRATEGY_DIR`, `VFINACC_DIR`, `DEPLOY_DIR`), `COMPOSE` now uses `-f 80-deploy/docker-compose.yml`, `make up` banner includes vFinacc
- `80-deploy/docker-compose.yml` — Build contexts updated to parent-relative paths (`../01-vkernel`, `../02-vstrategy`, `../03-vfinacc`)
- `01-vkernel/src/main/resources/application.yml` — Improved gateway route comments with folder references, added generic vApp route template

**World-Class Documentation**

- `90-guide/user/README.md` — Comprehensive user guide: Authentication (JWT, SSO, Magic Link), Using vKernel/vStrategy/vFinacc, API endpoint tables, Troubleshooting
- `90-guide/developer/README.md` — Developer guide: Architecture overview, Getting Started, Project Structure, How to Add a New vApp (7-step checklist), Coding Standards, Testing Strategy, Database & Migrations, gRPC IPC, Event Bus, CI/CD Pipeline, Deployment, Contributing

**README.md Rewrite**

- Project structure tree updated with all numbered folders
- Helm path updated to `./80-deploy/helm/vroute`

---

## [1.4.0] — 2026-03-12

### Added — vFinacc: vFinance R2R Module (SyR-FIN-00 through SyR-FIN-04)

**PRD & Design Sheets**

- `docs/prd/vfinacc-prd.md` — Full PRD (5 system requirements, NFRs, architecture overview)
- `sheets/vfinacc/api-contract.md` — REST API contract table (16 endpoints: Ledger, Transactions, Reconciliation, Cost Centers, Compliance, Health)
- `sheets/vfinacc/acceptance-criteria.md` — 7 Gherkin acceptance scenarios
- `sheets/vfinacc/data-model.md` — 5 table schemas with column types and constraints

**vFinacc Backend (Python 3.12 / FastAPI)**

- `vfinacc/app/config.py` — Pydantic Settings (port 8082, env-based configuration)
- `vfinacc/app/database.py` — Async SQLAlchemy engine (lazy init, asyncpg/aiosqlite)
- `vfinacc/app/models.py` — 5 ORM models: `LedgerEntry` (DRAFT/POSTED/FLAGGED/REVERSED), `Transaction` (RAW/MATCHED/RECONCILED/REJECTED), `ReconciliationMatch` (3-way: FULL/PARTIAL/NO_MATCH), `CostAllocation` (GROW/RUN/TRANSFORM/GIVE), `ComplianceCheck` (PASS/FLAG/FAIL)
- `vfinacc/app/schemas.py` — Pydantic v2 DTOs (from_attributes, field validators)
- `vfinacc/app/service.py` — Business logic (~290 lines): Continuous Ledger CRUD+posting, Transaction Ingestor, 3-way Reconciliation Engine (confidence %), Cost Center allocation (68/27/5/0.1 targets, 2% tolerance), Tax & Compliance Guard (VAT 10%, CIT 20%, $25K threshold)
- `vfinacc/app/routes.py` — FastAPI Router at `/api/v1/vfinacc` (16 endpoints)
- `vfinacc/app/grpc_client.py` — KernelGrpcClient (source="vfinacc", graceful degradation)
- `vfinacc/app/main.py` — FastAPI entry with lifespan (gRPC ping on startup), CORS, static files
- `vfinacc/manifest.json` — vApp manifest: 4 permissions, 4 published events, 2 subscribed events, depends on vkernel + vstrategy

**Database Migrations**

- `vfinacc/alembic.ini` + `alembic/env.py` — Alembic config (version table `alembic_version_vfinacc`)
- `vfinacc/alembic/versions/0001_vfinacc_init.py` — Schema (5 tables + indexes) + seed data (demo ledger entries, transactions, reconciliation matches, cost allocations, compliance checks)
- `V8__register_vfinacc.sql` — Flyway: register vfinacc in App Registry + inject 4 permissions

**Testing**

- `vfinacc/tests/test_finance_api.py` — 25 integration tests (pytest-asyncio + httpx + SQLite in-memory) covering all 5 SyR-FIN requirements: Ledger (7), Transactions (3), Reconciliation (5), Cost Centers (6), Compliance (6), Health (1)

**UI**

- `vfinacc/static/index.html` — Dark-theme dashboard (4 cards: Continuous Ledger, Reconciliation Engine, Cost Center Allocation, Tax & Compliance)

**Infrastructure**

- `vfinacc/Dockerfile` — 2-stage: Node 20-alpine (frontend) + Python 3.12-slim (runtime), port 8082
- `vfinacc/requirements.txt` — 15 dependencies (same stack as vstrategy)
- `vfinacc/pyproject.toml` — Project config + pytest settings

### Changed

- `docker-compose.yml` — Added vfinacc service (port 8082, shared DB, depends on postgres)
- `application.yml` — Added gateway routes: `vfinacc-route` (`/api/v1/vfinacc/**`) + `vfinacc-ui` (`/vfinacc/**`) → vfinacc:8082
- `Makefile` — Parameterized `pytest` macro (accepts directory arg), added `test-finacc` target, updated `test` to include vfinacc, updated `clean` for vfinacc pycache
- `README.md` — Added vFinacc to architecture diagram, tech stack, project structure, quick start section

---

## [1.3.0] — 2026-03-11

### Added — OIDC SSO + Magic Link + Universal Search + UI Shell + Helm

**OIDC/OAuth2 SSO (SyR-PLAT-01 complete)**

- `V7__oidc_magiclink_search.sql` — Flyway migration: `kernel_oidc_accounts`, `kernel_magic_links`, `kernel_search_index` tables + tsvector trigger
- `OidcAccountEntity.java` — `@GovernanceID 1.6.0` — Linked OIDC accounts (Google/Microsoft/GitHub), JSONB raw claims
- `OidcAuthController.java` — `@GovernanceID 1.6.1` — Full SSO flow: `GET /api/v1/auth/oidc/{provider}` (authorize URL), `GET /api/v1/auth/oidc/{provider}/callback` (code exchange → JWT), `GET /api/v1/auth/oidc/accounts` (list linked)

**Magic Link Passwordless Auth**

- `MagicLinkEntity.java` — `@GovernanceID 1.7.0` — Magic link tokens with SHA-256 hash, 15-minute TTL
- `MagicLinkController.java` — `@GovernanceID 1.7.1` — `POST /api/v1/auth/magic-link` (generate link), `GET /api/v1/auth/magic-link/verify` (verify → JWT)

**Universal Search (SyR-PLAT-02.02)**

- `SearchIndexEntity.java` — `@GovernanceID 5.0.0` — Unified search index entity (tsvector on PostgreSQL, LIKE fallback on H2)
- `SearchController.java` — `@GovernanceID 5.1.0` — `GET /api/v1/search?q=...&type=...&limit=...` (FTS with ranking), `POST /api/v1/search/index` (manual indexing)

**Adaptive UI Shell (SyR-PLAT-04)**

- `AdaptiveShellController.java` — `@GovernanceID 4.0.0` — Micro-frontend host: `GET /shell` (app launcher), `GET /shell/{appId}` (iframe isolation per vApp), sidebar nav, Ctrl+K search integration

**Helm Chart (K8s deployment)**

- `helm/vroute/Chart.yaml` — Helm v2 chart (appVersion 1.3.0)
- `helm/vroute/values.yaml` — Configurable: PostgreSQL, Redis, vKernel (2 replicas), vStrategy, Ingress (nginx + TLS), ServiceMonitor (Prometheus)
- `helm/vroute/templates/` — deployment-vkernel, deployment-vstrategy, statefulset-postgresql, deployment-redis, services, secrets, ingress, servicemonitor

### Changed

- `SecurityConfig.java` — Added permitAll for `/api/v1/auth/oidc/**`, `/api/v1/auth/magic-link/**`, `/api/v1/search`, `/shell/**`
- `application.yml` — Added `vkernel.oidc` config block (Google/Microsoft/GitHub client-id/secret via env vars)
- `Makefile` — **Test optimization**: prefers local Maven/Python (< 1s/test) over Docker; Docker fallback now uses volume caches (`vroute-maven-cache`, `vroute-pip-cache`), parallel execution (`-T 1C`); replaces `run.sh`

### Fixed

- `DashboardController.java` — Fixed `app.getDisplayName()` → `app.getName()` (method didn't exist on AppRegistryEntity)

## [1.2.0] — 2026-03-10

### Added — gRPC IPC + Auth Hardening + Prometheus + CI/CD

**Step 6: gRPC Internal Communication**

- `vkernel/src/main/proto/kernel.proto` — proto3 service definition: `KernelService` with `Ping`, `PublishEvent`, `GetInstalledApps` RPCs
- `vkernel/src/main/java/com/abivin/vkernel/g4_grpc/KernelGrpcService.java` — `@GrpcService` implementation, listens on port 9090
- `vkernel/pom.xml` — added `net.devh:grpc-server-spring-boot-starter:3.1.0.RELEASE`, `org.xolstice.maven.plugins:protobuf-maven-plugin:0.6.1`, `os-maven-plugin`
- `vkernel/src/main/resources/application.yml` — `grpc.server.port: 9090`
- `vstrategy/protos/kernel.proto` — proto copy for Python stub generation
- `vstrategy/app/grpc_client.py` — `KernelGrpcClient` with graceful degradation if gRPC unreachable
- `vstrategy/Dockerfile` — runs `grpc_tools.protoc` to auto-generate `app/grpc/` stubs at build time
- `docker-compose.yml` — exposes `9090:9090` on vKernel, adds `KERNEL_GRPC_HOST`/`KERNEL_GRPC_PORT` to vstrategy
- `vstrategy/app/main.py` — lifespan now pings Kernel gRPC on startup, closes channel on shutdown

**Step 7: Auth Hardening**

- `vkernel/src/main/resources/db/migration/V6__auth_hardening.sql` — `kernel_refresh_tokens` + `kernel_rate_limit_log` tables
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/RefreshTokenEntity.java` — DB entity, SHA-256 token hash, rotation chain
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/RefreshTokenService.java` — issue/rotate/revokeAll with reuse-attack detection
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/AuthController.java` — `POST /api/v1/auth/refresh` + `POST /api/v1/auth/logout`, login now returns `refresh_token`
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/RateLimitFilter.java` — sliding-window rate limiter (10 req/60s per IP for login/register)
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/TenantContext.java` — ThreadLocal tenant_id propagation
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/JwtProvider.java` — `tenant_id` claim embedded in JWT
- `vkernel/src/main/java/com/abivin/vkernel/g1_iam/SecurityConfig.java` — TenantContext set/clear in JWT filter; `/actuator/prometheus` permitted

**Backlog: Prometheus + CI/CD**

- `vkernel/pom.xml` — `micrometer-registry-prometheus` + `spring-boot-starter-actuator`
- `vkernel/src/main/resources/application.yml` — actuator endpoints exposed including `/actuator/prometheus`
- `.github/workflows/ci.yml` — 4-job CI pipeline: `test-vkernel` (mvn verify) → `test-vstrategy` (pytest, includes proto stub generation) → `docker-build` → `push-images` (GHCR, main branch only)

### Fixed

- `vkernel/src/main/resources/db/migration/V1__init_schema.sql` — `CHAR(2/3)` → `VARCHAR(2/3)` (Hibernate schema validation was failing)
- `vstrategy/Dockerfile` — `ENV PYTHONPATH=/app` (Alembic `ModuleNotFoundError: No module named 'app'`)
- `vstrategy/alembic/versions/0001_vstrategy_init.py` — `op.execute()` → `op.get_bind().exec_driver_sql()` (JSON colons interpreted as SQLAlchemy bind params)
- `vstrategy/requirements.txt` — added `psycopg2-binary==2.9.10` (Alembic sync engine requirement)

### Changed — vStrategy Python Rewrite (Java → Python/FastAPI)

**vStrategy backend rewritten entirely in Python 3.12 / FastAPI** — same API contract, same DB schema, same business logic:

- **Removed**: `pom.xml`, `src/` (all Java: `VStrategyApplication.java`, `PlanEntity.java`, `AlignmentNodeEntity.java`, `PivotSignalEntity.java`, `StrategyService.java`, `StrategyController.java`, `StrategyApiTests.java`, `V1__vstrategy_init.sql`)
- `requirements.txt` — FastAPI 0.115.6, SQLAlchemy 2.0.36 (async), Alembic 1.14.1, Pydantic 2.10.4, pytest-asyncio, httpx, aiosqlite
- `pyproject.toml` — Project metadata + pytest config (asyncio_mode = "auto")
- `app/config.py` — Pydantic Settings (env-based configuration)
- `app/database.py` — Lazy async SQLAlchemy engine + session factory (supports asyncpg/aiosqlite)
- `app/models.py` — SQLAlchemy ORM: `Plan`, `AlignmentNode`, `PivotSignal` with `FlexibleJSON` TypeDecorator (JSONB on PostgreSQL, JSON on SQLite)
- `app/schemas.py` — Pydantic v2 request/response DTOs
- `app/service.py` — Full business logic: CRUD, tree propagation, BSC scorecard, 68/27/5 S&OP validation, pivot signal detection
- `app/routes.py` — FastAPI Router at `/api/v1/vstrategy` (identical API contract to Java version)
- `app/main.py` — FastAPI app with CORS, lifespan, static file serving
- `alembic/versions/0001_vstrategy_init.py` — Schema + seed data migration (replaces Flyway)
- `alembic.ini` + `alembic/env.py` — Alembic config (uses `alembic_version_vstrategy` version table)

**Frontend rewritten in TypeScript**:

- `frontend/src/types.ts` — TypeScript interfaces (Plan, AlignmentNode, TreeNode, Scorecard, etc.)
- `frontend/src/api.ts` — Typed API client
- `frontend/src/renderers.ts` — Pure render functions (scorecard, tree, S&OP, signals)
- `frontend/src/main.ts` — Entry point (loadPlans, loadDashboard)
- `frontend/scripts/bundle.js` — Simple TS→IIFE bundler
- `static/index.html` — Same dark-theme dashboard

**Tests**: 19 integration tests (pytest-asyncio + httpx + SQLite in-memory) — all passing

**Infrastructure**:

- `Dockerfile` — Two-stage: Node 20-alpine (TS build) + Python 3.12-slim (runtime)
- `docker-compose.yml` — Updated env vars (`DATABASE_URL`), service comment
- `Makefile` (`test-strategy` target) — Added pytest runner, switched vstrategy from Maven to pytest

---

## [1.0.0] — 2026-03-02

### Added — Step 5: vStrategy vApp (SyR-STR-00 through SyR-STR-04)

**vStrategy — S2P2R Strategy Execution Module** (`vstrategy/`):

- `pom.xml` — Spring Boot 3.3.7, JPA, Flyway, H2 test
- `Dockerfile` — Multi-stage build, port 8081
- `VStrategyApplication.java` — `@GovernanceID vstrategy.0.0-BOOT`
- `PlanEntity.java` — `@GovernanceID vstrategy.0.0` — Strategic plan container (JSONB: baseline, MECE, decision log, S&OP config)
- `AlignmentNodeEntity.java` — `@GovernanceID vstrategy.0.1` — Universal tree node (VISION→BSC→OKR→INITIATIVE→TASK) with self-referential hierarchy
- `PivotSignalEntity.java` — `@GovernanceID vstrategy.0.2` — Threshold-based pivot triggers (RUNWAY_SECURITY, GROWTH_MOMENTUM)
- `StrategyService.java` — `@GovernanceID vstrategy.1.0` — Tree propagation, BSC scorecard, 68/27/5 validation, pivot signal detection
- `StrategyController.java` — `@GovernanceID vstrategy.2.0` — Full REST API (plans, tree, scorecard, S&OP, signals)
- `V1__vstrategy_init.sql` — Schema + seed data (demo Q1-2026 plan with full alignment tree)
- `manifest.json` — vApp manifest for App Engine registration
- `static/index.html` — Live dashboard (Alignment Tree, BSC bars, S&OP validation, Pivot Signals)
- `StrategyApiTests.java` — 20 integration tests (CRUD, propagation, scorecard, 68/27/5, pivot)
- `VStrategyApplicationTests.java` — Context load smoke test

**vKernel updates:**

- `V5__register_vstrategy.sql` — Auto-register vStrategy in App Registry + inject permissions
- `application.yml` — Gateway routes: `/api/v1/vstrategy/**` + `/vstrategy/**` → vstrategy:8081

**Infrastructure:**

- `docker-compose.yml` — Added vStrategy service (port 8081, shared DB)
- `Makefile` — `make {help|proto|build|dev|up|down|logs|ps|test|test-kernel|test-strategy|clean|clean-docker}` — replaces `run.sh`
- `docs/prd/vstrategy-prd.md` — vStrategy PRD (synced from Google Docs)

---

## [0.4.0] — 2026-03-02

### Added — Step 4: App Engine Full (SyR-PLAT-00)

**Flyway:**

- `V4__app_engine_tables.sql` — `kernel_app_registry` + `kernel_permissions` tables; seeds built-in apps (Settings, App Store)

**g0_engine — App Engine:**

- `AppRegistryEntity.java` — `@GovernanceID 0.1.0` — DB-backed app registry (`kernel_app_registry`); status: ACTIVE/INACTIVE/FAILED; manifest JSONB
- `PermissionEntity.java` — `@GovernanceID 1.2.0` — Permission injection registry (`kernel_permissions`); unique `permission_code`
- `ManifestModel.java` — `@GovernanceID 0.2.0` — Manifest POJO with `validate()`, regex format check on `app.id`
- `AppLifecycleService.java` — `@GovernanceID 0.3.0` — Install (dep resolution → registry → inject permissions → event), Uninstall (reverse-dep check → deactivate → event)
- `AppRegistryController.java` — `@GovernanceID 0.0.0` — Refactored: replaced hardcoded list with `AppLifecycleService`; added `DELETE /api/v1/apps/{appId}`, `GET /api/v1/apps/permissions`

---

## [0.3.0] — 2026-03-02

### Added — Step 3: Event Bus (SyR-PLAT-03)

**Flyway:**

- `V3__event_tables.sql` — `kernel_event_log` (append-only, no `updated_at`) + `kernel_event_subscriptions`; GIN + B-tree indexes

**g3_event — Event Bus:**

- `EventLogEntity.java` — `@GovernanceID 3.0.0` — Immutable event log entity + nested Repository (paginated by source/type)
- `SubscriptionEntity.java` — `@GovernanceID 3.0.1` — Pub/Sub subscription entity (UNIQUE subscriber+type)
- `KernelEvent.java` — `@GovernanceID 3.1.1` — Spring `ApplicationEvent` for in-process fan-out
- `EventBusService.java` — `@GovernanceID 3.1.0` — DB-first publish (QUEUED→DELIVERED) + Spring in-process fan-out; idempotent subscribe
- `EventBusController.java` — `@GovernanceID 3.2.0` — `POST /events/publish`, `POST /events/subscribe`, `GET /events/subscriptions`, `GET /events/log`

**Infrastructure:**

- `docker-compose.yml` — Added Redis 7-alpine service (port 6379, healthcheck); vkernel depends on it; `REDIS_HOST`/`REDIS_PORT` env vars passed
- `.env` — Added `REDIS_HOST=redis`, `REDIS_PORT=6379`

---

## [0.2.0] — 2026-03-02

### Added — Step 2: Data Backbone + Core Entities (SyR-PLAT-02)

**Flyway Schema Migrations:**

- `V1__init_schema.sql` — DDL for all tables: `kernel_users`, `kernel_tenants`, `kernel_stakeholders`, `kernel_currencies`, `kernel_countries`. GIN indexes on JSONB + full-text search.
- `V2__seed_data.sql` — Seed: 8 currencies (VND, USD, EUR, JPY, CNY, KRW, THB, SGD), 8 countries (VN, US, SG, JP, KR, CN, TH, DE), default tenant.

**g2_data (SyR-PLAT-02 — Data Backbone):**

- `TenantEntity.java` — `@GovernanceID 2.0.0` — `kernel_tenants` table + JSONB metadata
- `StakeholderEntity.java` — `@GovernanceID 2.0.1` — Golden Records (CUSTOMER/VENDOR/PARTNER) + JSONB + native JSONB query
- `CurrencyEntity.java` — `@GovernanceID 2.0.2` — ISO 4217 reference data
- `CountryEntity.java` — `@GovernanceID 2.0.3` — ISO 3166-1 reference data
- `DataExtensionController.java` — `@GovernanceID 2.1.0` — PATCH extend API, CRUD stakeholders, list currencies/countries

**Config Changes:**

- `pom.xml` — Added Flyway Core + Flyway PostgreSQL dependencies
- `application.yml` — Switched `ddl-auto: update` → `validate` + Flyway enabled
- `application-test.yml` — Flyway disabled, H2 MODE=PostgreSQL for compatibility

---

## [0.1.0] — 2026-03-02

### Added — Step 1: vKernel Core Initialization

**Build & Infrastructure:**

- `vkernel/pom.xml` — Maven project: Java 21, Spring Boot 3.3.7, Spring Cloud 2023.0.4 (Gateway MVC), jjwt 0.12.6, JPA, PostgreSQL, H2 (test)
- `vkernel/Dockerfile` — Multi-stage build (maven → jre-alpine)
- `docker-compose.yml` — PostgreSQL 16 + vKernel, healthcheck, volume persistence
- `.env` — Dev environment variables template

**Core Application:**

- `VKernelApplication.java` — `@GovernanceID 0.0.0-BOOT` — Entry point

**g1_iam (SyR-PLAT-01 — Identity & Access Management):**

- `SecurityConfig.java` — `@GovernanceID 1.0.0` — JWT stateless filter, BCrypt encoder, public auth routes
- `AuthController.java` — `@GovernanceID 1.0.1` — POST `/api/v1/auth/register`, POST `/api/v1/auth/login`
- `JwtProvider.java` — `@GovernanceID 1.0.2` — Token generation/validation (HMAC-SHA)
- `UserEntity.java` — `@GovernanceID 1.1.0` — `kernel_users` table + co-located Repository interface

**g0_engine (SyR-PLAT-00 — App Lifecycle):**

- `AppRegistryController.java` — `@GovernanceID 0.0.0` — GET `/api/v1/apps`, POST `/api/v1/apps/install` (stub)

**Config & Test:**

- `application.yml` — PostgreSQL datasource, JWT config, Gateway MVC route template
- `application-test.yml` — H2 in-memory for unit tests
- `VKernelApplicationTests.java` — Spring context smoke test

**Docs:**

- `README.md` — Architecture overview, project structure, quick start
- `CHANGELOG.md` — This file
- `TODO.md` — Next steps roadmap
