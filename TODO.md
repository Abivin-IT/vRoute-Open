# TODO — vRoute-Open Platform

> Danh sách task cho các prompt tiếp theo. Mỗi Step = 1 prompt session.
> Lịch sử các step đã hoàn thành xem tại [CHANGELOG.md](CHANGELOG.md).

## Completed

- [x] v1.8.0 — 6 vKernel System Apps (App Store, Settings/IAM, vAudit, vData/MDM, vFlow, vMonitor)
- [x] v1.7.1 — Shared UI consolidation + vMarketing-Org stability
- [x] v1.7.0 — vDesign Physical + vMarketing Org full implementation

## Priority 0 — Domain-Driven Design Refactoring

> **Highest priority.** Chuyển 5 apps từ flat-file sang feature-based DDD.
> Mỗi feature = 1 folder chứa 3 sub-folders: `models/`, `views/`, `controllers/`.
> Shared infra (`config`, `database`, `grpc_client`, `main`) giữ nguyên ở `app/` root.

### Step 0.1: 02-vstrategy — Split `app/` into 5 feature modules

**Current**: flat `app/{models,schemas,routes,service}.py` (3 models, 8 schemas, 12 routes)

**Target structure**:
```
02-vstrategy/app/
├── __init__.py
├── main.py                  # mount all feature routers
├── config.py                # shared
├── database.py              # shared
├── grpc_client.py           # shared
├── plan/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── entity.py        # Plan (SQLAlchemy)
│   │   └── schema.py        # PlanCreate, PlanUpdate, PlanOut
│   ├── views/
│   │   ├── __init__.py
│   │   └── renderer.py      # plan-specific HTML renderers (from renderers.ts)
│   └── controllers/
│       ├── __init__.py
│       ├── routes.py         # GET/POST /plans, GET/PUT /plans/{id}
│       └── service.py        # list_plans, get_plan, create_plan, update_plan
├── alignment/
│   ├── models/
│   │   ├── entity.py        # AlignmentNode
│   │   └── schema.py        # NodeCreate, NodeUpdate, NodeOut
│   ├── views/
│   │   └── renderer.py      # tree & BSC renderers
│   └── controllers/
│       ├── routes.py         # GET /plans/{id}/tree, POST /plans/{id}/nodes, PUT /nodes/{id}, POST /nodes/{id}/propagate
│       └── service.py        # get_tree, add_node, update_node, propagate_status
├── scorecard/
│   ├── models/               # (empty — computed from AlignmentNode)
│   ├── views/
│   │   └── renderer.py      # scorecard renderers
│   └── controllers/
│       ├── routes.py         # GET /plans/{id}/scorecard
│       └── service.py        # get_scorecard
├── sop/
│   ├── models/               # (empty — computed view)
│   ├── views/
│   │   └── renderer.py
│   └── controllers/
│       ├── routes.py         # GET /plans/{id}/sop/validate
│       └── service.py        # validate_sop
└── pivot_signal/
    ├── models/
    │   ├── entity.py        # PivotSignal
    │   └── schema.py        # SignalCheck, SignalOut
    ├── views/
    │   └── renderer.py
    └── controllers/
        ├── routes.py         # GET /plans/{id}/signals, POST /plans/{id}/signals/check
        └── service.py        # get_signals, check_pivot_signal
```

**Tasks**:
- [ ] Create 5 feature folders: `plan/`, `alignment/`, `scorecard/`, `sop/`, `pivot_signal/`
- [ ] Split `models.py` → `Plan` → `plan/models/entity.py`, `AlignmentNode` → `alignment/models/entity.py`, `PivotSignal` → `pivot_signal/models/entity.py`
- [ ] Split `schemas.py` → distribute DTOs to `<feature>/models/schema.py`
- [ ] Split `routes.py` → distribute endpoints to `<feature>/controllers/routes.py`
- [ ] Split `service.py` → distribute functions to `<feature>/controllers/service.py`
- [ ] Move frontend renderers → `<feature>/views/renderer.py` (or keep shared `frontend/` if TS)
- [ ] Update `main.py` — mount 5 feature routers via `app.include_router()`
- [ ] Update `alembic/env.py` — import all entity models for migration discovery
- [ ] Update `tests/` — adjust imports, verify all 19 tests pass
- [ ] `make test` — 0 failures

### Step 0.2: 03-vfinacc — Split `app/` into 5 feature modules

**Current**: flat `app/{models,schemas,routes,service}.py` (5 models, 11 schemas, 17 routes)

**Features → folders**:

| Feature | Folder | Entity | Routes |
|---------|--------|--------|--------|
| Continuous Ledger | `ledger/` | `LedgerEntry` | 5 (CRUD + post) |
| Transaction Ingestor | `transaction/` | `Transaction` | 3 (list, create, get) |
| Reconciliation Engine | `reconciliation/` | `ReconciliationMatch` | 3 (list, run, summary) |
| Cost Center Manager | `cost_center/` | `CostAllocation` | 3 (list, create, summary) |
| Tax & Compliance Guard | `compliance/` | `ComplianceCheck` | 3 (list, check, summary) |

**Tasks**:
- [ ] Create 5 feature folders with `models/`, `views/`, `controllers/` each
- [ ] Split `models.py` → 5 × `entity.py`
- [ ] Split `schemas.py` → 5 × `schema.py`
- [ ] Split `routes.py` → 5 × `routes.py`
- [ ] Split `service.py` → 5 × `service.py`
- [ ] Update `main.py`, `alembic/env.py`, test imports
- [ ] `make test` — 0 failures, 25 tests pass

### Step 0.3: 04-vdesign-physical — Split `app/` into 5 feature modules

**Current**: flat `app/{models,schemas,routes,service}.py` (5 models, 11 schemas, 24 routes)

**Features → folders**:

| Feature | Folder | Entity | Routes |
|---------|--------|--------|--------|
| Spec Master (DF) | `golden_sample/` | `GoldenSample` | 6 (CRUD + seal + compromise) |
| Material Inbox | `material/` | `MaterialInbox` | 4 (list, create, get, scrap) |
| Prototype Versions | `prototype/` | `Prototype` | 4 (list, create, get, retire) |
| Lab Testing | `lab_test/` | `LabTest` | 5 (list, create, summary, get, complete) |
| Handover Kit | `handover_kit/` | `HandoverKit` | 5 (list, create, get, advance, receive) |

**Tasks**:
- [ ] Create 5 feature folders with `models/`, `views/`, `controllers/` each
- [ ] Split monolithic files → per-feature MVC
- [ ] Update `main.py`, `alembic/env.py`, test imports
- [ ] `make test` — 0 failures, 35 tests pass

### Step 0.4: 05-vmarketing-org — Split `app/` into 5 feature modules

**Current**: flat `app/{models,schemas,routes,service}.py` (5 models, 11 schemas, 26 routes)

**Features → folders**:

| Feature | Folder | Entity | Routes |
|---------|--------|--------|--------|
| Campaign Orchestrator | `campaign/` | `Campaign` | 7 (CRUD + launch + pause + complete) |
| Tracking Pixel | `tracking/` | `TrackingEvent` | 4 (list, get, create, intent-summary) |
| Audience Segment | `segment/` | `AudienceSegment` | 4 (list, get, create, archive) |
| Content Asset | `content_asset/` | `ContentAsset` | 5 (list, get, create, publish, archive) |
| Lead Scorer | `lead_score/` | `LeadScore` | 6 (list, get, create, qualify, handoff, disqualify) |

**Tasks**:
- [ ] Create 5 feature folders with `models/`, `views/`, `controllers/` each
- [ ] Split monolithic files → per-feature MVC
- [ ] Update `main.py`, `alembic/env.py`, test imports
- [ ] `make test` — 0 failures, 28 tests pass

### Step 0.5: 01-vkernel (Java) — Add `models/views/controllers` sub-packages

**Current**: `g0_engine/` … `g5_search/` packages đã tách domain, nhưng chưa có MVC sub-structure. Root-level `DashboardController` + `AdaptiveShellController` chưa thuộc package nào.

**Target**: mỗi `gX_*` package có 3 sub-packages:

```
g0_engine/
├── models/
│   ├── AppRegistryEntity.java
│   ├── ManifestModel.java
│   └── PermissionEntity.java
├── views/
│   └── (templates: appstore.html, data.html)
└── controllers/
    ├── AppRegistryController.java
    └── AppLifecycleService.java

g1_iam/
├── models/
│   ├── UserEntity.java
│   ├── OidcAccountEntity.java
│   ├── MagicLinkEntity.java
│   └── RefreshTokenEntity.java
├── views/
│   └── (templates: settings.html, login.html)
└── controllers/
    ├── AuthController.java
    ├── OidcAuthController.java
    ├── MagicLinkController.java
    ├── SecurityConfig.java
    ├── JwtProvider.java
    ├── RefreshTokenService.java
    ├── RateLimitFilter.java
    └── TenantContext.java

g2_data/models/        → StakeholderEntity, CurrencyEntity, CountryEntity, TenantEntity
g2_data/controllers/   → DataExtensionController
g3_event/models/       → EventLogEntity, SubscriptionEntity, KernelEvent
g3_event/controllers/  → EventBusController, EventBusService
g4_grpc/controllers/   → KernelGrpcService
g5_search/models/      → SearchIndexEntity
g5_search/controllers/ → SearchController

g6_shell/              → NEW domain for UI Shell
├── views/             → AdaptiveShellController (serves HTML), all templates/vkernel/*.html
└── controllers/       → DashboardController (API endpoints for system apps)
```

**Tasks**:
- [ ] Create `models/`, `views/`, `controllers/` sub-packages in each `gX_*`
- [ ] Move entities → `models/`, controllers/services → `controllers/`
- [ ] Create `g6_shell` package; move `DashboardController` + `AdaptiveShellController`
- [ ] Update all `import` and `package` declarations
- [ ] Update `SecurityConfig` component scan if needed
- [ ] Update `PlatformApiTests` — adjust imports
- [ ] `make test` — all 65 Java tests pass

### Step 0.6: Frontend alignment (optional)

> TypeScript frontends (`frontend/src/`) đã clean — 4 files/service, không cross-import.
> Split trong từng feature chỉ cần nếu frontend phình to. Hiện tại = **không cần action**.

- [ ] Nếu frontend > 8 files/service → tách `api.ts`, `renderers.ts` vào feature folders
- [ ] Mỗi feature: `views/frontend/{api,renderer,types}.ts`

---

## Next 5 — Odoo End-to-End Parity

> Mỗi task đưa vRoute-Open gần hơn với Odoo end-to-end.
> Odoo reference: `/web/login` → app list → install → use → notify → search.

### 1. SSO Login Gateway Page (Odoo `/web/login`)

- **Gap**: Backend auth hoàn chỉnh (JWT + OIDC + Magic Link), nhưng **chưa có trang Login HTML**.
  Người dùng hiện phải gọi JSON API trực tiếp — không có onboarding flow.
- **Scope**:
  - [ ] `templates/vkernel/login.html` — split-pane Sign In / Sign Up form
  - [ ] Social SSO buttons (Google · Microsoft · GitHub) gọi `/api/v1/auth/oidc/*`
  - [ ] Magic-link tab (nhập email → gửi link)
  - [ ] POST form → nhận JWT → redirect `/shell`
  - [ ] `SecurityConfig` — unauthenticated → redirect `/vkernel/login`
- **Odoo parity**: 60 % → **95 %**

### 2. RBAC Enforcement + Role CRUD (Odoo `ir.model.access` + `ir.rule`)

- **Gap**: Permission registry tồn tại nhưng **không enforce**.
  Tất cả authenticated users có quyền giống nhau. Không có RoleEntity,
  không có role↔permission binding table, không có `@PreAuthorize`.
- **Scope**:
  - [ ] `RoleEntity` + `role_permissions` join table (Flyway migration)
  - [ ] `POST /api/v1/roles` — CRUD roles + assign permissions
  - [ ] `POST /api/v1/apps/permissions` — update role-permission matrix
  - [ ] `@PreAuthorize("hasAuthority('...')")` trên mỗi controller endpoint
  - [ ] Settings UI: Permission Matrix chuyển từ read-only → editable
- **Odoo parity**: 30 % → **80 %**

### 3. WebSocket Notification + Activity Feed (Odoo `mail.thread` / Discuss)

- **Gap**: EventBus backend tồn tại, UI shell có notification bell,
  nhưng **không có WebSocket**, không có NotificationEntity,
  endpoint `/api/v1/notifications/unread-count` mà UI gọi → **404**.
- **Scope**:
  - [ ] `spring-boot-starter-websocket` dependency + `WebSocketConfig`
  - [ ] `NotificationEntity` + `NotificationController` (CRUD + mark-read)
  - [ ] `EventBusService` → `SimpMessagingTemplate.convertAndSendToUser()`
  - [ ] Shell JS: replace polling with STOMP subscribe `/user/queue/notify`
  - [ ] Activity feed panel (Chatter-like) trong mỗi vApp detail page
- **Odoo parity**: 10 % → **75 %**

### 4. Universal Search Cmd+K Overlay (Odoo 17+ Command Palette)

- **Gap**: FTS backend + search box + Ctrl+K shortcut đã có,
  nhưng kết quả chỉ `console.log` — **không có dropdown/overlay UI**.
- **Scope**:
  - [ ] `search-overlay.js` — floating panel dưới search box
  - [ ] Grouped results (Apps · Records · Settings · Actions)
  - [ ] Keyboard navigation (↑↓ Enter Esc)
  - [ ] Deep-link: chọn result → navigate iframe tới vApp page
  - [ ] Recent searches + empty-state hint
- **Odoo parity**: 70 % → **95 %**

### 5. App Bundle Installer + Upgrade (Odoo "Apps" one-click install)

- **Gap**: Install/uninstall single app hoạt động, nhưng
  **bundle one-click** và **version upgrade** chưa có API.
- **Scope**:
  - [ ] `POST /api/v1/apps/bundles` — install bundle by ID (resolve → batch install)
  - [ ] `POST /api/v1/apps/{id}/upgrade` — bump version, re-run migrations
  - [ ] Bundle registry JSON (Manufacturing, Retail, Services bundles)
  - [ ] App Store UI: "Install Bundle" button gọi batch endpoint
  - [ ] Rollback nếu một app trong bundle fail
- **Odoo parity**: 85 % → **95 %**

---

## Backlog

- [ ] vOps, vSales, vHR, vSupport, vProcure, vDev — remaining 6 Business Apps
- [ ] Helm chart for production K8s deployment
