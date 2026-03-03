# PRODUCT REQUIREMENTS DOCUMENT: Master App Template

> **Document ID:** `0.0.0-C4-SPEC-CPO-master-app-prd`
> **Version:** 1.0
> **Status:** APPROVED
> **Owner:** CPO (Chief Product Officer)
> **Applies to:** All Business Apps (vStrategy, vFinacc, vDesign Physical, vMarketing Org, and all future apps)
> **Policy Ref:** ISO 25010:2023 | [EARTH] A1-POL-EARTH | [FIRE] A1-POL-FIRE

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [1. Executive Summary](#1-executive-summary)
- [2. Business Goals \& Success Metrics](#2-business-goals--success-metrics)
- [3. Product Overview](#3-product-overview)
- [4. Functional Requirements](#4-functional-requirements)
- [5. Non-Functional Requirements](#5-non-functional-requirements)
- [6. Analytics \& Data Tracking](#6-analytics--data-tracking)
- [7. QA \& Acceptance](#7-qa--acceptance)
- [8. Go-to-Market](#8-go-to-market)
- [9. Appendix](#9-appendix)

---

## 1. Executive Summary

This document defines the **Master App Template** — the standard structure, features, and quality attributes that **every** Business App in the vRoute ecosystem must implement before adding domain-specific logic.

> _Tất cả các apps (vStrategy, vFinacc, vDesign Physical, vMarketing Org và các apps sau này) đều phải implement chuẩn theo Master App trước, sau đó mới bổ sung nghiệp vụ riêng._

**Key Principle:** A newly scaffolded app that implements FR-APP-00 through FR-APP-04 and all 5 NFR categories is already a **fully functional CRUD application** — capable of creating, reading, updating, deleting, listing, importing, exporting, and automating records. Domain-specific PRDs (e.g., `vstrategy-prd.md`) add specialized business rules on top of this foundation.

---

## 2. Business Goals & Success Metrics

| Goal                   | Metric                                      | Target   |
| ---------------------- | ------------------------------------------- | -------- |
| Unified UX             | Time to learn a new app (for existing user) | < 30 min |
| Faster app development | Time from scaffold to first CRUD deploy     | < 1 day  |
| Cross-app consistency  | % of shared components reused               | > 80 %   |
| Quality baseline       | All 5 NFR categories passing                | 100 %    |
| Onboarding efficiency  | New developer productive on any app         | < 1 week |

---

## 3. Product Overview

Every Business App in vRoute is a **vApp** that runs inside the vKernel Adaptive UI Shell (SyR-PLAT-04). The Master App Template defines the 5 standard functional modules and 5 quality attributes that form the common foundation.

### Architecture Position

```
┌─────────────────────────────────────────────────────────────┐
│                    vKernel  (Platform OS)                    │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │
│  │ IAM    │  │ Data   │  │ Event  │  │ UI     │            │
│  │ PLAT-01│  │ PLAT-02│  │ PLAT-03│  │ PLAT-04│            │
│  └────────┘  └────────┘  └────────┘  └────────┘            │
├─────────────────────────────────────────────────────────────┤
│              Master App Template (this doc)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐ ┌──────┐  │
│  │FR-APP-00 │ │FR-APP-01 │ │FR-APP-02 │ │ -03  │ │ -04  │  │
│  │Core Txn  │ │Master    │ │Inter-App │ │Report│ │Config│  │
│  │Engine    │ │Data Mgmt │ │Automation│ │      │ │      │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────┘ └──────┘  │
├─────────────────────────────────────────────────────────────┤
│         Domain-Specific PRDs (vstrategy, vfinacc, …)        │
│  SyR-STR-00…04 │ SyR-FIN-00…04 │ SyR-PHY-00…04 │ …       │
└─────────────────────────────────────────────────────────────┘
```

### vApp Feature-Based DDD Structure

Every vApp follows the same directory pattern:

```
<app>/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entry, mount all feature routers
│   ├── config.py                  # Shared config (env-based, Pydantic Settings)
│   ├── database.py                # Async SQLAlchemy engine + session factory
│   ├── grpc_client.py             # KernelGrpcClient (IPC)
│   ├── <feature_1>/              # FR-APP-00: Core Transaction
│   │   ├── models/
│   │   │   ├── entity.py          # SQLAlchemy ORM entity
│   │   │   └── schema.py          # Pydantic v2 request/response DTOs
│   │   ├── views/
│   │   │   └── renderer.py        # HTML/template renderers
│   │   └── controllers/
│   │       ├── routes.py           # FastAPI Router endpoints
│   │       └── service.py          # Business logic
│   ├── <feature_2>/               # FR-APP-01: Master Data
│   ├── <feature_3>/               # FR-APP-02: Automation
│   ├── <feature_4>/               # FR-APP-03: Reporting
│   └── <feature_5>/               # FR-APP-04: Configurations
├── alembic/                        # Database migrations
├── tests/                          # Integration tests
├── manifest.json                   # vApp manifest for App Engine
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

---

## 4. Functional Requirements

> Every app MUST implement these 5 standard functional modules.
> Tracing Code: `FR-APP-[ID]`. In domain-specific PRDs, replace `APP` with domain prefix (e.g., `FR-STR-00`).

### 4.1. FR-APP-00 | Core Transaction Engine

**Purpose:** The primary CRUD engine for the app's core business entity. This is the **defining requirement** — the one capability that justifies the app's existence.

| Capability | Description                                                           |
| ---------- | --------------------------------------------------------------------- |
| CREATE     | Create new records via Form View with field validation                |
| READ       | View single record detail (Form View) or browse records (List/Kanban) |
| UPDATE     | Edit records inline (List) or via Form View, with optimistic locking  |
| DELETE     | Soft-delete with archive; hard-delete restricted to admin             |
| LIST       | Paginated list with server-side sort, filter, and full-text search    |
| IMPORT     | Bulk import from CSV/Excel with validation report                     |
| EXPORT     | Export filtered results to CSV/Excel/PDF                              |
| APPROVE    | Multi-step approval workflow (Draft → Confirmed → Approved → Done)    |

#### Wireframe — Kanban View (Core Transaction)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [+ CREATE]    Sales Orders          🔍 Search...          ☰ List │▦ Kanban│📊  │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─── Draft ────────┐  ┌─── Confirmed ──────┐  ┌─── Done ──────────┐           │
│  │                   │  │                     │  │                    │           │
│  │ ┌───────────────┐ │  │ ┌─────────────────┐ │  │ ┌────────────────┐ │           │
│  │ │ SO-002        │ │  │ │ SO-001          │ │  │ │ SO-005         │ │           │
│  │ │ TechViet Ltd  │ │  │ │ Abivin JSC      │ │  │ │ LogiCo         │ │           │
│  │ │ $8,750        │ │  │ │ $12,400         │ │  │ │ $31,200        │ │           │
│  │ └───────────────┘ │  │ └─────────────────┘ │  │ └────────────────┘ │           │
│  │ ┌───────────────┐ │  │ ┌─────────────────┐ │  │                    │           │
│  │ │ SO-004        │ │  │ │ SO-003          │ │  │                    │           │
│  │ │ Mekong Corp   │ │  │ │ GreenCo         │ │  │                    │           │
│  │ │ $5,200        │ │  │ │ $23,100         │ │  │                    │           │
│  │ └───────────────┘ │  │ └─────────────────┘ │  │                    │           │
│  └───────────────────┘  └─────────────────────┘  └────────────────────┘           │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.2. FR-APP-01 | Master Data Management

**Purpose:** Manage reference/master data entities that the core transactions depend on. Master data is shared across the app and potentially across apps via the Data Backbone (SyR-PLAT-02).

| Capability          | Description                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| CRUD Master Records | Standard create/read/update/archive for reference entities                 |
| Bulk Operations     | Select-all → bulk update, bulk archive, bulk export                        |
| Data Validation     | Enforce unique constraints, format rules, mandatory fields                 |
| JSONB Extension     | Support dynamic custom fields via `metadata` JSONB column (SyR-PLAT-02.01) |
| Cross-App Sharing   | Publish master data to Data Backbone for other apps to consume             |
| Import/Merge        | Deduplicate on import; merge duplicate records with conflict resolution    |

#### Wireframe — List View with Bulk Actions (Master Data)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [+ CREATE]    Customers             🔍 Search...          ☰ List │▦ Kanban│📊  │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ☑ Select All (3 selected)          [⬇ Export]  [🗑 Archive]  [✏ Bulk Edit]     │
│  ─────────────────────────────────────────────────────────────────────────       │
│  ☑  Abivin JSC          Ho Chi Minh    Technology     ● Active    2024-01-15    │
│  ☑  TechViet Ltd        Hanoi          Software       ● Active    2024-02-20    │
│  ☑  GreenCo             Da Nang        Agriculture    ○ Inactive  2023-11-08    │
│  ☐  Mekong Corp         Can Tho        Logistics      ● Active    2024-03-01    │
│  ☐  Samsung Vina        Bac Ninh       Electronics    ● Active    2024-03-10    │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────       │
│  ◄ 1  2  3 ►              Showing 1-20 of 87 records                            │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.3. FR-APP-02 | Inter-App Automation

**Purpose:** Define event-driven automation rules that connect this app to other apps via the Event Bus (SyR-PLAT-03). Each app must both **publish** events when key state changes occur and **subscribe** to events from other apps to trigger automated actions.

| Capability                | Description                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Event Publishing          | Emit domain events on state transitions (e.g., `ORDER_CONFIRMED`, `PLAN_APPROVED`) |
| Event Subscription        | Listen to events from other apps and trigger internal actions                      |
| Automation Rules          | Configurable trigger → action mappings (no-code for business users)                |
| Flow Visualization        | Visual tree/flow diagram showing event chains across apps                          |
| Retry & Dead-Letter Queue | Failed automations retry 3× then route to DLQ for manual review                    |
| Audit Trail               | Every automation execution logged with timestamp, payload hash, status             |

#### Wireframe — Tree/Flow View (Automation)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [+ CREATE RULE]  Automation Rules    🔍 Search...          ☰ List │🌳 Flow │📊 │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   ┌─────────────────┐          ┌─────────────────────┐                          │
│   │  🔵 TRIGGER      │          │  🟢 ACTION           │                          │
│   │  vSales          │ ───────► │  vFinance            │                          │
│   │  ORDER_CONFIRMED │  event   │  CREATE_INV_DRAFT    │                          │
│   │  {deal_id, amt}  │          │  {ref_id, amount}    │                          │
│   └─────────────────┘          └──────────┬────────────┘                          │
│                                            │                                      │
│                                            ▼                                      │
│                                 ┌─────────────────────┐                          │
│                                 │  🟡 ACTION           │                          │
│                                 │  vStrategy           │                          │
│                                 │  UPDATE_REVENUE_KPI  │                          │
│                                 │  {kpi_id, delta}     │                          │
│                                 └─────────────────────┘                          │
│                                                                                  │
│  History: ✅ Run #142 (2s ago) | ✅ Run #141 (5m ago) | ❌ Run #140 (DLQ)       │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.4. FR-APP-03 | Analytical Reporting

**Purpose:** Provide real-time and historical analytics dashboards for the app's data. Every app must expose its key metrics through standard chart views consumable by the UI Shell.

| Capability        | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| Graph View        | Bar, Line, Pie charts with configurable X/Y dimensions                   |
| Pivot Table       | Row/Column grouping with measure aggregation (Sum, Avg, Count, Min, Max) |
| Dashboard Widgets | KPI cards with trend indicators (↑ ↓ →) shown on app home page           |
| Scheduled Reports | Cron-based report generation + email/webhook delivery                    |
| Export            | Export any chart/table to PNG, CSV, or PDF                               |
| Cross-App Metrics | Publish key metrics to Data Backbone for platform-wide dashboards        |

#### Wireframe — Graph View (Reporting)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [+ CREATE REPORT] Revenue Analysis  🔍 Search...          ☰ List │▦ │📊 Graph  │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Dimension: [Month ▾]    Measure: [Revenue ▾]    Chart: [Bar ▾]                 │
│                                                                                  │
│  Revenue ($K)                                                                    │
│  250 ┤                                                    ████                   │
│  200 ┤                              ████                  ████                   │
│  150 ┤                ████          ████         ████     ████                   │
│  100 ┤    ████        ████          ████         ████     ████                   │
│   50 ┤    ████        ████          ████         ████     ████                   │
│    0 ┼────████────────████──────────████─────────████─────████──►                │
│         Jan          Feb           Mar          Apr      May                     │
│                                                                                  │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐                  │
│  │ Total Revenue│ Avg Order    │ Orders Count │ Growth Rate  │                  │
│  │ $850,000  ↑  │ $12,400      │ 234          │ +18.5 % ↑    │                  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘                  │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.5. FR-APP-04 | App Configurations & Compliance

**Purpose:** Every app must provide a Settings/Configuration page where administrators can customize behavior, set business rules, and manage compliance requirements without code changes.

| Capability         | Description                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| General Settings   | App-level toggles: enable/disable features, default values, timezone, currency |
| Business Rules     | Configurable validation rules (e.g., approval thresholds, field constraints)   |
| Notification Prefs | Per-app notification settings (email, in-app, webhook triggers)                |
| Integration Config | API keys, webhook URLs, third-party service connections                        |
| Compliance Rules   | Regulatory checks (tax rates, audit requirements, data retention policies)     |
| Audit Log Viewer   | Browse audit trail for this app's records (who changed what, when)             |

#### Wireframe — Form View (Configurations)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [💾 SAVE]          App Settings       🔍 Search...          ☰ List │📋 Form    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─ General ──────────────────────────────────────────────────────────────────┐  │
│  │  App Name:          [ vFinance                    ]                        │  │
│  │  Default Currency:  [ VND ▾ ]    Timezone: [ Asia/Ho_Chi_Minh ▾ ]         │  │
│  │  Auto-Approve:      [✓] Enable auto-approve for amounts < $1,000          │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│  ┌─ Compliance ───────────────────────────────────────────────────────────────┐  │
│  │  VAT Rate:          [ 10  ] %    Review Threshold: [ $25,000 ]            │  │
│  │  Data Retention:    [ 7   ] years                                          │  │
│  │  Audit Log:         [✓] Enable     [View Audit Log →]                     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│  ┌─ Notifications ────────────────────────────────────────────────────────────┐  │
│  │  Email on Approval:     [✓]     Webhook on Error: [✓]                     │  │
│  │  Webhook URL:       [ https://hooks.slack.com/services/...       ]        │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Non-Functional Requirements

> Aligned to **ISO 25010:2023** quality model. Every app must meet ALL 5 NFR categories.
> Tracing Code: `NFR-XXX-[ID]`. Replace `XXX` with domain prefix (e.g., `NFR-STR-00`).

### 5.1. NFR-XXX-00 | Security

**Framework:** CIA Triad (Confidentiality · Integrity · Availability)

| Attribute       | Requirement                                                                      | Verification         |
| --------------- | -------------------------------------------------------------------------------- | -------------------- |
| Confidentiality | All API endpoints require JWT authentication; sensitive fields encrypted at rest | Pen-test             |
| Integrity       | Input validation on all endpoints; CSRF protection; SQL injection prevention     | Security scan (SAST) |
| Availability    | Auth failure does not crash app; graceful degradation on IAM service outage      | Chaos test           |
| RBAC            | All endpoints enforce role-based permissions via `@PreAuthorize` or middleware   | Security audit       |
| Data Isolation  | Multi-tenant Row-Level Security (RLS); tenant A cannot access tenant B's data    | Cross-tenant test    |

---

### 5.2. NFR-XXX-01 | Reliability & Safety

**Framework:** RAS + Safety (Reliability · Availability · Serviceability + Safety)

| Attribute      | Requirement                                                                          | Target               |
| -------------- | ------------------------------------------------------------------------------------ | -------------------- |
| Reliability    | Zero data loss on transaction commit; all writes use DB transactions                 | 99.9 % success rate  |
| Availability   | App recovers from crash within 30s; health endpoint responds within 1s               | 99.5 % uptime        |
| Serviceability | Structured JSON logs; correlation IDs propagated across services                     | Log query < 5s       |
| Safety         | Destructive actions (delete, approve large amounts) require confirmation + audit log | 100 % logged         |
| Idempotency    | POST endpoints that create resources must be idempotent (via `X-Idempotency-Key`)    | No duplicate records |

---

### 5.3. NFR-XXX-02 | Performance

**Framework:** L-T-C (Latency · Throughput · Capacity) + USE Method + Google 4 Golden Signals

| Signal     | Metric                              | Target                   |
| ---------- | ----------------------------------- | ------------------------ |
| Latency    | API response time (p50 / p95 / p99) | 100ms / 300ms / 1s       |
| Traffic    | Concurrent users supported          | ≥ 100 per app instance   |
| Errors     | Error rate under normal load        | < 0.1 %                  |
| Saturation | CPU / Memory usage at peak          | < 70 % CPU, < 80 % RAM   |
| Throughput | Transactions per second (TPS)       | ≥ 50 TPS per instance    |
| Capacity   | Records per entity table            | ≥ 1M without degradation |
| Page Load  | Initial page render (LCP)           | < 2.5s                   |
| Search     | Full-text search response           | < 500ms                  |

---

### 5.4. NFR-XXX-03 | Interaction Capability

**Framework:** E-E-S (Effectiveness · Efficiency · Satisfaction)

| Attribute      | Requirement                                                                     | Metric                |
| -------------- | ------------------------------------------------------------------------------- | --------------------- |
| Effectiveness  | User can complete primary task (CRUD) without documentation                     | Task success > 95 %   |
| Efficiency     | Common workflows (create → approve) require ≤ 3 clicks                          | Avg clicks ≤ 3        |
| Satisfaction   | UI consistent with vKernel Shell; 7 standard views; keyboard shortcuts (Ctrl+K) | SUS score ≥ 70        |
| Accessibility  | WCAG 2.1 AA compliance; screen reader support; keyboard navigation              | Lighthouse ≥ 90       |
| Responsiveness | Usable on desktop (1024px+) and tablet (768px+)                                 | No horizontal scroll  |
| Error UX       | Validation errors shown inline; toast notifications for async operations        | Error visible < 200ms |

---

### 5.5. NFR-XXX-04 | Maintainability, Flexibility & Compatibility

**Framework:** M-T-F-C (Modularity · Testability · Flexibility · Compatibility)

| Attribute     | Requirement                                                                          | Target                   |
| ------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| Modularity    | Feature-based DDD structure (models/views/controllers per feature)                   | Max 1 import cycle       |
| Testability   | Every feature module has integration tests; ≥ 80 % code coverage                     | ≥ 80 % coverage          |
| Analyzability | Structured code with `@GovernanceID` annotations; clear naming conventions           | Code review < 30 min/PR  |
| Flexibility   | JSONB `metadata` extension on all core entities; configurable business rules         | No code change for rules |
| Compatibility | REST API contract backward-compatible across minor versions; manifest.json versioned | Zero breaking changes    |
| Deployability | Docker image build < 2 min; one-command deploy via `make` or Helm                    | Deploy < 5 min           |

---

## 6. Analytics & Data Tracking

Every app must expose analytics data to the platform for cross-app dashboards and monitoring.

| Data Point              | Source                  | Frequency   | Consumer      |
| ----------------------- | ----------------------- | ----------- | ------------- |
| Record count by status  | Core Transaction Engine | Real-time   | App Dashboard |
| CRUD operation counts   | API middleware          | Per-request | vMonitor      |
| Error rates by endpoint | API middleware          | Per-request | vMonitor      |
| User activity           | Auth middleware         | Per-session | vAudit        |
| Business KPIs           | Reporting module        | Scheduled   | vStrategy     |
| Event throughput        | Event Bus integration   | Per-event   | vFlow         |

---

## 7. QA & Acceptance

### 7.1. Verification Methods (I-A-D-T)

Every requirement is verified using one or more of these 4 methods:

| Method        | Code | Description                                              | When Used                           |
| ------------- | ---- | -------------------------------------------------------- | ----------------------------------- |
| Inspection    | I    | Manual review of code, documents, or configurations      | Architecture review, code review    |
| Analysis      | A    | Mathematical or logical proof that requirement is met    | Performance modeling, capacity plan |
| Demonstration | D    | Show working feature in a controlled environment         | Sprint demo, UAT session            |
| Test          | T    | Automated or manual test execution with pass/fail result | CI pipeline, regression testing     |

### 7.2. Requirements Traceability Matrix (RTM Template)

Every app PRD must include an RTM mapping requirements to verification:

| Req ID     | Requirement Name                | V-Method | Test/Evidence                          | Status    |
| ---------- | ------------------------------- | -------- | -------------------------------------- | --------- |
| FR-APP-00  | Core Transaction Engine         | T        | `test_<app>_crud.py` — CRUD tests      | ☐ Not Run |
| FR-APP-01  | Master Data Management          | T        | `test_<app>_master.py` — Master data   | ☐ Not Run |
| FR-APP-02  | Inter-App Automation            | T + D    | `test_<app>_events.py` + demo          | ☐ Not Run |
| FR-APP-03  | Analytical Reporting            | D        | Sprint demo — chart views              | ☐ Not Run |
| FR-APP-04  | App Configurations              | T + I    | `test_<app>_config.py` + code review   | ☐ Not Run |
| NFR-XXX-00 | Security                        | T + A    | Pen-test report + SAST scan            | ☐ Not Run |
| NFR-XXX-01 | Reliability & Safety            | T        | Chaos test + idempotency test          | ☐ Not Run |
| NFR-XXX-02 | Performance                     | T + A    | Load test (k6/Locust) + capacity model | ☐ Not Run |
| NFR-XXX-03 | Interaction Capability          | D + T    | UAT session + Lighthouse audit         | ☐ Not Run |
| NFR-XXX-04 | Maintainability & Compatibility | I + T    | Code review + coverage report          | ☐ Not Run |

### 7.3. Acceptance Criteria Template

Each app must define Gherkin scenarios for every FR. Example pattern:

```gherkin
Feature: Core Transaction Engine
  Scenario: Create a new record
    Given user has CREATE permission for <entity>
    When user fills the Form View and clicks SAVE
    Then a new record is created with status DRAFT
    And an event <APP>_RECORD_CREATED is published

  Scenario: Bulk export records
    Given user is on List View with 50+ records
    When user selects all and clicks EXPORT → CSV
    Then a CSV file is downloaded containing all selected records
    And export is logged in audit trail
```

---

## 8. Go-to-Market

### Adoption Checklist for New Apps

Before a new vApp can be deployed to production:

- [ ] All 5 FR modules implemented (FR-APP-00 through FR-APP-04)
- [ ] All 5 NFR categories verified (NFR-XXX-00 through NFR-XXX-04)
- [ ] `manifest.json` with correct `app_id`, permissions, events, dependencies
- [ ] Integration tests covering all endpoints (≥ 80 % code coverage)
- [ ] Feature-based DDD directory structure matching the template
- [ ] API contract documented in `api-contract-summary.md`
- [ ] Acceptance criteria documented in `acceptance-criteria.md`
- [ ] Requirements traced in `requirements-traceability-matrix.md`
- [ ] Dockerfile + docker-compose entry configured
- [ ] Code review completed by at least 1 team member

---

## 9. Appendix

### A. Mapping to Existing Apps

| App              | FR-APP-00 (Core Txn)        | FR-APP-01 (Master Data) | FR-APP-02 (Automation)   | FR-APP-03 (Reporting) | FR-APP-04 (Config)     |
| ---------------- | --------------------------- | ----------------------- | ------------------------ | --------------------- | ---------------------- |
| vStrategy        | Plans (SyR-STR-00)          | Alignment Tree          | PLAN_APPROVED event      | BSC Scorecard         | S&OP Config            |
| vFinacc          | Ledger Entries (SyR-FIN-00) | Chart of Accounts       | ORDER→INVOICE automation | P&L / Balance Sheet   | Tax & Compliance rules |
| vDesign Physical | Golden Samples (SyR-PHY-00) | Materials Inbox         | TOOLING_DISPATCHED event | Lab Test Reports      | Spec Tolerance Config  |
| vMarketing Org   | Campaigns (SyR-MKT-ORG-00)  | Audience Segments       | INTENT_HOT_SIGNAL event  | Campaign Analytics    | Scoring Thresholds     |

### B. View Type Reference

| #   | View Type | Primary Use                | 3 Defining Features                                |
| --- | --------- | -------------------------- | -------------------------------------------------- |
| 1   | List      | Browse & bulk operations   | Sortable columns · Bulk actions · Inline edit      |
| 2   | Kanban    | Pipeline & status tracking | Drag-and-drop · Stage columns · Color coding       |
| 3   | Form      | Single record detail       | Field validation · Chatter log · Related records   |
| 4   | Calendar  | Date-based planning        | Day/Week/Month · Drag reschedule · Color by status |
| 5   | Graph     | Visual analytics           | Bar/Line/Pie · Dimension selector · Export         |
| 6   | Pivot     | Multi-dimensional analysis | Row/Column group · Aggregation · Drill-down        |
| 7   | Map       | Geospatial data            | Location pins · Cluster zoom · Route overlay       |

### C. Naming Conventions

| Item                 | Convention                   | Example                         |
| -------------------- | ---------------------------- | ------------------------------- |
| Requirement ID (FR)  | `FR-<APP>-<NN>`              | `FR-STR-00`, `FR-FIN-02`        |
| Requirement ID (NFR) | `NFR-<APP>-<NN>`             | `NFR-STR-00`, `NFR-FIN-02`      |
| Event name           | `<DOMAIN>_<ENTITY>_<ACTION>` | `FINANCE_INVOICE_APPROVED`      |
| API route            | `/api/v1/<app>/<entity>`     | `/api/v1/vfinacc/ledger`        |
| Test file            | `test_<feature>_api.py`      | `test_ledger_api.py`            |
| Feature folder       | `<snake_case>/`              | `golden_sample/`, `lead_score/` |
