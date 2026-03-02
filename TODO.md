# TODO — vRoute-Open Platform

> Danh sách task cho các prompt tiếp theo. Mỗi Step = 1 prompt session.

## ~~Step 2: Data Backbone + Core Entities (SyR-PLAT-02)~~ ✅ DONE

- [x] Tạo package `g2_data` — Core Entities: `TenantEntity`, `StakeholderEntity`, `CurrencyEntity`, `CountryEntity`
- [x] JSONB metadata column cho dynamic field extension (SyR-PLAT-02.01)
- [x] Data Extension API: `PATCH /api/v1/data/entities/{type}/{id}/extend`
- [x] Flyway migration scripts thay thế `ddl-auto: update` (V1 schema + V2 seed)
- [x] Seed data: 8 currencies, 8 countries, default tenant

## ~~Step 3: Event Bus & IPC (SyR-PLAT-03)~~ ✅ DONE

- [x] Tạo package `g3_event` — Event Registry + Pub/Sub engine
- [x] `POST /api/v1/events/publish` — Event publishing API
- [x] `POST /api/v1/events/subscribe` — Subscription registration
- [x] Audit trail logging (immutable event log table)
- [x] Redis service in docker-compose (distributed pub/sub — Spring dep deferred)

## ~~Step 4: App Engine Full (SyR-PLAT-00 complete)~~ ✅ DONE

- [x] Manifest.json parser + validator (`ManifestModel.java`)
- [x] Dependency resolution engine (`AppLifecycleService`)
- [x] `app_registry` table — DB-backed, replaces hardcoded stub
- [x] Permission injection on install (`PermissionEntity` + `AppLifecycleService`)
- [x] Install/Uninstall lifecycle + `APP_INSTALLED`/`APP_UNINSTALLED` events

## ~~Step 5: First vApp — vStrategy~~ ✅ DONE (v1.1 Python rewrite)

- [x] Scaffold `vstrategy/` — Spring Boot 3.3.7 project (port 8081, shared PostgreSQL DB)
- [x] S2P2R entities: `PlanEntity` (JSONB baseline/objectives/gap/MECE/SOP), `AlignmentNodeEntity` (self-referential tree), `PivotSignalEntity`
- [x] Full REST API: Plans CRUD, Alignment tree CRUD, Status propagation, BSC Scorecard, S&OP 68/27/5 validation, Pivot signals
- [x] Flyway migration `V1__vstrategy_init.sql` — 3 tables + indexes + demo seed (Q1-2026 plan with full alignment tree)
- [x] `manifest.json` cho vStrategy (permissions, events published/subscribed)
- [x] Gateway routes: `/api/v1/vstrategy/**` + `/vstrategy/**` → vstrategy:8081
- [x] Thêm vstrategy service vào `docker-compose.yml`
- [x] vKernel `V5__register_vstrategy.sql` — Auto-register in app registry + inject permissions
- [x] Dark-themed HTML dashboard (`static/index.html`) — BSC bars, alignment tree, S&OP table, MECE cards, pivot signals
- [x] 20 integration tests (`StrategyApiTests.java`) — all passing
- [x] `Makefile` — `make {help|dev|up|down|test|clean}` — replaces `run.sh`
- [x] PRD synced to `docs/prd/vstrategy-prd.md`

### Step 5b: Python Rewrite (Java → Python/FastAPI) ✅ DONE

- [x] Rewrite backend: Python 3.12 / FastAPI / SQLAlchemy (async) / Alembic
- [x] `FlexibleJSON` TypeDecorator — JSONB on PostgreSQL, JSON on SQLite (test portability)
- [x] Lazy engine creation in `database.py` — no asyncpg required at import time
- [x] TypeScript frontend: `types.ts`, `api.ts`, `renderers.ts`, `main.ts` + IIFE bundler
- [x] 19 integration tests (pytest-asyncio + httpx + aiosqlite) — all passing
- [x] Docker multi-stage build: Node 20-alpine (TS) + Python 3.12-slim (runtime)
- [x] `Makefile` `test-strategy` target — pytest runner for vStrategy (replaces `run_python_test()`)

## ~~Step 6: gRPC Internal Communication~~ ✅ DONE

- [x] Proto definitions cho internal IPC — `vkernel/src/main/proto/kernel.proto` (proto3, `KernelService`: Ping / PublishEvent / GetInstalledApps)
- [x] gRPC server trong vKernel — `KernelGrpcService.java` (`@GrpcService`, port 9090), `pom.xml` updated (grpc-server-spring-boot-starter, protobuf-maven-plugin)
- [x] gRPC client trong vStrategy — `vstrategy/app/grpc_client.py` (KernelGrpcClient, graceful degradation), stubs auto-generated in Dockerfile
- [x] docker-compose port 9090 exposed, `KERNEL_GRPC_HOST`/`KERNEL_GRPC_PORT` env vars wired
- [x] vstrategy `main.py` lifespan pings Kernel gRPC on startup

## ~~Step 7: Auth Hardening~~ ✅ DONE

- [x] Refresh token rotation — opaque token, SHA-256 hash stored, 30-day expiry, reuse-attack detection (`RefreshTokenEntity`, `RefreshTokenService`, `V6__auth_hardening.sql`)
- [x] `POST /api/v1/auth/refresh` + `POST /api/v1/auth/logout` endpoints
- [x] Rate limiting on auth endpoints — sliding window 10 req/60s per IP (`RateLimitFilter.java`)
- [x] Multi-tenant isolation — `TenantContext` ThreadLocal, `tenant_id` claim in JWT
- [x] OIDC/OAuth2 provider integration (Google, Microsoft, GitHub SSO) — `OidcAuthController.java`, `OidcAccountEntity.java`, V7 migration
- [x] Magic link (passwordless) authentication — `MagicLinkController.java`, `MagicLinkEntity.java`

## Backlog ✅ ALL DONE

- [x] Universal Search (SyR-PLAT-02.02) — PostgreSQL FTS with tsvector + GIN index; `SearchController.java`, `SearchIndexEntity.java`, `GET /api/v1/search?q=...`
- [x] Adaptive UI Shell (SyR-PLAT-04) — Micro-frontend host with sidebar app-switcher, iframe isolation; `AdaptiveShellController.java`, `GET /shell`
- [x] Prometheus metrics — `micrometer-registry-prometheus` wired, `/actuator/prometheus` exposed
- [x] Helm chart cho K8s deployment — `helm/vroute/` (Chart.yaml, values.yaml, deployment/service/secret/ingress/servicemonitor templates)
- [x] CI/CD pipeline (GitHub Actions) — `.github/workflows/ci.yml`: test-vkernel → test-vstrategy → docker-build → push GHCR
- [x] Test optimization — `make test` uses local Maven/Python when available (< 1s/test), Docker fallback with volume cache

## Step 8: Second vApp — vFinacc (SyR-FIN-00 through SyR-FIN-04) ✅ DONE

- [x] PRD & design sheets: `docs/prd/vfinacc-prd.md`, `sheets/vfinacc/{api-contract,acceptance-criteria,data-model}.md`
- [x] Scaffold `vfinacc/` — Python 3.12 / FastAPI (port 8082, shared PostgreSQL DB)
- [x] 5 ORM models: `LedgerEntry` (DRAFT/POSTED), `Transaction` (RAW/MATCHED/RECONCILED), `ReconciliationMatch` (3-way), `CostAllocation` (GROW/RUN/TRANSFORM/GIVE), `ComplianceCheck` (VAT/CIT/THRESHOLD)
- [x] Business logic service.py (~290 lines): Continuous Ledger, Transaction Ingestor, 3-way Reconciliation Engine, Cost Center 68/27/5/0.1 allocation, Tax & Compliance Guard
- [x] Full REST API: 16 endpoints at `/api/v1/vfinacc` (Ledger, Transactions, Reconciliation, Cost Centers, Compliance, Health)
- [x] `manifest.json` — 4 permissions (finance.\*), 4 published events, 2 subscribed events, depends on vstrategy
- [x] Alembic migration `0001_vfinacc_init.py` — 5 tables + indexes + seed data
- [x] vKernel `V8__register_vfinacc.sql` — Auto-register in app registry + inject 4 permissions
- [x] Gateway routes: `/api/v1/vfinacc/**` + `/vfinacc/**` → vfinacc:8082
- [x] Dark-themed HTML dashboard (`static/index.html`) — Ledger, Reconciliation, Cost Centers, Compliance cards
- [x] 25 integration tests (pytest-asyncio + httpx + aiosqlite) — all domains covered
- [x] `Dockerfile` — 2-stage: Node 20-alpine + Python 3.12-slim, port 8082
- [x] Added to `docker-compose.yml`, `Makefile` (`test-finacc` target), `README.md`
