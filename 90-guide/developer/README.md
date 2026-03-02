# vRoute-Open — Developer Guide

> Last updated: 2026-03-02 | Platform version: 1.5.0

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [How to Add a New vApp](#how-to-add-a-new-vapp)
- [Coding Standards](#coding-standards)
- [Testing Strategy](#testing-strategy)
- [Database \& Migrations](#database--migrations)
- [gRPC IPC](#grpc-ipc)
- [Event Bus](#event-bus)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: Business Apps (vApps)                              │
│  ♟️ 02-vstrategy │ 💰 03-vfinacc │ next: vSales, vHR …     │
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

**Key principles:**

- **Kernel owns shared concerns** — auth, routing, events, data, search
- **vApps are autonomous** — own DB tables, own migrations, own tech stack
- **Communication via contract** — REST (gateway), gRPC (IPC), Event Bus (pub/sub)
- **Folder numbering** — lower prefix = higher importance (01 > 02 > 03)

---

## Getting Started

### Prerequisites

| Tool                    | Version | Purpose                    |
| ----------------------- | ------- | -------------------------- |
| Docker Desktop          | 24+     | Container runtime          |
| Git                     | 2.40+   | Version control            |
| Make (GNU)              | 4.0+    | Build automation           |
| Java 21 (optional)      | 21 LTS  | Local vKernel development  |
| Python 3.12+ (optional) | 3.12+   | Local vApp development     |
| Node.js 20+ (optional)  | 20 LTS  | TypeScript frontend builds |

### Quick Setup

```bash
# 1. Clone the repo
git clone https://github.com/Abivin-IT/vRoute-Open.git
cd vRoute-Open

# 2. Copy environment file
cp .env.example .env

# 3. Start everything (builds Docker images + starts services)
make up

# 4. Verify
curl http://localhost:8080/api/v1/apps                    # should list installed apps
curl http://localhost:8080/api/v1/vstrategy/health        # via gateway
curl http://localhost:8080/api/v1/vfinacc/health          # via gateway

# 5. Run all tests
make test
```

### Local Development (without Docker)

```bash
# Python vApps
python -m venv .venv
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r 02-vstrategy/requirements.txt
pip install -r 03-vfinacc/requirements.txt

# Run tests locally (fastest)
cd 02-vstrategy && python -m pytest tests/ -v
cd 03-vfinacc && python -m pytest tests/ -v

# Java vKernel (requires local Maven + JDK 21)
cd 01-vkernel && mvn test
```

---

## Project Structure

```
vRoute-Open/
├── 00-design/                    # Design artifacts
│   ├── docs/                     #   PRD documents
│   │   ├── vkernel-prd.md        #     Platform requirements (SyR-PLAT-00→05)
│   │   ├── vstrategy-prd.md      #     Strategy requirements (SyR-STR-00→04)
│   │   └── vfinacc-prd.md        #     Finance requirements (SyR-FIN-00→04)
│   └── sheets/                   #   Data tables & contracts
│       ├── api-contract-summary.md
│       ├── acceptance-criteria.md
│       ├── data-model.md (vfinacc/)
│       └── ...
├── 01-vkernel/                   # Core OS (Java 21 / Spring Boot)
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/java/com/abivin/vkernel/
│       ├── g0_engine/            #   App Engine (SyR-PLAT-00)
│       ├── g1_iam/               #   IAM (SyR-PLAT-01)
│       ├── g2_data/              #   Data Backbone (SyR-PLAT-02)
│       ├── g3_event/             #   Event Bus (SyR-PLAT-03)
│       ├── g4_grpc/              #   gRPC IPC (SyR-PLAT-04)
│       └── g5_search/            #   Universal Search (SyR-PLAT-02.02)
├── 02-vstrategy/                 # vApp: Strategy (Python 3.12 / FastAPI)
│   ├── app/                      #   FastAPI application
│   ├── frontend/                 #   TypeScript frontend
│   ├── tests/                    #   pytest-asyncio tests
│   ├── alembic/                  #   Database migrations
│   ├── manifest.json             #   vApp manifest
│   └── Dockerfile
├── 03-vfinacc/                   # vApp: Finance (Python 3.12 / FastAPI)
│   ├── app/                      #   FastAPI application
│   ├── tests/                    #   pytest-asyncio tests
│   ├── alembic/                  #   Database migrations
│   ├── manifest.json             #   vApp manifest
│   └── Dockerfile
├── 80-deploy/                    # Deployment infrastructure
│   ├── docker-compose.yml        #   Dev environment (PostgreSQL + Redis + all services)
│   └── helm/vroute/              #   Kubernetes Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── 90-guide/                     # Documentation
│   ├── user/README.md            #   End-user guide
│   └── developer/README.md       #   This file
├── .github/workflows/ci.yml     # CI/CD pipeline
├── Makefile                      # Build automation
├── CHANGELOG.md                  # Version history
└── TODO.md                       # Roadmap
```

### Folder Numbering Convention

| Prefix | Category                   | Examples                   |
| ------ | -------------------------- | -------------------------- |
| `00-`  | Design (docs/sheets)       | `00-design/`               |
| `01-`  | Core OS (highest priority) | `01-vkernel/`              |
| `02-`  | First vApp                 | `02-vstrategy/`            |
| `03-`  | Second vApp                | `03-vfinacc/`              |
| `04-`… | Future vApps               | `04-vsales/`, `05-vhr/`, … |
| `80-`  | Deployment infra           | `80-deploy/`               |
| `90-`  | Guides & docs              | `90-guide/`                |

**Rule:** Lower number = higher importance. Future vApps increment from `04-`.

---

## How to Add a New vApp

Adding a new vApp requires **7 steps**. Use `03-vfinacc/` as a reference template.

### Step 1: PRD & Design

```bash
# Create PRD
touch 00-design/docs/vnewapp-prd.md

# Create data sheets
mkdir -p 00-design/sheets/vnewapp
touch 00-design/sheets/vnewapp/{api-contract,acceptance-criteria,data-model}.md
```

### Step 2: Scaffold the App

```bash
mkdir -p 04-vnewapp/{app,tests,alembic/versions,static}

# Copy boilerplate from vfinacc
cp 03-vfinacc/requirements.txt 04-vnewapp/
cp 03-vfinacc/pyproject.toml 04-vnewapp/
cp 03-vfinacc/alembic.ini 04-vnewapp/
cp 03-vfinacc/alembic/env.py 04-vnewapp/alembic/
cp 03-vfinacc/alembic/script.py.mako 04-vnewapp/alembic/
cp 03-vfinacc/Dockerfile 04-vnewapp/
```

Create these files:

| File                 | Purpose                                |
| -------------------- | -------------------------------------- |
| `app/__init__.py`    | Package marker                         |
| `app/config.py`      | Pydantic Settings (PORT, DATABASE_URL) |
| `app/database.py`    | Async SQLAlchemy engine                |
| `app/models.py`      | ORM models (extend `Base`)             |
| `app/schemas.py`     | Pydantic request/response DTOs         |
| `app/service.py`     | Business logic                         |
| `app/routes.py`      | FastAPI Router at `/api/v1/vnewapp`    |
| `app/main.py`        | FastAPI app entry + lifespan           |
| `app/grpc_client.py` | KernelGrpcClient (optional)            |
| `manifest.json`      | vApp manifest for App Engine           |
| `static/index.html`  | Dashboard UI                           |
| `tests/conftest.py`  | Test fixtures (SQLite in-memory)       |
| `tests/test_*.py`    | Integration tests                      |

### Step 3: Create manifest.json

```json
{
  "app": {
    "id": "com.vcorp.vnewapp",
    "name": "vNewApp",
    "version": "1.0.0",
    "min_kernel_version": "0.4.0"
  },
  "dependencies": [
    { "app_id": "com.vcorp.kernel.settings", "version_range": "^1.0.0" }
  ],
  "permissions": [
    {
      "code": "newapp.view",
      "name": "View",
      "category": "newapp",
      "default_roles": ["CEO"]
    }
  ],
  "events": {
    "published": ["NEWAPP_EVENT"],
    "subscribed": []
  }
}
```

### Step 4: Register in vKernel

Create a Flyway migration: `01-vkernel/src/main/resources/db/migration/V{N}__register_vnewapp.sql`

```sql
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by)
VALUES ('com.vcorp.vnewapp', 'vNewApp', '1.0.0', '🆕', 'ACTIVE', '{...}', 'system');

INSERT INTO kernel_permissions (app_id, permission_code, name, description, category)
VALUES ('com.vcorp.vnewapp', 'newapp.view', 'View', 'View access', 'newapp');
```

### Step 5: Add Gateway Routes

In `01-vkernel/src/main/resources/application.yml`, add:

```yaml
- id: vnewapp-route
  uri: http://vnewapp:PORT
  predicates:
    - Path=/api/v1/vnewapp/**
- id: vnewapp-ui
  uri: http://vnewapp:PORT
  predicates:
    - Path=/vnewapp/**
```

### Step 6: Add to Infrastructure

**docker-compose.yml** (`80-deploy/docker-compose.yml`):

```yaml
vnewapp:
  build:
    context: ../04-vnewapp
    dockerfile: Dockerfile
  ports:
    - "PORT:PORT"
  environment:
    DATABASE_URL: postgresql://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
  depends_on:
    postgres:
      condition: service_healthy
```

**Makefile** — add directory variable + test target:

```makefile
VNEWAPP_DIR := $(ROOT)/04-vnewapp

test-newapp:
	$(call pytest,$(VNEWAPP_DIR))
```

**CI/CD** (`.github/workflows/ci.yml`) — add test job + push job.

### Step 7: Update Documentation

- `README.md` — add to project structure and quick start
- `CHANGELOG.md` — document the new version
- `TODO.md` — add step with all tasks checked

---

## Coding Standards

### Java (vKernel — `01-vkernel/`)

| Rule                   | Example                                       |
| ---------------------- | --------------------------------------------- |
| Governance ID required | `/** @GovernanceID 1.0.0 */`                  |
| Package naming         | `g{N}_{domain}` (e.g., `g0_engine`, `g1_iam`) |
| CamelCase files        | `AppRegistryEntity.java`                      |
| No `@Autowired` fields | Use constructor injection                     |
| Tests                  | JUnit 5 + MockMvc + `@SpringBootTest`         |

### Python (vApps — `02-vstrategy/`, `03-vfinacc/`)

| Rule                       | Example                                    |
| -------------------------- | ------------------------------------------ |
| Async everywhere           | `async def`, `AsyncSession`, `await`       |
| Pydantic v2 DTOs           | `class Out(BaseModel): model_config = ...` |
| FlexibleJSON TypeDecorator | JSONB on PostgreSQL, JSON on SQLite        |
| Lazy engine creation       | No DB connection at import time            |
| Tests                      | pytest-asyncio + httpx + SQLite in-memory  |
| No unused imports          | Enforced by GitHub Code Quality            |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(vfinacc): implement ledger CRUD endpoints
fix(vkernel): correct gateway route for vfinacc
chore: restructure folders with numbered prefixes
refactor(vstrategy): extract service from routes
test(vfinacc): add compliance check edge cases
docs: update developer guide
```

---

## Testing Strategy

| Layer     | Tool                   | Location               | Speed |
| --------- | ---------------------- | ---------------------- | ----- |
| vKernel   | JUnit 5 + MockMvc + H2 | `01-vkernel/src/test/` | ~3s   |
| vStrategy | pytest-asyncio + httpx | `02-vstrategy/tests/`  | ~0.5s |
| vFinacc   | pytest-asyncio + httpx | `03-vfinacc/tests/`    | ~0.7s |
| Docker    | `docker compose build` | CI/CD                  | ~2min |

### Run Tests

```bash
make test              # all tests (vKernel + vStrategy + vFinacc)
make test-kernel       # JUnit 5 only
make test-strategy     # pytest only (vStrategy)
make test-finacc       # pytest only (vFinacc)
make test-app-vnewapp  # generic: any vApp by folder name
```

### Test Priority

1. **Unit tests** — business logic in `service.py` / `*Service.java`
2. **Integration tests** — full API round-trip (create → read → update → verify)
3. **Edge cases** — invalid input, state transitions (DRAFT → POSTED), permission checks
4. **Docker build** — ensures Dockerfile and compose work end-to-end

---

## Database & Migrations

### Shared PostgreSQL

All services share one PostgreSQL 16 instance. Each vApp prefixes its tables:

| vApp      | Table prefix  | Migration tool | Version table               |
| --------- | ------------- | -------------- | --------------------------- |
| vKernel   | `kernel_*`    | Flyway         | `flyway_schema_history`     |
| vStrategy | `vstrategy_*` | Alembic        | `alembic_version_vstrategy` |
| vFinacc   | `vfinacc_*`   | Alembic        | `alembic_version_vfinacc`   |

### Creating a Migration

**Flyway (vKernel):**

```sql
-- V{N}__description.sql
CREATE TABLE kernel_new_table ( ... );
```

**Alembic (vApps):**

```bash
cd 03-vfinacc
alembic revision --autogenerate -m "add new column"
alembic upgrade head
```

### FlexibleJSON Pattern

All vApps use a `FlexibleJSON` TypeDecorator that automatically uses:

- **JSONB** on PostgreSQL (production) — supports indexing, containment queries
- **JSON** on SQLite (tests) — lightweight, fast in-memory testing

---

## gRPC IPC

vKernel exposes `KernelService` on port 9090:

| RPC Method         | Purpose                    |
| ------------------ | -------------------------- |
| `Ping`             | Health check / heartbeat   |
| `PublishEvent`     | Publish event to Event Bus |
| `GetInstalledApps` | List registered apps       |

### Python Client (vApps)

```python
from app.grpc_client import KernelGrpcClient

client = KernelGrpcClient()
await client.connect()
await client.ping()       # Returns "pong" or None if unreachable
await client.close()
```

The client **degrades gracefully** — if gRPC is unreachable, it logs a warning and continues. No import-time errors.

---

## Event Bus

### Publishing Events

```bash
curl -X POST http://localhost:8080/api/v1/events/publish \
  -H "Content-Type: application/json" \
  -d '{"type":"TRANSACTION_POSTED","source":"vfinacc","payload":{...}}'
```

### Standard Event Types

| Event                  | Source    | Description                 |
| ---------------------- | --------- | --------------------------- |
| `APP_INSTALLED`        | vKernel   | New vApp installed          |
| `APP_UNINSTALLED`      | vKernel   | vApp uninstalled            |
| `OKR_STATUS_CHANGED`   | vStrategy | OKR status updated          |
| `PIVOT_SIGNAL_RAISED`  | vStrategy | Threshold pivot alert       |
| `TRANSACTION_POSTED`   | vFinacc   | Journal entry posted        |
| `BUDGET_OVERRUN_ALERT` | vFinacc   | Cost center over budget     |
| `RECON_COMPLETED`      | vFinacc   | Reconciliation run finished |
| `COMPLIANCE_VIOLATION` | vFinacc   | Tax/compliance check failed |

---

## CI/CD Pipeline

```
┌──────────────┐   ┌───────────────┐   ┌───────────────┐   ┌────────────┐   ┌─────────────┐
│ test-vkernel │   │ test-vstrategy│   │ test-vfinacc  │   │docker-build│   │ push-images │
│ (JUnit 5)    │──▶│ (pytest)      │──▶│ (pytest)      │──▶│ (compose)  │──▶│ (GHCR)      │
└──────────────┘   └───────────────┘   └───────────────┘   └────────────┘   └─────────────┘
                                                                              main branch only
```

- **Triggers:** push to `main`, any PR to `main`
- **Registry:** GitHub Container Registry (`ghcr.io`)
- **Images:** `vkernel`, `vstrategy`, `vfinacc` — tagged with SHA + `latest`
- **Config:** `.github/workflows/ci.yml`

---

## Deployment

### Development (Docker Compose)

```bash
make up        # start all (80-deploy/docker-compose.yml)
make dev       # foreground mode with live logs
make down      # stop
make logs      # tail logs
```

### Production (Kubernetes / Helm)

```bash
helm install vroute ./80-deploy/helm/vroute \
  --set vkernel.env.JWT_SECRET="production-secret-32-chars-min" \
  --set postgresql.password="strong-password"

helm upgrade vroute ./80-deploy/helm/vroute
helm uninstall vroute
```

Helm chart includes: deployments, services, secrets, ingress (nginx + TLS), ServiceMonitor (Prometheus).

---

## Contributing

### Branch Naming

```
feat/{app}-{description}     # feat/vfinacc-add-budget-alerts
fix/{app}-{description}      # fix/vkernel-gateway-timeout
chore/{description}          # chore/restructure-folders
```

### Pull Request Checklist

- [ ] All tests pass (`make test`)
- [ ] No unused imports (GitHub Code Quality)
- [ ] `CHANGELOG.md` updated with new version entry
- [ ] `README.md` project structure updated (if folder changes)
- [ ] Commit messages follow Conventional Commits
- [ ] New vApp registered in vKernel (Flyway SQL + gateway routes)
- [ ] Docker build verified (`make up`)

### Code Review

All PRs are reviewed by **github-code-quality[bot]** for:

- Unused imports
- Dead code
- Potential bugs
- Style consistency
