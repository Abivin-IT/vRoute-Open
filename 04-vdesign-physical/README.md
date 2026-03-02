# 04-vdesign-physical — I2S Physical Layer

> **vDesign Physical** manages physical entities in the Idea-to-Spec process:
> Golden Sample Vault, Material Inbox, Prototype Version Control,
> Lab Feasibility Testing, Tooling Handover Kits.

---

## Access (via vKernel gateway)

| URL                                                            | Description    |
| -------------------------------------------------------------- | -------------- |
| `http://localhost:8080/vdesign-physical/`                      | Dashboard UI   |
| `http://localhost:8080/api/v1/vdesign-physical/health`         | Health check   |
| `http://localhost:8080/api/v1/vdesign-physical/golden-samples` | Golden Samples |

> **No direct port access.** All traffic goes through [01-vkernel](../01-vkernel/) gateway on `:8080`.

## API Endpoints

| Method | Path                                                      | Description                 |
| ------ | --------------------------------------------------------- | --------------------------- |
| GET    | `/api/v1/vdesign-physical/golden-samples`                 | List golden samples         |
| POST   | `/api/v1/vdesign-physical/golden-samples`                 | Create golden sample        |
| GET    | `/api/v1/vdesign-physical/golden-samples/{id}`            | Get sample details          |
| PUT    | `/api/v1/vdesign-physical/golden-samples/{id}`            | Update sample               |
| POST   | `/api/v1/vdesign-physical/golden-samples/{id}/seal`       | Seal sample (lock)          |
| POST   | `/api/v1/vdesign-physical/golden-samples/{id}/compromise` | Mark as compromised         |
| POST   | `/api/v1/vdesign-physical/materials`                      | Ingest material             |
| GET    | `/api/v1/vdesign-physical/materials`                      | List materials              |
| GET    | `/api/v1/vdesign-physical/materials/{id}`                 | Get material details        |
| POST   | `/api/v1/vdesign-physical/materials/{id}/scrap`           | Scrap material              |
| POST   | `/api/v1/vdesign-physical/prototypes`                     | Create prototype            |
| GET    | `/api/v1/vdesign-physical/prototypes`                     | List prototypes             |
| GET    | `/api/v1/vdesign-physical/prototypes/{id}`                | Get prototype details       |
| POST   | `/api/v1/vdesign-physical/prototypes/{id}/retire`         | Retire prototype (OBSOLETE) |
| POST   | `/api/v1/vdesign-physical/lab-tests`                      | Create lab test             |
| GET    | `/api/v1/vdesign-physical/lab-tests`                      | List lab tests              |
| GET    | `/api/v1/vdesign-physical/lab-tests/summary`              | Lab test summary            |
| GET    | `/api/v1/vdesign-physical/lab-tests/{id}`                 | Get test details            |
| POST   | `/api/v1/vdesign-physical/lab-tests/{id}/complete`        | Complete test (PASS/FAIL)   |
| POST   | `/api/v1/vdesign-physical/handover-kits`                  | Create handover kit         |
| GET    | `/api/v1/vdesign-physical/handover-kits`                  | List handover kits          |
| GET    | `/api/v1/vdesign-physical/handover-kits/{id}`             | Get kit details             |
| POST   | `/api/v1/vdesign-physical/handover-kits/{id}/advance`     | Advance kit status          |
| POST   | `/api/v1/vdesign-physical/handover-kits/{id}/receive`     | Mark kit as received        |
| GET    | `/api/v1/vdesign-physical/health`                         | Health check                |

## Tech Stack

- **Python 3.12** / FastAPI / async SQLAlchemy 2.x / Pydantic v2
- **Alembic** migrations (version table: `alembic_version_vdesign_physical`)
- **gRPC client** → [01-vkernel](../01-vkernel/) port 9090 (graceful degradation)
- **25+ integration tests** (pytest-asyncio + httpx + SQLite in-memory)

## Integration with vKernel

| Integration Point | Details                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------- |
| Gateway routing   | `application.yml` routes `/api/v1/vdesign-physical/**` here                                   |
| App Registry      | Registered via `V9__register_vdesign_physical.sql` in vKernel                                 |
| gRPC IPC          | `grpc_client.py` pings vKernel on startup                                                     |
| Manifest          | `manifest.json` — 3 permissions, 4 events published                                           |
| Events published  | `GOLDEN_SAMPLE_SEALED`, `SAMPLE_COMPROMISED`, `LAB_TEST_COMPLETED`, `HANDOVER_KIT_DISPATCHED` |
| Events subscribed | `SPEC_APPROVED`, `BUILD_REQUEST_CREATED`, `APP_INSTALLED`                                     |

## Dependencies

| Depends On                   | Reason                                 |
| ---------------------------- | -------------------------------------- |
| [01-vkernel](../01-vkernel/) | Auth, Gateway, App Registry, Event Bus |

## Cross-References

- **PRD:** [vdesign-physical-prd.md](../00-design/docs/vdesign-physical-prd.md)
- **vKernel Gateway:** [application.yml](../01-vkernel/src/main/resources/application.yml)
- **Docker Compose:** [docker-compose.yml](../80-deploy/docker-compose.yml)
