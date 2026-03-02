# Acceptance Criteria (Flat Table)

> Source: vKernel PRD Section 6 — All Gherkin scenarios extracted as a flat reference table.

| # | Req Group | Feature | Scenario | Given | When | Then |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | SyR-PLAT-00 | App Manifest Parsing | Parse valid manifest.json | Valid manifest.json for "vSales" with name, version 2.1.0, deps ["vContacts"], menu structure | System parses manifest during installation | App metadata stored; dependencies registered; menu items queued for UI Shell injection |
| 2 | SyR-PLAT-00 | App Manifest Parsing | Reject invalid manifest.json | manifest.json missing required field "name" | System attempts to parse it | Installation fails with "Invalid manifest: missing name"; no partial install; error logged |
| 3 | SyR-PLAT-00 | Dependency Resolution | Auto-prompt for missing dependencies | vSales requires "vContacts" (not installed) | Admin clicks "Install vSales" | System detects missing dep; popup: "vSales requires vContacts. Install both?"; [Cancel] + [Install Both] |
| 4 | SyR-PLAT-00 | Dependency Resolution | Install both when confirmed | Dependency popup shown for vSales → vContacts | Admin clicks [Install Both] | vContacts installs first; vSales installs after; total < 15s; success notification |
| 5 | SyR-PLAT-00 | Version Control & Rollback | Successful rollback | vFinance v2.0 running; v2.1 causes error | Admin selects "Rollback to v2.0" | Reverts to v2.0 manifest + code; active in < 5s; data integrity preserved; rollback logged |
| 6 | SyR-PLAT-00 | Version Control & Rollback | Rollback fails (incompatible data) | Rollback to v1.0 would break schema | Admin attempts rollback | System blocks; warning: "Rollback to v1.0 incompatible with current data schema"; suggests migration |
| 7 | SyR-PLAT-01 | Centralized AuthN | Successful SSO login across Apps | User "nguyenvana" with role FAM logs in via OIDC | User navigates vFinance → vSales | No additional login; session token propagated; access granted based on global role |
| 8 | SyR-PLAT-01 | Centralized AuthN | Session expiration and re-auth | User idle > 30 min (configurable) | User tries to access vHR | Redirect to login page; previous session invalidated |
| 9 | SyR-PLAT-01 | Granular AuthZ | New role created and propagated | Admin creates role "Sales Lead" | vSales is installed | "Sales Lead" appears in Permission Matrix for vSales; default permissions applied (read-only) |
| 10 | SyR-PLAT-01 | Permission Injection | App injects permissions on install | vFinance is being installed | Installation completes | "finance.invoice.approve" added to AuthZ; roles can be granted via matrix; no duplicates |
| 11 | SyR-PLAT-01 | Permission Injection | Permission removal on uninstall | vFinance is uninstalled | Uninstall completes | All vFinance permissions removed from registry; roles retain only core permissions |
| 12 | SyR-PLAT-02 | Core Entities | Reference Golden Record without duplication | Company "Abivin" exists in core entities | vSales creates a new Deal for Abivin | References same core Company ID; no duplicate Company record in vSales |
| 13 | SyR-PLAT-02 | Dynamic JSONB Fields | Extend core entity with JSONB | Company table has metadata JSONB column | vMarketing installs and adds "facebook_url" | New records store facebook_url in metadata; existing records intact; vFinance adds "tax_code" independently |
| 14 | SyR-PLAT-02 | Dynamic JSONB Fields | Query extended field cross-App | Company has metadata {"facebook_url": "fb.com/abivin"} | User searches "facebook_url:fb.com/abivin" in Global Search | Returns Company record correctly |
| 15 | SyR-PLAT-02 | Universal Search | Global search returns cross-App results | Data exists in vSales, vFinance, vHR for "Abivin" | User types "Abivin" in Cmd+K search | Results grouped by App; top result highlighted; search time < 500ms |
| 16 | SyR-PLAT-03 | Event Registry | Publish standard event | vSales publishes "ORDER_CONFIRMED" | Event is emitted | Registered in Event Registry with payload schema validation; persisted for audit |
| 17 | SyR-PLAT-03 | Subscription Engine | Successful event subscription and trigger | vFinance subscribes to "ORDER_CONFIRMED" | vSales publishes ORDER_CONFIRMED {deal_id: 9021, amount: 5000} | vFinance receives event < 1s; CREATE_INV_DRAFT triggered; Invoice draft created (ref_id: 9021) |
| 18 | SyR-PLAT-03 | Audit Trail Logging | Log every IPC transaction | Event is published and consumed | Processing completes | Audit log records: timestamp, source, target, event type, payload hash, status; immutable & queryable |
| 19 | SyR-PLAT-04 | Dynamic Navigation Rail | Sidebar updates on App install | Only vFinance installed | vSales installed successfully | vSales icon appears in Left Sidebar; position respects install order/priority |
| 20 | SyR-PLAT-04 | Unified Notification Center | Aggregate notifications | vFinance: "Invoice Overdue"; vSales: "Deal Won" | User clicks Bell icon | Notifications in one stream, sorted by urgency (High first); clicking opens relevant App record |
| 21 | SyR-PLAT-04 | Command Palette (CLI UI) | Execute command via Command Palette | User types "/finance check-balance" in Cmd+K | Command is executed | Routes to vFinance balance check; result displayed inline or opens relevant page |

## Summary

| Req Group | Feature Count | Scenario Count |
| --- | --- | --- |
| SyR-PLAT-00 (App Engine) | 3 | 6 |
| SyR-PLAT-01 (IAM) | 3 | 5 |
| SyR-PLAT-02 (Data Backbone) | 3 | 4 |
| SyR-PLAT-03 (IPC/Event Bus) | 3 | 3 |
| SyR-PLAT-04 (UI Shell) | 3 | 3 |
| **Total** | **15** | **21** |
