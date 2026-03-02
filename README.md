# vRoute-Open — Corp as Code Platform

> **Composable Enterprise OS** — Hệ điều hành doanh nghiệp tháo lắp đầu tiên tại VN.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: Business Apps (vApps)                              │
│  ♟️ vStrategy │ 💰 vFinacc │ vSales │ vHR │ ...             │
├─────────────────────────────────────────────────────────────┤
│  TIER 2: vKernel Core OS (Java 21 / Spring Boot 3.3)       │
│  ┌──────────┐ ┌─────────┐ ┌───────────┐ ┌──────────────┐   │
│  │ API GW   │ │ IAM/SSO │ │ App Engine│ │ Data Backbone│   │
│  │ (Router) │ │(JWT+OIDC│ │ (Install/ │ │ (JSONB ext)  │   │
│  │          │ │+MagicLk)│ │ Lifecycle)│ │              │   │
│  └──────────┘ └─────────┘ └───────────┘ └──────────────┘   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ Event Bus│ │  Search  │ │ UI Shell │ │   gRPC IPC   │   │
│  │ Pub/Sub  │ │ FTS(PG)  │ │micro-fe  │ │ (port 9090)  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  TIER 3: PostgreSQL 16 │ Redis 7 │ Event Store             │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer    | Technology                                              | Status   |
| -------- | ------------------------------------------------------- | -------- |
| Core OS  | Java 21, Spring Boot 3.3, Spring Cloud GW               | **v1.3** |
| vApps    | Python 3.12 / FastAPI (vStrategy, vFinacc), TS frontend  | **v1.4** |
| Database | PostgreSQL 16, Flyway (kernel) + Alembic (vApps)        | **v1.3** |
| Events   | Pub/Sub (Spring + DB), Redis (infra ready)              | **v1.3** |
| IPC      | gRPC / protobuf3 (vKernel port 9090)                    | **v1.3** |
| Auth     | JWT + OIDC SSO (Google/Microsoft/GitHub) + Magic Link   | **v1.3** |
| Search   | PostgreSQL FTS (tsvector + GIN + ts_rank)               | **v1.3** |
| UI       | Adaptive Shell (micro-frontend host, iframe isolation)  | **v1.3** |
| Metrics  | Micrometer + Prometheus (actuator endpoint)             | **v1.3** |
| CI/CD    | GitHub Actions (test → docker-build → GHCR push)        | **v1.3** |
| Tests    | JUnit 5 + MockMvc (vKernel), pytest-asyncio (vStrategy, vFinacc) | **v1.4** |
| Deploy   | Docker Compose (dev), Helm chart (prod K8s)             | **v1.3** |

## Project Structure

```
vRoute-Open/
├── Makefile                          # make {help|dev|up|down|test|clean}
├── docker-compose.yml                # PostgreSQL + Redis + vKernel + vStrategy + vFinacc
├── .env                              # Dev environment vars
├── helm/                             # Kubernetes Helm chart
│   └── vroute/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/                # deployment, service, secret, ingress, servicemonitor
├── docs/prd/
│   ├── vstrategy-prd.md              # vStrategy PRD (synced from Google Docs)
│   ├── vfinacc-prd.md                # vFinacc PRD (SyR-FIN-00 through SyR-FIN-04)
│   └── vkernel-prd.md                # vKernel PRD (SyR-PLAT-00 through SyR-PLAT-05)
├── vkernel/                          # Core OS (Java 21 / Spring Boot 3.3.7)
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/java/com/abivin/vkernel/
│       ├── VKernelApplication.java       # 0.0.0-BOOT
│       ├── DashboardController.java      # 0.0.0-DASH — HTML dashboard (4 pages)
│       ├── AdaptiveShellController.java  # 4.0.0 — Micro-frontend host (SyR-PLAT-04)
│       ├── g0_engine/                    # SyR-PLAT-00: App Engine
│       │   ├── AppRegistryController.java    # 0.0.0
│       │   ├── AppRegistryEntity.java        # 0.1.0
│       │   ├── AppLifecycleService.java      # 0.3.0
│       │   ├── ManifestModel.java            # 0.2.0
│       │   └── PermissionEntity.java         # 1.2.0
│       ├── g1_iam/                       # SyR-PLAT-01: IAM (JWT + OIDC + Magic Link)
│       │   ├── SecurityConfig.java           # 1.0.0
│       │   ├── AuthController.java           # 1.0.1
│       │   ├── JwtProvider.java              # 1.0.2
│       │   ├── UserEntity.java               # 1.1.0
│       │   ├── RefreshTokenEntity.java       # 1.4.0 — Opaque refresh tokens
│       │   ├── RefreshTokenService.java      # 1.5.0 — Rotation + reuse detection
│       │   ├── RateLimitFilter.java          # 1.3.0 — Sliding window rate limiter
│       │   ├── TenantContext.java            # 1.2.1 — Multi-tenant ThreadLocal
│       │   ├── OidcAccountEntity.java        # 1.6.0 — OIDC linked accounts
│       │   ├── OidcAuthController.java       # 1.6.1 — Google/Microsoft/GitHub SSO
│       │   ├── MagicLinkEntity.java          # 1.7.0 — Passwordless auth tokens
│       │   └── MagicLinkController.java      # 1.7.1 — Magic link send/verify
│       ├── g2_data/                      # SyR-PLAT-02: Data Backbone
│       │   ├── TenantEntity.java             # 2.0.0
│       │   ├── StakeholderEntity.java        # 2.0.1
│       │   ├── CurrencyEntity.java           # 2.0.2
│       │   ├── CountryEntity.java            # 2.0.3
│       │   └── DataExtensionController.java  # 2.1.0
│       ├── g3_event/                     # SyR-PLAT-03: Event Bus
│       │   ├── EventLogEntity.java           # 3.0.0
│       │   ├── SubscriptionEntity.java       # 3.0.1
│       │   ├── KernelEvent.java              # 3.1.1
│       │   ├── EventBusService.java          # 3.1.0
│       │   └── EventBusController.java       # 3.2.0
│       ├── g4_grpc/                      # SyR-PLAT-04: gRPC IPC
│       │   └── KernelGrpcService.java        # 4.0.0
│       └── g5_search/                    # SyR-PLAT-02.02: Universal Search
│           ├── SearchIndexEntity.java        # 5.0.0 — FTS index (tsvector)
│           └── SearchController.java         # 5.1.0 — GET /api/v1/search
├── vstrategy/                        # vApp: S2P2R Strategy Module (Python 3.12 / FastAPI)
│   ├── requirements.txt              # Python dependencies
│   ├── pyproject.toml                # Project config + pytest settings
│   ├── Dockerfile                    # Multi-stage: Node (TS build) + Python runtime
│   ├── manifest.json                 # vApp manifest (for App Engine)
│   ├── alembic.ini                   # Alembic migration config
│   ├── alembic/                      # Database migrations
│   │   └── versions/
│   │       └── 0001_vstrategy_init.py    # Schema + seed data
│   ├── protos/                       # Proto files for gRPC stub generation
│   │   └── kernel.proto
│   ├── app/                          # FastAPI application
│   │   ├── config.py                     # Pydantic Settings
│   │   ├── database.py                   # Async SQLAlchemy engine
│   │   ├── models.py                     # ORM: Plan, AlignmentNode, PivotSignal
│   │   ├── schemas.py                    # Pydantic DTOs
│   │   ├── service.py                    # Business logic (vstrategy.1.0)
│   │   ├── routes.py                     # REST API endpoints (vstrategy.2.0)
│   │   ├── grpc_client.py                # KernelGrpcClient (IPC, step 6)
│   │   ├── grpc/                         # Auto-generated stubs (Docker build)
│   │   └── main.py                       # FastAPI app entry
│   ├── frontend/                     # TypeScript frontend
│   │   ├── src/                          # TS source (types, api, renderers, main)
│   │   └── scripts/bundle.js             # TS→IIFE bundler
│   ├── static/index.html             # Dashboard (dark theme)
│   └── tests/
│       └── test_strategy_api.py      # 19 integration tests (pytest-asyncio)
├── vfinacc/                          # vApp: vFinance R2R Module (Python 3.12 / FastAPI)
│   ├── requirements.txt              # Python dependencies
│   ├── pyproject.toml                # Project config + pytest settings
│   ├── Dockerfile                    # Multi-stage: Node (TS build) + Python runtime
│   ├── manifest.json                 # vApp manifest (for App Engine)
│   ├── alembic.ini                   # Alembic migration config
│   ├── alembic/                      # Database migrations
│   │   └── versions/
│   │       └── 0001_vfinacc_init.py      # Schema + seed data (5 tables)
│   ├── app/                          # FastAPI application
│   │   ├── config.py                     # Pydantic Settings
│   │   ├── database.py                   # Async SQLAlchemy engine
│   │   ├── models.py                     # ORM: LedgerEntry, Transaction, ReconciliationMatch, CostAllocation, ComplianceCheck
│   │   ├── schemas.py                    # Pydantic DTOs
│   │   ├── service.py                    # Business logic (5 SyR-FIN requirements)
│   │   ├── routes.py                     # REST API endpoints (/api/v1/vfinacc)
│   │   ├── grpc_client.py                # KernelGrpcClient (IPC)
│   │   └── main.py                       # FastAPI app entry
│   ├── static/index.html             # Dashboard (dark theme)
│   └── tests/
│       └── test_finance_api.py       # 25 integration tests (pytest-asyncio)
├── CHANGELOG.md
└── TODO.md
```

## Governance Numbering

| Package     | SyR Mapping    | Description                       |
| ----------- | -------------- | --------------------------------- |
| `g0_engine` | SyR-PLAT-00    | App Engine (Install/Lifecycle)    |
| `g1_iam`    | SyR-PLAT-01    | IAM (JWT + OIDC SSO + Magic Link) |
| `g2_data`   | SyR-PLAT-02    | Data Backbone + JSONB ext         |
| `g3_event`  | SyR-PLAT-03    | Event Bus & Pub/Sub               |
| `g4_grpc`   | SyR-PLAT-04    | gRPC Internal IPC                 |
| `g5_search` | SyR-PLAT-02.02 | Universal Search (FTS)            |

**Java naming rule**: Tên file CamelCase chuẩn. Mỗi class BẮT BUỘC có `@GovernanceID x.y.z` trong Javadoc.

## Quick Start

```bash
# Start entire platform (PostgreSQL + Redis + vKernel + vStrategy + vFinacc)
make up

# Open vStrategy dashboard
# http://localhost:8081

# Open vFinacc dashboard
# http://localhost:8082

# vKernel APIs
curl http://localhost:8080/api/v1/apps
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"123456"}'

# Auth flow (refresh tokens)
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"123456"}'  # returns access_token + refresh_token
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<token>"}'

# OIDC SSO (Google/Microsoft/GitHub)
curl http://localhost:8080/api/v1/auth/oidc/google        # returns authorization_url
curl http://localhost:8080/api/v1/auth/oidc/microsoft      # returns authorization_url

# Magic Link (passwordless)
curl -X POST http://localhost:8080/api/v1/auth/magic-link \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com"}'                         # returns magic_link URL

# Universal Search
curl "http://localhost:8080/api/v1/search?q=vietnam&type=STAKEHOLDER&limit=10"

# Adaptive UI Shell
# http://localhost:8080/shell                              # app launcher
# http://localhost:8080/shell/com.vcorp.vstrategy          # load vStrategy

# Prometheus metrics
curl http://localhost:8080/actuator/prometheus

# gRPC (port 9090) — use grpcurl or a gRPC client
# grpcurl -plaintext localhost:9090 kernel.KernelService/Ping

# vStrategy APIs
curl http://localhost:8081/api/v1/vstrategy/plans
curl http://localhost:8081/api/v1/vstrategy/health

# vFinacc APIs
curl http://localhost:8082/api/v1/vfinacc/ledger
curl http://localhost:8082/api/v1/vfinacc/transactions
curl http://localhost:8082/api/v1/vfinacc/reconciliation
curl http://localhost:8082/api/v1/vfinacc/cost-centers
curl http://localhost:8082/api/v1/vfinacc/compliance
curl http://localhost:8082/api/v1/vfinacc/health

# Run all tests
make test

# Stop
make down
```

## Kubernetes Deployment (Helm)

```bash
# Install with Helm
helm install vroute ./helm/vroute \
  --set vkernel.env.JWT_SECRET="your-production-secret-32-chars" \
  --set postgresql.password="strong-db-password"

# Upgrade
helm upgrade vroute ./helm/vroute

# Uninstall
helm uninstall vroute
```

## Organizational Blocks (vApps — planned)

```
├── 1-Back-Office-Block/              # Khối Hành chính
│   ├── 1.1-IT-Department/
│   ├── 1.2-Finance-Accounting-Admin/
│   ├── 1.3-HR/
│   └── 1.4-Procurement/
├── 2-Production-Block/               # Khối Sản xuất
│   ├── 3.1-Product-Design/
│   ├── 3.2-Product-Development/
│   └── 3.3-Product-Operation/
└── 3-Front-Office-Block/             # Khối Kinh doanh
    ├── 2.1-Marketing/
    ├── 2.2-Business-Development/
    └── 2.3-Account-Management/
```
