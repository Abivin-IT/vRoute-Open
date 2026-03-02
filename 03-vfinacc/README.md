# 03-vfinacc — R2R Finance Module

> **vFinacc** handles Record-to-Report finance operations:
> Continuous Ledger, Transaction Ingestion, 3-way Reconciliation,
> Cost Center Allocation, Tax & Compliance Guard.

---

## Access (via vKernel gateway)

| URL                                           | Description  |
| --------------------------------------------- | ------------ |
| `http://localhost:8080/vfinacc/`              | Dashboard UI |
| `http://localhost:8080/api/v1/vfinacc/health` | Health check |
| `http://localhost:8080/api/v1/vfinacc/ledger` | Ledger CRUD  |

> **No direct port access.** All traffic goes through [01-vkernel](../01-vkernel/) gateway on `:8080`.

## API Endpoints

| Method | Path                                     | Description              |
| ------ | ---------------------------------------- | ------------------------ |
| GET    | `/api/v1/vfinacc/ledger`                 | List ledger entries      |
| POST   | `/api/v1/vfinacc/ledger`                 | Create draft entry       |
| PUT    | `/api/v1/vfinacc/ledger/{id}`            | Update draft entry       |
| POST   | `/api/v1/vfinacc/ledger/{id}/post`       | Post entry (finalize)    |
| POST   | `/api/v1/vfinacc/transactions`           | Ingest transaction       |
| GET    | `/api/v1/vfinacc/transactions`           | List transactions        |
| POST   | `/api/v1/vfinacc/reconciliation/run`     | Run 3-way reconciliation |
| GET    | `/api/v1/vfinacc/reconciliation`         | List matches             |
| GET    | `/api/v1/vfinacc/reconciliation/summary` | Match summary stats      |
| POST   | `/api/v1/vfinacc/cost-centers`           | Create cost allocation   |
| GET    | `/api/v1/vfinacc/cost-centers`           | List cost centers        |
| GET    | `/api/v1/vfinacc/cost-centers/summary`   | Budget vs actuals        |
| POST   | `/api/v1/vfinacc/compliance/check`       | Run compliance check     |
| GET    | `/api/v1/vfinacc/compliance`             | List checks              |
| GET    | `/api/v1/vfinacc/compliance/summary`     | Pass/flag/fail summary   |
| GET    | `/api/v1/vfinacc/health`                 | Health check             |

## Tech Stack

- **Python 3.12** / FastAPI / async SQLAlchemy 2.x / Pydantic v2
- **Alembic** migrations (version table: `alembic_version_vfinacc`)
- **gRPC client** → [01-vkernel](../01-vkernel/) port 9090 (graceful degradation)
- **28 integration tests** (pytest-asyncio + httpx + SQLite in-memory)

## Integration with vKernel

| Integration Point | Details                                                                                 |
| ----------------- | --------------------------------------------------------------------------------------- |
| Gateway routing   | `application.yml` routes `/api/v1/vfinacc/**` here                                      |
| App Registry      | Registered via `V8__register_vfinacc.sql` in vKernel                                    |
| gRPC IPC          | `grpc_client.py` pings vKernel on startup                                               |
| Manifest          | `manifest.json` — 4 permissions, 4 events published                                     |
| Events published  | `TRANSACTION_POSTED`, `BUDGET_OVERRUN_ALERT`, `RECON_COMPLETED`, `COMPLIANCE_VIOLATION` |
| Events subscribed | `APP_INSTALLED`, `OKR_STATUS_CHANGED`                                                   |

## Dependencies

| Depends On                       | Reason                                    |
| -------------------------------- | ----------------------------------------- |
| [01-vkernel](../01-vkernel/)     | Gateway, auth, app registry, gRPC, events |
| [02-vstrategy](../02-vstrategy/) | Cost Center targets from S&OP plan        |

## Depended On By

_No downstream consumers yet._

## Related

- [01-vkernel](../01-vkernel/) — Core OS (gateway, auth, events)
- [02-vstrategy](../02-vstrategy/) — Strategy vApp (upstream dependency)
- [00-design/docs/vfinacc-prd.md](../00-design/docs/vfinacc-prd.md) — PRD
- [00-design/sheets/vfinacc/](../00-design/sheets/vfinacc/) — Data model & API contract
- [90-guide/user](../90-guide/user/) — User guide
