# vRoute-Open — User Guide

> Last updated: 2026-03-02 | Platform version: 1.5.0

---

## Table of Contents

1. [What is vRoute-Open?](#what-is-vroute-open)
2. [Accessing the Platform](#accessing-the-platform)
3. [Authentication](#authentication)
4. [Using vKernel (Core OS)](#using-vkernel-core-os)
5. [Using vStrategy](#using-vstrategy)
6. [Using vFinacc](#using-vfinacc)
7. [App Store & Shell](#app-store--shell)
8. [Troubleshooting](#troubleshooting)

---

## What is vRoute-Open?

vRoute-Open is a **Composable Enterprise OS** — a modular platform where each business function (Finance, Strategy, HR, Sales…) runs as an independent **vApp** coordinated by a central **vKernel** core.

Think of it as an operating system for your company:

| Concept            | vRoute Equivalent                                 |
| ------------------ | ------------------------------------------------- |
| OS Kernel          | **vKernel** (API Gateway, IAM, Event Bus)         |
| Installed Apps     | **vApps** (vStrategy, vFinacc, …)                 |
| App Store          | **App Engine** (`/api/v1/apps`)                   |
| File System        | **Data Backbone** (PostgreSQL + JSONB extensions) |
| Search (Spotlight) | **Universal Search** (`Ctrl+K`)                   |

---

## Accessing the Platform

| Service      | URL                                         | Description        |
| ------------ | ------------------------------------------- | ------------------ |
| vKernel      | `http://localhost:8080`                     | Core OS dashboard  |
| App Launcher | `http://localhost:8080/shell`               | Adaptive UI Shell  |
| vStrategy    | `http://localhost:8080/vstrategy/`          | Strategy dashboard |
| vFinacc      | `http://localhost:8080/vfinacc/`            | Finance dashboard  |
| Prometheus   | `http://localhost:8080/actuator/prometheus` | Metrics endpoint   |

### Prerequisites

- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- At least 4 GB RAM allocated to Docker
- Port 8080, 5432, 6379, 9090 free

### Start the Platform

```bash
make up          # builds & starts all services (background)
make logs        # tail real-time logs
make down        # stop everything
```

---

## Authentication

### Register a New Account

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@company.com", "password":"your-password"}'
```

### Login (JWT)

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@company.com", "password":"your-password"}'
# Returns: { "access_token": "...", "refresh_token": "..." }
```

### Refresh Token

```bash
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<your-refresh-token>"}'
```

### SSO (Google / Microsoft / GitHub)

1. Navigate to `GET /api/v1/auth/oidc/google` (or `/microsoft`, `/github`)
2. You receive an `authorization_url` — open it in browser
3. After consent, callback auto-exchanges code for JWT

### Magic Link (Passwordless)

```bash
curl -X POST http://localhost:8080/api/v1/auth/magic-link \
  -H "Content-Type: application/json" \
  -d '{"email":"you@company.com"}'
# Check email for the magic link → auto-login → JWT returned
```

---

## Using vKernel (Core OS)

### Dashboard

Open `http://localhost:8080/dashboard/health` to view:

- **System Health** — uptime, memory, disk, database connectivity
- **Prometheus Metrics** — JVM, HTTP, gRPC counters
- **App Registry** — installed vApps and their status

### Installed Apps

```bash
curl http://localhost:8080/api/v1/apps
```

Returns a list of all registered vApps with status (`ACTIVE` / `INACTIVE`), permissions, and events.

### Universal Search

```bash
curl "http://localhost:8080/api/v1/search?q=vietnam&type=STAKEHOLDER&limit=10"
```

Searches across all indexed entities using PostgreSQL full-text search with ranking.

### Event Bus

```bash
# Publish an event
curl -X POST http://localhost:8080/api/v1/events/publish \
  -H "Content-Type: application/json" \
  -d '{"type":"CUSTOM_EVENT","source":"manual","payload":{"key":"value"}}'

# List event log
curl http://localhost:8080/api/v1/events/log
```

---

## Using vStrategy

**vStrategy** is the S2P2R (Strategy-to-Plan-to-Result) module for corporate strategy execution.

### Dashboard

Open `http://localhost:8080/vstrategy/` for the visual dashboard showing:

- **Balanced Scorecard** — Financial / Customer / Internal / Learning perspectives
- **Alignment Tree** — VISION → BSC → OKR → INITIATIVE → TASK hierarchy
- **S&OP Validation** — 68% GROW / 27% RUN / 5% TRANSFORM ratio check
- **Pivot Signals** — Automated threshold alerts (RUNWAY_SECURITY, GROWTH_MOMENTUM)

### Key API Endpoints

| Action          | Method | Endpoint                                 |
| --------------- | ------ | ---------------------------------------- |
| List plans      | GET    | `/api/v1/vstrategy/plans`                |
| Create plan     | POST   | `/api/v1/vstrategy/plans`                |
| Alignment tree  | GET    | `/api/v1/vstrategy/plans/{id}/tree`      |
| BSC Scorecard   | GET    | `/api/v1/vstrategy/plans/{id}/scorecard` |
| S&OP Validation | GET    | `/api/v1/vstrategy/plans/{id}/sop`       |
| Pivot Signals   | GET    | `/api/v1/vstrategy/signals`              |
| Health          | GET    | `/api/v1/vstrategy/health`               |

---

## Using vFinacc

**vFinacc** is the R2R (Record-to-Report) finance module covering the full accounting cycle.

### Dashboard

Open `http://localhost:8080/vfinacc/` for the finance dashboard showing:

- **Continuous Ledger** — Journal entries with DRAFT/POSTED/FLAGGED/REVERSED states
- **Reconciliation Engine** — 3-way PO ↔ GRN ↔ Invoice matching with confidence scores
- **Cost Center Allocation** — GROW/RUN/TRANSFORM/GIVE budget tracking (68/27/5/0.1 targets)
- **Tax & Compliance Guard** — VAT, CIT, threshold checks with PASS/FLAG/FAIL results

### Key API Endpoints

| Action                 | Method | Endpoint                                 |
| ---------------------- | ------ | ---------------------------------------- |
| List ledger entries    | GET    | `/api/v1/vfinacc/ledger`                 |
| Create draft entry     | POST   | `/api/v1/vfinacc/ledger`                 |
| Post entry (finalize)  | POST   | `/api/v1/vfinacc/ledger/{id}/post`       |
| Ingest transaction     | POST   | `/api/v1/vfinacc/transactions`           |
| Run reconciliation     | POST   | `/api/v1/vfinacc/reconciliation/run`     |
| Reconciliation summary | GET    | `/api/v1/vfinacc/reconciliation/summary` |
| Create cost allocation | POST   | `/api/v1/vfinacc/cost-centers`           |
| Cost center summary    | GET    | `/api/v1/vfinacc/cost-centers/summary`   |
| Run compliance check   | POST   | `/api/v1/vfinacc/compliance/check`       |
| Compliance summary     | GET    | `/api/v1/vfinacc/compliance/summary`     |
| Health                 | GET    | `/api/v1/vfinacc/health`                 |

### Workflow Example: Post a Journal Entry

```bash
# 1. Create a draft ledger entry (all via gateway :8080)
curl -X POST http://localhost:8080/api/v1/vfinacc/ledger \
  -H "Content-Type: application/json" \
  -d '{
    "entry_number": "JE-2026-001",
    "entry_date": "2026-03-02",
    "description": "Office supplies",
    "debit_account": "6100-OPEX",
    "credit_account": "1100-CASH",
    "amount": 500000,
    "currency": "VND"
  }'
# Returns: { "id": "...", "status": "DRAFT", ... }

# 2. Post the entry (DRAFT → POSTED, irreversible)
curl -X POST http://localhost:8080/api/v1/vfinacc/ledger/{id}/post

# 3. Run a compliance check
curl -X POST http://localhost:8080/api/v1/vfinacc/compliance/check \
  -H "Content-Type: application/json" \
  -d '{"ledger_entry_id": "{id}", "check_type": "TAX_VAT"}'
```

---

## App Store & Shell

### Adaptive UI Shell

Open `http://localhost:8080/shell` to access:

- **App Launcher** — grid of all installed vApps
- **Sidebar Navigation** — quick switch between apps
- **Ctrl+K Search** — universal search across all data

Each vApp loads in an isolated iframe — apps cannot interfere with each other.

### Installing Apps via API

```bash
# Install from manifest
curl -X POST http://localhost:8080/api/v1/apps/install \
  -H "Content-Type: application/json" \
  -d @03-vfinacc/manifest.json

# List installed apps
curl http://localhost:8080/api/v1/apps

# Uninstall
curl -X DELETE http://localhost:8080/api/v1/apps/com.vcorp.vfinacc
```

---

## Troubleshooting

| Problem                             | Solution                                              |
| ----------------------------------- | ----------------------------------------------------- |
| Port 8080 already in use            | `make down` first, or change ports in `.env`          |
| Database connection refused         | Wait 10s after `make up` for PostgreSQL to be healthy |
| vApp dashboard shows blank page     | Check `make logs` — may be Alembic migration error    |
| JWT expired                         | Send refresh token to `/api/v1/auth/refresh`          |
| OIDC login fails                    | Ensure `GOOGLE_CLIENT_ID` etc. are set in `.env`      |
| gRPC connection refused             | vKernel gRPC runs on port 9090 — check `make logs`    |
| `make up` build fails               | Run `make clean-docker` then retry                    |
| Tests fail with ModuleNotFoundError | Activate venv: `source .venv/Scripts/activate`        |
