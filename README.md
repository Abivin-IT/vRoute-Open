# vRoute-Open — Corp as Code Platform

> **Composable Enterprise OS** — Hệ điều hành doanh nghiệp tháo lắp đầu tiên tại VN.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: Business Apps (vApps)                              │
│  ♟️ vStrategy │ 💰 vFinacc │ 🔬 vDesign │ 📢 vMarketing │ …  │
├─────────────────────────────────────────────────────────────┤
│  TIER 1.5: System Utilities (6)                             │
│  🏪 App Store│ ⚙ Settings │ 🗃 vData   │ ⚡ vFlow        │   │
│  🔒 vAudit   │ 📈 vMonitor│            │                 │   │
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

| Layer    | Technology                                                                                | Status   |
| -------- | ----------------------------------------------------------------------------------------- | -------- |
| Core OS  | Java 21, Spring Boot 3.3, Spring Cloud GW                                                 | **v1.8** |
| vApps    | Python 3.12 / FastAPI (vStrategy, vFinacc, vDesign Physical, vMarketing Org), TS frontend | **v1.7** |
| Database | PostgreSQL 16, Flyway (kernel) + Alembic (vApps)                                          | **v1.3** |
| Events   | Pub/Sub (Spring + DB), Redis (infra ready)                                                | **v1.3** |
| IPC      | gRPC / protobuf3 (vKernel port 9090)                                                      | **v1.3** |
| Auth     | JWT + OIDC SSO (Google/Microsoft/GitHub) + Magic Link                                     | **v1.3** |
| Search   | PostgreSQL FTS (tsvector + GIN + ts_rank)                                                 | **v1.3** |
| UI       | Adaptive Shell (micro-frontend host, iframe isolation)                                    | **v1.3** |
| Metrics  | Micrometer + Prometheus (actuator endpoint)                                               | **v1.3** |
| CI/CD    | GitHub Actions (test → docker-build → GHCR push)                                          | **v1.3** |
| Tests    | JUnit 5 + MockMvc (vKernel), pytest-asyncio (vStrategy, vFinacc)                          | **v1.4** |
| Deploy   | Docker Compose (dev), Helm chart (prod K8s)                                               | **v1.3** |

## Project Structure

> **Folder numbering:** lower prefix = higher importance. `01-` = core OS, `02-`/`03-` = vApps, `80-` = infra, `90-` = docs.

```
vRoute-Open/
├── 00-design/                        # Design artifacts
│   ├── docs/                         #   PRD documents
│   │   ├── vkernel-prd.md            #     Platform requirements (SyR-PLAT-00→05)
│   │   ├── vstrategy-prd.md          #     Strategy requirements (SyR-STR-00→04)
│       ├── vfinacc-prd.md            #     Finance requirements (SyR-FIN-00→04)
│       ├── vdesign-physical-prd.md   #     Physical design requirements (SyR-PHY-00→04)
│       └── vmarketing-org-prd.md     #     Marketing requirements (SyR-MKT-ORG-00→04)
│   └── sheets/                       #   Data tables & contracts
│       ├── api-contract-summary.md
│       ├── acceptance-criteria.md
│       └── vfinacc/                  #     vFinacc-specific sheets
├── 01-vkernel/                       # Core OS (Java 21 / Spring Boot 3.3)
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/java/com/abivin/vkernel/
│       ├── g0_engine/                #   SyR-PLAT-00: App Engine
│       ├── g1_iam/                   #   SyR-PLAT-01: IAM (JWT + OIDC + Magic Link)
│       ├── g2_data/                  #   SyR-PLAT-02: Data Backbone + JSONB
│       ├── g3_event/                 #   SyR-PLAT-03: Event Bus & Pub/Sub
│       ├── g4_grpc/                  #   SyR-PLAT-04: gRPC IPC (port 9090)
│       └── g5_search/               #   SyR-PLAT-02.02: Universal Search (FTS)
├── 02-vstrategy/                     # vApp: S2P2R Strategy (Python 3.12 / FastAPI)
│   ├── app/                          #   FastAPI application
│   ├── frontend/                     #   TypeScript frontend
│   ├── tests/                        #   19 integration tests (pytest-asyncio)
│   ├── alembic/                      #   Database migrations
│   ├── manifest.json                 #   vApp manifest
│   └── Dockerfile
├── 03-vfinacc/                       # vApp: Finance R2R (Python 3.12 / FastAPI)
│   ├── app/                          #   FastAPI application
│   ├── frontend/                     #   TypeScript frontend
│   ├── tests/                        #   25 integration tests (pytest-asyncio)
│   ├── alembic/                      #   Database migrations
│   ├── manifest.json                 #   vApp manifest
│   └── Dockerfile
├── 04-vdesign-physical/              # vApp: Physical Design I2S (Python 3.12 / FastAPI)
│   ├── app/                          #   FastAPI application
│   ├── frontend/                     #   TypeScript frontend
│   ├── tests/                        #   35 integration tests (pytest-asyncio)
│   ├── alembic/                      #   Database migrations
│   ├── manifest.json                 #   vApp manifest
│   └── Dockerfile
├── 05-vmarketing-org/                # vApp: Marketing M2L ABM Engine (Python 3.12 / FastAPI)
│   ├── app/                          #   FastAPI application
│   ├── frontend/                     #   TypeScript frontend
│   ├── tests/                        #   28 integration tests (pytest-asyncio)
│   ├── alembic/                      #   Database migrations
│   ├── manifest.json                 #   vApp manifest
│   └── Dockerfile
├── 80-deploy/                        # Deployment infrastructure
│   ├── docker-compose.yml            #   Dev environment (all services)
│   └── helm/vroute/                  #   Kubernetes Helm chart
├── 90-guide/                         # Documentation
│   ├── user/README.md                #   End-user guide
│   └── developer/README.md           #   Developer / contributor guide
├── .github/workflows/ci.yml         # CI/CD pipeline
├── Makefile                          # make {help|dev|up|down|test|clean}
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
# Start entire platform (PostgreSQL + Redis + vKernel + vStrategy + vFinacc + vDesign Physical + vMarketing Org)
make up

# Open vStrategy dashboard (proxied via vKernel gateway)
# http://localhost:8080/vstrategy/

# Open vFinacc dashboard (proxied via vKernel gateway)
# http://localhost:8080/vfinacc/

# Open vDesign Physical dashboard (proxied via vKernel gateway)
# http://localhost:8080/vdesign-physical/

# Open vMarketing Org dashboard (proxied via vKernel gateway)
# http://localhost:8080/vmarketing-org/

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

# vStrategy APIs (all through vKernel gateway :8080)
curl http://localhost:8080/api/v1/vstrategy/plans
curl http://localhost:8080/api/v1/vstrategy/health

# vFinacc APIs (all through vKernel gateway :8080)
curl http://localhost:8080/api/v1/vfinacc/ledger
curl http://localhost:8080/api/v1/vfinacc/transactions
curl http://localhost:8080/api/v1/vfinacc/reconciliation
curl http://localhost:8080/api/v1/vfinacc/cost-centers
curl http://localhost:8080/api/v1/vfinacc/compliance
curl http://localhost:8080/api/v1/vfinacc/health

# vDesign Physical APIs (all through vKernel gateway :8080)
curl http://localhost:8080/api/v1/vdesign-physical/golden-samples
curl http://localhost:8080/api/v1/vdesign-physical/materials
curl http://localhost:8080/api/v1/vdesign-physical/prototypes
curl http://localhost:8080/api/v1/vdesign-physical/lab-tests
curl http://localhost:8080/api/v1/vdesign-physical/lab-tests/summary
curl http://localhost:8080/api/v1/vdesign-physical/handover-kits
curl http://localhost:8080/api/v1/vdesign-physical/health

# vMarketing Org APIs (all through vKernel gateway :8080)
curl http://localhost:8080/api/v1/vmarketing-org/campaigns
curl http://localhost:8080/api/v1/vmarketing-org/tracking-events
curl http://localhost:8080/api/v1/vmarketing-org/segments
curl http://localhost:8080/api/v1/vmarketing-org/assets
curl http://localhost:8080/api/v1/vmarketing-org/leads
curl http://localhost:8080/api/v1/vmarketing-org/health

# Run all tests
make test

# Stop
make down
```

## Kubernetes Deployment (Helm)

See [80-deploy/README.md](80-deploy/README.md) for full deployment guide (local / staging / production).

```bash
# Staging (single-server, branch: staging)
make up-staging

# Production (K8s cluster, branch: main)
helm upgrade --install vroute ./80-deploy/helm/vroute \
  -f ./80-deploy/helm/vroute/values-prod.yaml \
  --set ingress.host="$PROD_DOMAIN" \
  --set postgresql.password="$DB_PASS" \
  --set vkernel.env.JWT_SECRET="$JWT_SECRET" \
  -n vroute --create-namespace
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
