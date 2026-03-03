# TODO — vRoute-Open Platform

> Danh sách task cho các prompt tiếp theo. Mỗi Step = 1 prompt session.
> Lịch sử các step đã hoàn thành xem tại [CHANGELOG.md](CHANGELOG.md).

## Completed

- [x] v1.9.0 — DDD refactoring (5 apps → feature-based MVC) + Sheets restructuring (cross-app tables)
- [x] v1.8.1 — UI Refactor (sidebar, home launcher, dashboard redirect)
- [x] v1.8.0 — 6 vKernel System Apps (App Store, Settings/IAM, vAudit, vData/MDM, vFlow, vMonitor)
- [x] v1.7.1 — Shared UI consolidation + vMarketing-Org stability
- [x] v1.7.0 — vDesign Physical + vMarketing Org full implementation

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
