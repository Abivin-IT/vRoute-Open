# Non-Functional Requirements — Targets

> Source: vKernel PRD Section 5 + Business App PRDs.

| # | Scope | NFR ID | Name | Metric | Target | Verification Method | Priority |
|---|-------|--------|------|--------|--------|---------------------|----------|
| 1 | Platform | NFR-PLAT-01 | Performance | App install/hot-swap time (p95) | < 10 seconds | Benchmark | Must |
| 2 | Platform | NFR-PLAT-01 | Performance | Cross-App query latency (p99) | < 300 ms | Benchmark | Must |
| 3 | Platform | NFR-PLAT-02 | Reliability & Availability | Downtime during App install/update/remove | Zero | Chaos testing | Must |
| 4 | Platform | NFR-PLAT-02 | Reliability & Availability | Platform uptime (monthly) | >= 99.9% | Monitoring / SLA | Must |
| 5 | Platform | NFR-PLAT-03 | Security & Compliance | IPC event logging | Immutable (append-only) | Pen-test + compliance check | Must |
| 6 | Platform | NFR-PLAT-03 | Security & Compliance | RBAC enforcement | Every request validated (no bypass) | Pen-test | Must |
| 7 | Platform | NFR-PLAT-03 | Security & Compliance | Compliance readiness | ISO 27001, VN ND123 (Hoa don dien tu) | Compliance check | Must |
| 8 | Platform | NFR-PLAT-04 | Scalability | Concurrent users | 1,000 with < 1s avg response | Load test | Later |
| 9 | Platform | NFR-PLAT-04 | Scalability | Scaling model | Horizontal via Kubernetes | Architecture review | Later |
| 10 | Platform | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Database isolation | Separate DB per Tenant (physical isolation) | Security audit + RLS test | Must |
| 11 | Platform | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Inter-App data access | API-only (via manifest apis.provided); no direct DB access | Cross-tenant pen-test | Must |
| 12 | Platform | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | Inter-App auth | Re-Auth & Re-Authz on every call (X-App-ID + permission) | Security audit | Must |
| 13 | Platform | NFR-PLAT-05 | Multi-Tenancy & Data Isolation | JSONB field visibility | Scoped per App (e.g., only vMarketing sees facebook_url) | Integration test | Must |
| 14 | vDesign Physical | NFR-PHY-00 | Seal Protection | Unauthorized access to sealed sample | Blocked + security violation logged | Security audit | Must |
| 15 | vDesign Physical | NFR-PHY-01 | Spec Drift Alert | Weight deviation > 5% from CAD | SPEC_DRIFT_DETECTED auto-published | Integration test | Must |
| 16 | vFinacc | NFR-FIN-00 | Ledger Immutability | Posted entry modification | Blocked — append-only (reversal journal required) | Data integrity check | Must |
| 17 | vMarketing Org | NFR-MKT-00 | Content Compliance | Expired/non-compliant content attachment | Campaign START blocked + audit trail | System test | Must |

## Observability Metrics (Prometheus)

| Metric Name | Type | Source | Scope |
|-------------|------|--------|-------|
| `install_duration_seconds` | Histogram | App Engine (SyR-PLAT-00) | Platform |
| `cross_query_latency_ms` | Histogram | Data Service (SyR-PLAT-02) | Platform |
| `event_pubsub_success_rate` | Gauge | Event Bus (SyR-PLAT-03) | Platform |
| `reconciliation_match_rate` | Gauge | Reconciliation (SyR-FIN-02) | vFinacc |
| `convergence_scan_duration_ms` | Histogram | Spec Master (SyR-PHY-00) | vDesign Physical |
| `lead_score_accuracy_pct` | Gauge | Lead Scorer (SyR-MKT-ORG-04) | vMarketing Org |
