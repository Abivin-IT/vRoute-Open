# Requirements Traceability Matrix

> Source: vKernel PRD Section 3.1

| Req ID         | Requirement Name                   | Source Policy           | Verification Method                           | Priority | Notes                                                       |
| -------------- | ---------------------------------- | ----------------------- | --------------------------------------------- | -------- | ----------------------------------------------------------- |
| SyR-PLAT-00    | App Lifecycle (Dynamic App Engine) | [WATER] 3.2 Code First  | System Test (Install/Uninstall)               | Must     | Core defining requirement                                   |
| SyR-PLAT-00.00 | App Launcher                       | [WATER] 3.2             | UAT                                           | Must     | Central dashboard & access control                          |
| SyR-PLAT-00.01 | App Store                          | [WATER] 3.2             | System Test                                   | Must     | Dependency resolution, security scans                       |
| SyR-PLAT-00.02 | Installation Manager               | [WATER] 3.2             | System Test + Rollback Test                   | Must     | Zero-downtime upgrades, save points                         |
| SyR-PLAT-01    | Unified IAM                        | [AIR] 3. Agent Identity | Security Test (Pen-test)                      | Must     | Security & SSO baseline                                     |
| SyR-PLAT-01.00 | Unified Authentication (AuthN)     | [AIR] 3.                | Pen-test + SSO Test                           | Must     | Centralized SSO, Magic Link, OIDC                           |
| SyR-PLAT-01.01 | Role-Based Authorization (AuthZ)   | [AIR] 3.                | Security Audit                                | Must     | WHO Codes, global role governance                           |
| SyR-PLAT-01.02 | Dynamic Permission Injection       | [AIR] 3.                | Integration Test                              | Must     | App injects permissions on install                          |
| SyR-PLAT-02    | Data Backbone                      | [EARTH] 6. Database     | Data Integrity Check                          | Must     | No silos — critical                                         |
| SyR-PLAT-02.00 | Core Entities & Stakeholder Mgmt   | [EARTH] 6.              | Data Integrity Check                          | Must     | Golden Records (Users, Stakeholders, Currencies, Countries) |
| SyR-PLAT-02.01 | Dynamic JSONB Fields               | [EARTH] 6.              | Integration Test                              | Must     | Extend entities without schema changes                      |
| SyR-PLAT-02.02 | Universal Search                   | [EARTH] 6.              | Performance Test                              | Must     | Postgres FTS, cross-App search                              |
| SyR-PLAT-03    | Event Bus & Automation (IPC)       | [WATER] 3. Process Arch | Integration Test                              | Must     | Automation foundation                                       |
| SyR-PLAT-03.01 | Event Registry                     | [WATER] 3.              | Integration Test                              | Must     | Standard event catalog                                      |
| SyR-PLAT-03.02 | Subscription Engine (Pub/Sub)      | [WATER] 3.              | Integration Test                              | Must     | Cross-app event subscriptions                               |
| SyR-PLAT-03.03 | Audit Trail Logging                | [WATER] 3.              | Security Audit                                | Must     | Immutable IPC transaction log                               |
| SyR-PLAT-04    | Adaptive UI Shell                  | [AIR] 6. Standards      | UAT (User Acceptance)                         | Must     | Unified UX                                                  |
| SyR-PLAT-04.01 | Dynamic Navigation Rail            | [AIR] 6.                | UAT                                           | Must     | Persistent left sidebar                                     |
| SyR-PLAT-04.02 | Unified Notification Center        | [AIR] 6.                | UAT                                           | Must     | Aggregated bell icon stream                                 |
| SyR-PLAT-04.03 | Command Palette (CLI UI)           | [AIR] 6.                | UAT                                           | Must     | AI Agent command execution                                  |
| NFR-PLAT-01    | Performance                        | —                       | Benchmark                                     | Must     | <10s install, <300ms query                                  |
| NFR-PLAT-02    | Reliability & Availability         | [WATER]                 | Chaos Testing                                 | Must     | Zero-downtime, 99.9% uptime                                 |
| NFR-PLAT-03    | Security & Compliance              | [WATER]                 | Pen-test + Compliance Check                   | Must     | ISO 27001, ND123, RBAC on every req                         |
| NFR-PLAT-04    | Scalability                        | —                       | Load Test                                     | Later    | 1,000 concurrent users                                      |
| NFR-PLAT-05    | Data Isolation & Secure Access     | [EARTH] 6 + [AIR] 3     | Security Audit + RLS Test + Cross-Tenant Test | Must     | Separate DB per tenant, API-only access                     |
