# Non-Functional Requirements — Targets

> Source: vKernel PRD Section 5

| # | NFR ID | Name | Metric | Target | Verification Method | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | NFR-PLAT-01 | Performance | App install/hot-swap time (p95) | < 10 seconds | Benchmark | Must |
| 2 | NFR-PLAT-01 | Performance | Cross-App query latency (p99) | < 300 ms | Benchmark | Must |
| 3 | NFR-PLAT-02 | Reliability & Availability | Downtime during App install/update/remove | Zero | Chaos testing | Must |
| 4 | NFR-PLAT-02 | Reliability & Availability | Platform uptime (monthly) | >= 99.9% | Monitoring / SLA | Must |
| 5 | NFR-PLAT-03 | Security & Compliance | IPC event logging | Immutable (append-only) | Pen-test + compliance check | Must |
| 6 | NFR-PLAT-03 | Security & Compliance | RBAC enforcement | Every request validated (no bypass) | Pen-test | Must |
| 7 | NFR-PLAT-03 | Security & Compliance | Compliance readiness | ISO 27001, VN ND123 (Hoa don dien tu) | Compliance check | Must |
| 8 | NFR-PLAT-04 | Scalability | Concurrent users | 1,000 with < 1s avg response | Load test | Later |
| 9 | NFR-PLAT-04 | Scalability | Scaling model | Horizontal via Kubernetes | Architecture review | Later |
| 10 | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Database isolation | Separate DB per Tenant (physical isolation) | Security audit + RLS test | Must |
| 11 | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Inter-App data access | API-only (via manifest apis.provided); no direct DB access | Cross-tenant pen-test | Must |
| 12 | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Inter-App auth | Re-Auth & Re-Authz on every call (X-App-ID + permission) | Security audit | Must |
| 13 | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | JSONB field visibility | Scoped per App (e.g., only vMarketing sees facebook_url) | Integration test | Must |

## Observability Metrics (Prometheus)

| Metric Name | Type | Source |
| --- | --- | --- |
| `install_duration_seconds` | Histogram | App Engine (SyR-PLAT-00) |
| `cross_query_latency_ms` | Histogram | Data Service (SyR-PLAT-02) |
| `event_pubsub_success_rate` | Gauge | Event Bus (SyR-PLAT-03) |
