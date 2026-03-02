# vKernel PRD — Core OS Platform Kernel

> **Document ID:** `0.0.0-C4-SPEC-CTO-platform-vkernel-prd`
> **Version:** 1.2 (aligned with FIRE Policy v1.0)
> **Status:** APPROVED
> **Owner:** CTO
> **Tech Stack:** Java 21 / Spring Boot 3.3 / PostgreSQL 16 / Flyway / gRPC / Spring Cloud Gateway
> **Policy Ref:** [FIRE] A0-POL-FIRE-PLATFORM (Core Infrastructure)

## 1. Introduction

### 1.1. Purpose

vKernel là Core OS (hạt nhân) của nền tảng vRoute — Composable Enterprise OS.
Cung cấp foundation services cho tất cả Business Apps (vApps):
Identity & Access Management, App Engine (install/lifecycle), Data Backbone,
Event Bus (Pub/Sub), gRPC IPC, và API Gateway routing.

### 1.2. Scope

- **In Scope:** IAM (JWT + refresh tokens + rate limiting + multi-tenant),
  App Engine (manifest-based install/uninstall/lifecycle),
  Data Backbone (core entities + JSONB extension),
  Event Bus (publish/subscribe + audit trail),
  gRPC IPC (KernelService),
  API Gateway (Spring Cloud Gateway MVC routing),
  Observability (Prometheus + Actuator).
- **Out of Scope:** Business logic (delegated to vApps), UI rendering (delegated to vApps + UI Shell).

### 1.3. Definitions

| Term           | Definition                                                                   |
| -------------- | ---------------------------------------------------------------------------- |
| vKernel        | Core OS platform — shared infrastructure services for all vApps              |
| vApp           | Business application module (e.g., vStrategy, vFinance) running on vKernel   |
| Manifest       | JSON descriptor for a vApp — permissions, events, dependencies               |
| Event Bus      | Internal Pub/Sub system for cross-app communication with immutable audit log |
| Data Backbone  | Shared core entities (tenants, stakeholders, currencies) + JSONB extension   |
| Golden Record  | Master data entity (stakeholder) managed by Data Backbone                    |
| Alignment Tree | Hierarchical goal structure (Vision→BSC→OKR→Initiative→Task)                 |

### 1.4. Problem & Opportunity

**Problem:**

- Enterprise software is monolithic — changing one module risks breaking others
- Each department buys separate SaaS → data silos, no single source of truth
- Custom integrations are fragile and hard to maintain

**Opportunity:**

- Composable architecture: install/uninstall vApps like mobile apps
- Shared data backbone: Golden Records accessible to all apps
- Event-driven IPC: loose coupling between modules
- Single IAM: one identity across all apps

### 1.5. User Personas

| Persona        | Role      | Needs                                                   |
| -------------- | --------- | ------------------------------------------------------- |
| Platform Admin | IT/CTO    | Install/manage vApps, configure tenants, monitor health |
| App Developer  | Engineer  | Register events, extend data, authenticate via JWT      |
| Business User  | Staff/Mgr | Single sign-on, cross-app data visibility               |

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: vApps (vStrategy, vFinance, vSales, ...)           │
│  ◆ Each vApp: own port, own DB schema, own frontend         │
├─────────────────────────────────────────── gRPC (9090) ─────┤
│  TIER 2: vKernel Core OS (Java 21 / Spring Boot 3.3)       │
│  ┌──────────┐ ┌─────────┐ ┌───────────┐ ┌──────────────┐   │
│  │ g0_engine│ │ g1_iam  │ │ g2_data   │ │ g3_event     │   │
│  │ App Reg  │ │ JWT/Auth│ │ Backbone  │ │ Pub/Sub      │   │
│  │ Manifest │ │ Refresh │ │ JSONB ext │ │ Audit Trail  │   │
│  │ Lifecycl │ │ Rate lim│ │ Tenants   │ │ Subscriptions│   │
│  └──────────┘ └─────────┘ └───────────┘ └──────────────┘   │
│  ┌──────────┐ ┌────────────────────────────────────────┐   │
│  │ g4_grpc  │ │ Spring Cloud Gateway MVC (routing)      │   │
│  │ IPC Svc  │ │ /api/v1/vstrategy/** → vstrategy:8081   │   │
│  └──────────┘ └────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  TIER 3: PostgreSQL 16 │ Redis 7 │ Flyway migrations       │
└─────────────────────────────────────────────────────────────┘
```

## 3. System Requirements

### 3.1 SyR-PLAT-00: App Engine (Dynamic App Registry)

| Req ID        | Name                          | Priority |
| ------------- | ----------------------------- | -------- |
| SyR-PLAT-00.0 | App Registry (DB-backed)      | Must     |
| SyR-PLAT-00.1 | Manifest Parser & Validator   | Must     |
| SyR-PLAT-00.2 | Dependency Resolution         | Must     |
| SyR-PLAT-00.3 | Install / Uninstall Lifecycle | Must     |
| SyR-PLAT-00.4 | Permission Injection          | Must     |

**Key Features:**

- `GET /api/v1/apps` — List installed (ACTIVE) apps
- `POST /api/v1/apps/install` — Install app from manifest URL or inline JSON
- `DELETE /api/v1/apps/{appId}` — Uninstall (deactivate) app
- `GET /api/v1/apps/permissions` — List injected permissions (optional `?app=`)
- Manifest model: `app_id`, `version`, `display_name`, `permissions[]`, `events.published[]`, `events.subscribed[]`, `dependencies[]`
- Install lifecycle fires `APP_INSTALLED` event; uninstall fires `APP_UNINSTALLED`
- Auto-registers vStrategy via Flyway migration `V5__register_vstrategy.sql`

### 3.2 SyR-PLAT-01: Identity & Access Management (IAM)

| Req ID        | Name                               | Priority |
| ------------- | ---------------------------------- | -------- |
| SyR-PLAT-01.0 | JWT Authentication                 | Must     |
| SyR-PLAT-01.1 | User Registration & Login          | Must     |
| SyR-PLAT-01.2 | Refresh Token Rotation (SHA-256)   | Must     |
| SyR-PLAT-01.3 | Rate Limiting (auth endpoints)     | Must     |
| SyR-PLAT-01.4 | Multi-tenant Context (ThreadLocal) | Must     |
| SyR-PLAT-01.5 | OIDC/SSO Integration               | Deferred |
| SyR-PLAT-01.6 | Magic Link (Passwordless)          | Deferred |

**Key Features:**

- `POST /api/v1/auth/register` — Create user (email + password + tenant)
- `POST /api/v1/auth/login` — Returns access_token (JWT) + refresh_token (opaque, SHA-256 hashed)
- `POST /api/v1/auth/refresh` — Rotate refresh token (old → revoke, new → issue)
- `POST /api/v1/auth/logout` — Revoke all refresh tokens for current user
- Refresh token: 32-byte SecureRandom, stored as SHA-256 hex hash, 30-day expiry
- Reuse-attack detection: if revoked token is presented again, all user tokens revoked
- Rate limiting: sliding window 10 req/60s per IP on `/login` and `/register`
- TenantContext: ThreadLocal populated from JWT `tenant_id` claim, cleared after request
- JWT contains: `sub` (email), `roles`, `tenant_id`, `iat`, `exp`

### 3.3 SyR-PLAT-02: Data Backbone

| Req ID        | Name                          | Priority |
| ------------- | ----------------------------- | -------- |
| SyR-PLAT-02.0 | Core Entities (Tenants, etc.) | Must     |
| SyR-PLAT-02.1 | JSONB Extension API           | Must     |
| SyR-PLAT-02.2 | Reference Data (Currencies)   | Must     |
| SyR-PLAT-02.3 | Universal Search (FTS)        | Deferred |

**Key Features:**

- Core entities: `kernel_tenants`, `kernel_stakeholders` (Golden Records), `kernel_currencies`, `kernel_countries`
- JSONB extension: `PATCH /api/v1/data/entities/{type}/{id}/extend` — merge custom fields without schema changes
- Read-only reference endpoints:
  - `GET /api/v1/data/currencies` — 8 seeded currencies (VND, USD, EUR, JPY, CNY, KRW, THB, SGD)
  - `GET /api/v1/data/countries` — 8 seeded ASEAN + trade partner countries
  - `GET /api/v1/data/tenants` — List tenants
  - `GET /api/v1/data/stakeholders?tenant=` — List stakeholders

### 3.4 SyR-PLAT-03: Event Bus & IPC

| Req ID        | Name                        | Priority |
| ------------- | --------------------------- | -------- |
| SyR-PLAT-03.0 | Event Publishing            | Must     |
| SyR-PLAT-03.1 | Subscription Registration   | Must     |
| SyR-PLAT-03.2 | Immutable Audit Trail       | Must     |
| SyR-PLAT-03.3 | Distributed Pub/Sub (Redis) | Deferred |

**Key Features:**

- `POST /api/v1/events/publish` — Publish event (Headers: `X-App-ID`, `X-Correlation-ID`)
- `POST /api/v1/events/subscribe` — Register subscription (idempotent)
- `GET /api/v1/events/subscriptions?app=` — List subscriptions
- `GET /api/v1/events/log` — Immutable audit trail
- Events stored in `kernel_event_log` (id, type, version, source_app, payload JSONB, status, correlation_id, subscribers_notified)
- Subscriptions stored in `kernel_subscriptions` (subscriber_app, event_type, status)

### 3.5 SyR-PLAT-04: gRPC IPC (Internal Communication)

| Req ID        | Name                      | Priority |
| ------------- | ------------------------- | -------- |
| SyR-PLAT-04.0 | KernelService Ping        | Must     |
| SyR-PLAT-04.1 | Event Publishing via gRPC | Must     |
| SyR-PLAT-04.2 | App Discovery via gRPC    | Must     |

**Key Features:**

- Proto: `kernel.proto` (proto3) — package `vkernel`
- Service: `KernelService` on port 9090
- RPCs: `Ping(PingRequest) → PingResponse`, `PublishEvent(GrpcEventRequest) → GrpcEventResponse`, `GetInstalledApps(GetAppsRequest) → GetAppsResponse`
- Server: `net.devh:grpc-server-spring-boot-starter` auto-registers service
- Health + Reflection services auto-enabled

### 3.6 SyR-PLAT-05: Observability

| Req ID        | Name               | Priority |
| ------------- | ------------------ | -------- |
| SyR-PLAT-05.0 | Health Endpoint    | Must     |
| SyR-PLAT-05.1 | Prometheus Metrics | Must     |
| SyR-PLAT-05.2 | Structured Logging | Should   |

**Key Features:**

- `GET /actuator/health` — Health check with DB, disk, ping components
- `GET /actuator/prometheus` — Micrometer metrics (JVM, HTTP, gRPC, custom)
- `GET /actuator/info` — Application info
- Logging: structured console pattern with ISO8601 timestamps

## 4. Non-Functional Requirements (NFRs)

| NFR ID  | Metric                         | Target      |
| ------- | ------------------------------ | ----------- |
| NFR-001 | API response time (p99)        | < 200ms     |
| NFR-002 | Auth endpoint throughput       | ≥ 100 req/s |
| NFR-003 | gRPC Ping latency              | < 10ms      |
| NFR-004 | Event publishing latency       | < 50ms      |
| NFR-005 | DB connection pool utilization | < 80%       |
| NFR-006 | Flyway migrations (cold start) | < 5s        |
| NFR-007 | JWT validation overhead        | < 2ms       |
| NFR-008 | Rate limiter memory (per IP)   | < 1KB       |

## 5. Acceptance Criteria (Gherkin)

### SyR-PLAT-00: App Engine

```gherkin
Feature: App Engine Lifecycle
  Scenario: Install vApp from manifest
    Given a valid manifest.json for "vStrategy"
    When POST /api/v1/apps/install with inline manifest
    Then response status is 201
    And GET /api/v1/apps returns "vstrategy" with status ACTIVE
    And APP_INSTALLED event is published

  Scenario: Uninstall vApp
    Given "vstrategy" is ACTIVE
    When DELETE /api/v1/apps/vstrategy
    Then response status is 200
    And "vstrategy" status is INACTIVE
    And APP_UNINSTALLED event is published
```

### SyR-PLAT-01: IAM

```gherkin
Feature: Authentication & Authorization
  Scenario: Register + Login
    Given POST /api/v1/auth/register with valid email/password
    Then response contains JWT token

  Scenario: Refresh Token Rotation
    Given a valid refresh token from login
    When POST /api/v1/auth/refresh with that token
    Then new access_token and refresh_token are returned
    And old refresh token is revoked

  Scenario: Rate Limiting
    Given 11 rapid POST requests to /api/v1/auth/login
    Then the 11th request returns 429 Too Many Requests

  Scenario: Reuse Attack Detection
    Given refresh token A has been rotated to token B
    When POST /api/v1/auth/refresh with token A (reuse)
    Then all user tokens are revoked
```

### SyR-PLAT-02: Data Backbone

```gherkin
Feature: Data Extension
  Scenario: Extend stakeholder with custom fields
    Given stakeholder "CUST-001" exists
    When PATCH /api/v1/data/entities/stakeholder/{id}/extend with { "facebook_url": ... }
    Then stakeholder metadata contains "facebook_url"
```

### SyR-PLAT-03: Event Bus

```gherkin
Feature: Event Publishing & Subscription
  Scenario: Publish and notify subscribers
    Given "vfinance" is subscribed to "SALES_ORDER_CONFIRMED"
    When POST /api/v1/events/publish with event_type "SALES_ORDER_CONFIRMED"
    Then event is logged with subscribers_notified ≥ 1
```

### SyR-PLAT-04: gRPC IPC

```gherkin
Feature: gRPC KernelService
  Scenario: Ping from vApp
    Given gRPC channel to localhost:9090
    When call KernelService.Ping with from="vstrategy"
    Then response status is "UP" and version is present
```

## 6. Flyway Migrations

| Version | File                         | Description                       |
| ------- | ---------------------------- | --------------------------------- |
| V1      | `V1__init_schema.sql`        | Core tables: users, tenants, etc. |
| V2      | `V2__seed_data.sql`          | Currencies + countries seed       |
| V3      | `V3__event_bus.sql`          | Event log + subscriptions tables  |
| V4      | `V4__app_registry.sql`       | App registry + permissions tables |
| V5      | `V5__register_vstrategy.sql` | Auto-register vStrategy           |
| V6      | `V6__auth_hardening.sql`     | Refresh tokens + rate limit log   |

## 7. API Summary

| Method | Path                                       | Auth   | SyR ID        |
| ------ | ------------------------------------------ | ------ | ------------- |
| POST   | `/api/v1/auth/register`                    | Public | SyR-PLAT-01.1 |
| POST   | `/api/v1/auth/login`                       | Public | SyR-PLAT-01.1 |
| POST   | `/api/v1/auth/refresh`                     | Public | SyR-PLAT-01.2 |
| POST   | `/api/v1/auth/logout`                      | JWT    | SyR-PLAT-01.2 |
| GET    | `/api/v1/apps`                             | JWT    | SyR-PLAT-00.0 |
| POST   | `/api/v1/apps/install`                     | JWT    | SyR-PLAT-00.3 |
| DELETE | `/api/v1/apps/{appId}`                     | JWT    | SyR-PLAT-00.3 |
| GET    | `/api/v1/apps/permissions`                 | JWT    | SyR-PLAT-00.4 |
| PATCH  | `/api/v1/data/entities/{type}/{id}/extend` | JWT    | SyR-PLAT-02.1 |
| GET    | `/api/v1/data/currencies`                  | JWT    | SyR-PLAT-02.2 |
| GET    | `/api/v1/data/countries`                   | JWT    | SyR-PLAT-02.2 |
| GET    | `/api/v1/data/tenants`                     | JWT    | SyR-PLAT-02.0 |
| GET    | `/api/v1/data/stakeholders`                | JWT    | SyR-PLAT-02.0 |
| POST   | `/api/v1/events/publish`                   | JWT    | SyR-PLAT-03.0 |
| POST   | `/api/v1/events/subscribe`                 | JWT    | SyR-PLAT-03.1 |
| GET    | `/api/v1/events/subscriptions`             | JWT    | SyR-PLAT-03.2 |
| GET    | `/api/v1/events/log`                       | JWT    | SyR-PLAT-03.2 |
| GET    | `/actuator/health`                         | Public | SyR-PLAT-05.0 |
| GET    | `/actuator/prometheus`                     | Public | SyR-PLAT-05.1 |

## 8. Governance Mapping

| Package     | SyR Mapping | Description                    | GovernanceID |
| ----------- | ----------- | ------------------------------ | ------------ |
| `g0_engine` | SyR-PLAT-00 | App Engine (Install/Lifecycle) | 0.x.x        |
| `g1_iam`    | SyR-PLAT-01 | Identity & Access Mgmt         | 1.x.x        |
| `g2_data`   | SyR-PLAT-02 | Data Backbone + JSONB ext      | 2.x.x        |
| `g3_event`  | SyR-PLAT-03 | Event Bus & Pub/Sub            | 3.x.x        |
| `g4_grpc`   | SyR-PLAT-04 | gRPC IPC Service               | 4.x.x        |
