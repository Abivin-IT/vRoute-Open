# 01-vkernel — Core OS

> **vKernel** is the central operating system of the vRoute platform.
> All traffic flows through vKernel's API Gateway on **port 8080**.

---

## What vKernel Does

| Module        | Package                   | SyR ID         | Description                                                                        |
| ------------- | ------------------------- | -------------- | ---------------------------------------------------------------------------------- |
| App Engine    | `g0_engine`               | SyR-PLAT-00    | Install/uninstall vApps, manifest parsing, dependency resolution                   |
| IAM / Auth    | `g1_iam`                  | SyR-PLAT-01    | JWT, refresh tokens, OIDC SSO (Google/Microsoft/GitHub), Magic Link, rate limiting |
| Data Backbone | `g2_data`                 | SyR-PLAT-02    | Core entities (Tenant, Stakeholder, Currency, Country), JSONB extension            |
| Event Bus     | `g3_event`                | SyR-PLAT-03    | Pub/Sub event publishing, subscriptions, audit log                                 |
| gRPC IPC      | `g4_grpc`                 | SyR-PLAT-04    | Internal RPC for vApps (Ping, PublishEvent, GetInstalledApps)                      |
| Search        | `g5_search`               | SyR-PLAT-02.02 | PostgreSQL FTS with tsvector + GIN index                                           |
| API Gateway   | Spring Cloud              | —              | Routes `/api/v1/{vapp}/**` and `/{vapp}/**` to backend services                    |
| UI Shell      | `AdaptiveShellController` | —              | Micro-frontend host, iframe isolation, Ctrl+K search                               |

## Gateway Routes → vApps

All vApps are accessed via vKernel gateway on `:8080`. No direct port exposure.

| Route Pattern          | Target Service                                    | Type    |
| ---------------------- | ------------------------------------------------- | ------- |
| `/api/v1/vstrategy/**` | [02-vstrategy](../02-vstrategy/) (internal :8081) | API     |
| `/vstrategy/**`        | [02-vstrategy](../02-vstrategy/) (internal :8081) | UI/HTML |
| `/api/v1/vfinacc/**`   | [03-vfinacc](../03-vfinacc/) (internal :8082)     | API     |
| `/vfinacc/**`          | [03-vfinacc](../03-vfinacc/) (internal :8082)     | UI/HTML |
| `/api/v1/vnewapp/**`   | Template — see `application.yml`                  | —       |

## Registered vApps (Flyway)

| SQL Migration                | Registers                        |
| ---------------------------- | -------------------------------- |
| `V5__register_vstrategy.sql` | [02-vstrategy](../02-vstrategy/) |
| `V8__register_vfinacc.sql`   | [03-vfinacc](../03-vfinacc/)     |

## Tech Stack

- **Java 21** / Spring Boot 3.3 / Spring Cloud Gateway MVC
- **PostgreSQL 16** (Flyway migrations)
- **gRPC** server on port 9090
- **Prometheus** metrics via Micrometer

## Related

- [02-vstrategy](../02-vstrategy/) — S2P2R Strategy vApp
- [03-vfinacc](../03-vfinacc/) — R2R Finance vApp
- [00-design/docs/vkernel-prd.md](../00-design/docs/vkernel-prd.md) — Platform PRD
- [80-deploy](../80-deploy/) — Docker Compose & Helm chart
- [90-guide/developer](../90-guide/developer/) — Developer guide
