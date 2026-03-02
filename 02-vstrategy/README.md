# 02-vstrategy — S2P2R Strategy Module

> **vStrategy** handles Strategy-to-Plan-to-Result execution:
> Balanced Scorecard, Alignment Trees, S&OP Validation, Pivot Signals.

---

## Access (via vKernel gateway)

| URL                                             | Description  |
| ----------------------------------------------- | ------------ |
| `http://localhost:8080/vstrategy/`              | Dashboard UI |
| `http://localhost:8080/api/v1/vstrategy/health` | Health check |
| `http://localhost:8080/api/v1/vstrategy/plans`  | Plans CRUD   |

> **No direct port access.** All traffic goes through [01-vkernel](../01-vkernel/) gateway on `:8080`.

## API Endpoints

| Method | Path                                     | Description             |
| ------ | ---------------------------------------- | ----------------------- |
| GET    | `/api/v1/vstrategy/plans`                | List plans              |
| POST   | `/api/v1/vstrategy/plans`                | Create plan             |
| PUT    | `/api/v1/vstrategy/plans/{id}`           | Update plan             |
| GET    | `/api/v1/vstrategy/plans/{id}/tree`      | Alignment tree          |
| POST   | `/api/v1/vstrategy/plans/{id}/tree`      | Add tree node           |
| PUT    | `/api/v1/vstrategy/tree/{nodeId}`        | Update node             |
| POST   | `/api/v1/vstrategy/plans/{id}/propagate` | Status propagation      |
| GET    | `/api/v1/vstrategy/plans/{id}/scorecard` | BSC Scorecard           |
| GET    | `/api/v1/vstrategy/plans/{id}/sop`       | S&OP 68/27/5 validation |
| POST   | `/api/v1/vstrategy/signals/check`        | Check pivot signals     |
| GET    | `/api/v1/vstrategy/signals`              | List pivot signals      |
| GET    | `/api/v1/vstrategy/health`               | Health check            |

## Tech Stack

- **Python 3.12** / FastAPI / async SQLAlchemy 2.x / Pydantic v2
- **Alembic** migrations (version table: `alembic_version_vstrategy`)
- **TypeScript** frontend (IIFE bundle → `static/`)
- **gRPC client** → [01-vkernel](../01-vkernel/) port 9090 (graceful degradation)

## Integration with vKernel

| Integration Point | Details                                                      |
| ----------------- | ------------------------------------------------------------ |
| Gateway routing   | `application.yml` routes `/api/v1/vstrategy/**` here         |
| App Registry      | Registered via `V5__register_vstrategy.sql` in vKernel       |
| gRPC IPC          | `grpc_client.py` pings vKernel on startup                    |
| Manifest          | `manifest.json` — 4 permissions, 3 events published          |
| Events published  | `OKR_STATUS_CHANGED`, `PIVOT_SIGNAL_RAISED`, `SOP_VALIDATED` |

## Dependencies

| Depends On                   | Reason                                    |
| ---------------------------- | ----------------------------------------- |
| [01-vkernel](../01-vkernel/) | Gateway, auth, app registry, gRPC, events |

## Depended On By

| Consumer                     | Reason                                  |
| ---------------------------- | --------------------------------------- |
| [03-vfinacc](../03-vfinacc/) | Cost Center targets come from S&OP plan |

## Related

- [01-vkernel](../01-vkernel/) — Core OS (gateway, auth, events)
- [03-vfinacc](../03-vfinacc/) — Finance vApp (depends on vStrategy)
- [00-design/docs/vstrategy-prd.md](../00-design/docs/vstrategy-prd.md) — PRD
- [90-guide/user](../90-guide/user/) — User guide
