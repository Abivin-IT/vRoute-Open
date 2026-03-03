# Requirements Traceability Matrix

> Cross-app requirements registry. Sources: all 5 PRDs (§3.1).
> Total: **45 requirements** across 5 apps.

## Functional Requirements

| #   | App              | Req ID         | Requirement Name                        | Source Policy             | Verification Method             | Priority | Process Cycle |
| --- | ---------------- | -------------- | --------------------------------------- | ------------------------- | ------------------------------- | -------- | ------------- |
| 1   | vKernel          | SyR-PLAT-00    | App Lifecycle (Dynamic App Engine)      | [WATER] 3.2 Code First    | System Test (Install/Uninstall) | Must     | Platform      |
| 2   | vKernel          | SyR-PLAT-00.00 | App Launcher                            | [WATER] 3.2               | UAT                             | Must     | Platform      |
| 3   | vKernel          | SyR-PLAT-00.01 | App Store                               | [WATER] 3.2               | System Test                     | Must     | Platform      |
| 4   | vKernel          | SyR-PLAT-00.02 | Installation Manager                    | [WATER] 3.2               | System Test + Rollback Test     | Must     | Platform      |
| 5   | vKernel          | SyR-PLAT-01    | Unified IAM                             | [AIR] 3. Agent Identity   | Security Test (Pen-test)        | Must     | Platform      |
| 6   | vKernel          | SyR-PLAT-01.00 | Unified Authentication (AuthN)          | [AIR] 3.                  | Pen-test + SSO Test             | Must     | Platform      |
| 7   | vKernel          | SyR-PLAT-01.01 | Role-Based Authorization (AuthZ)        | [AIR] 3.                  | Security Audit                  | Must     | Platform      |
| 8   | vKernel          | SyR-PLAT-01.02 | Dynamic Permission Injection            | [AIR] 3.                  | Integration Test                | Must     | Platform      |
| 9   | vKernel          | SyR-PLAT-02    | Data Backbone                           | [EARTH] 6. Database       | Data Integrity Check            | Must     | Platform      |
| 10  | vKernel          | SyR-PLAT-02.00 | Core Entities & Stakeholder Mgmt        | [EARTH] 6.                | Data Integrity Check            | Must     | Platform      |
| 11  | vKernel          | SyR-PLAT-02.01 | Dynamic JSONB Fields                    | [EARTH] 6.                | Integration Test                | Must     | Platform      |
| 12  | vKernel          | SyR-PLAT-02.02 | Universal Search                        | [EARTH] 6.                | Performance Test                | Must     | Platform      |
| 13  | vKernel          | SyR-PLAT-03    | Event Bus & Automation (IPC)            | [WATER] 3. Process Arch   | Integration Test                | Must     | Platform      |
| 14  | vKernel          | SyR-PLAT-03.01 | Event Registry                          | [WATER] 3.                | Integration Test                | Must     | Platform      |
| 15  | vKernel          | SyR-PLAT-03.02 | Subscription Engine (Pub/Sub)           | [WATER] 3.                | Integration Test                | Must     | Platform      |
| 16  | vKernel          | SyR-PLAT-03.03 | Audit Trail Logging                     | [WATER] 3.                | Security Audit                  | Must     | Platform      |
| 17  | vKernel          | SyR-PLAT-04    | Adaptive UI Shell                       | [AIR] 6. Standards        | UAT (User Acceptance)           | Must     | Platform      |
| 18  | vKernel          | SyR-PLAT-04.01 | Dynamic Navigation Rail                 | [AIR] 6.                  | UAT                             | Must     | Platform      |
| 19  | vKernel          | SyR-PLAT-04.02 | Unified Notification Center             | [AIR] 6.                  | UAT                             | Must     | Platform      |
| 20  | vKernel          | SyR-PLAT-04.03 | Command Palette (CLI UI)                | [AIR] 6.                  | UAT                             | Must     | Platform      |
| 21  | vStrategy        | SyR-STR-00     | Alignment Tree & Goal Establishment     | vstrategy-prd §3.1        | System Test                     | Must     | S2P2R         |
| 22  | vStrategy        | SyR-STR-01     | Contextual Baseline & Objectives        | vstrategy-prd §3.1        | System Test                     | Must     | S2P2R         |
| 23  | vStrategy        | SyR-STR-02     | Strategic Analysis & Solution Selection | vstrategy-prd §3.1        | System Test                     | Must     | S2P2R         |
| 24  | vStrategy        | SyR-STR-03     | Integrated S&OP & Resource Allocation   | vstrategy-prd §3.1        | System Test                     | Must     | S2P2R         |
| 25  | vStrategy        | SyR-STR-04     | Performance Review & Variance Analysis  | vstrategy-prd §3.1        | System Test                     | Must     | S2P2R         |
| 26  | vFinacc          | SyR-FIN-00     | Continuous Ledger                       | vfinacc-prd §3.1          | Integration Test                | Must     | R2R           |
| 27  | vFinacc          | SyR-FIN-01     | Transaction Ingestor                    | vfinacc-prd §3.1          | Integration Test                | Must     | R2R           |
| 28  | vFinacc          | SyR-FIN-02     | Reconciliation Engine (3-Way Match)     | vfinacc-prd §3.1          | Integration Test                | Must     | R2R           |
| 29  | vFinacc          | SyR-FIN-03     | Cost Center Manager                     | vfinacc-prd §3.1          | Integration Test                | Must     | R2R           |
| 30  | vFinacc          | SyR-FIN-04     | Tax & Compliance Guard                  | vfinacc-prd §3.1          | Compliance Check                | Must     | R2R           |
| 31  | vDesign Physical | SyR-PHY-00     | Spec Master (Golden Sample Vault)       | vdesign-physical-prd §3.1 | Metrology Scan (CMM)            | Must     | I2S Physical  |
| 32  | vDesign Physical | SyR-PHY-01     | Idea Inbox (Material Inbox)             | vdesign-physical-prd §3.1 | Visual Inspection               | Must     | I2S Physical  |
| 33  | vDesign Physical | SyR-PHY-02     | Version Control (Prototypes)            | vdesign-physical-prd §3.1 | RFID Tracking                   | Must     | I2S Physical  |
| 34  | vDesign Physical | SyR-PHY-03     | Feasibility Checker (Lab Testing)       | vdesign-physical-prd §3.1 | Stress/Drop Testing             | Must     | I2S Physical  |
| 35  | vDesign Physical | SyR-PHY-04     | Handover Kit (Tooling)                  | vdesign-physical-prd §3.1 | Physical Inventory Check        | Must     | I2S Physical  |
| 36  | vMarketing Org   | SyR-MKT-ORG-00 | Campaign Orchestrator                   | vmarketing-org-prd §3.1   | System Test: multi-channel      | Must     | M2L ABM       |
| 37  | vMarketing Org   | SyR-MKT-ORG-01 | Tracking Pixel                          | vmarketing-org-prd §3.1   | UAT: real user event capture    | Must     | M2L ABM       |
| 38  | vMarketing Org   | SyR-MKT-ORG-02 | Audience Segment                        | vmarketing-org-prd §3.1   | Logic Test: filter validation   | Must     | M2L ABM       |
| 39  | vMarketing Org   | SyR-MKT-ORG-03 | Content Asset                           | vmarketing-org-prd §3.1   | System Test: media management   | Must     | M2L ABM       |
| 40  | vMarketing Org   | SyR-MKT-ORG-04 | Lead Scorer                             | vmarketing-org-prd §3.1   | Benchmark: AI Lead Grading      | Must     | M2L ABM       |

## Non-Functional Requirements

| #   | App     | NFR ID      | Name                       | Metric                    | Target                   | Verification         | Priority |
| --- | ------- | ----------- | -------------------------- | ------------------------- | ------------------------ | -------------------- | -------- |
| 41  | vKernel | NFR-PLAT-01 | Performance                | App install time (p95)    | < 10 seconds             | Benchmark            | Must     |
| 42  | vKernel | NFR-PLAT-02 | Reliability & Availability | Platform uptime (monthly) | >= 99.9%                 | Chaos Testing        | Must     |
| 43  | vKernel | NFR-PLAT-03 | Security & Compliance      | RBAC enforcement          | Every request validated  | Pen-test             | Must     |
| 44  | vKernel | NFR-PLAT-04 | Scalability                | Concurrent users          | 1,000 with < 1s response | Load Test            | Later    |
| 45  | vKernel | NFR-PLAT-05 | Data Isolation             | Database isolation        | Separate DB per Tenant   | Security Audit + RLS | Must     |

## Summary

| App              | Process Cycle | Functional Reqs | NFR Reqs | Total  |
| ---------------- | ------------- | --------------- | -------- | ------ |
| vKernel          | Platform      | 20              | 5        | 25     |
| vStrategy        | S2P2R         | 5               | —        | 5      |
| vFinacc          | R2R           | 5               | —        | 5      |
| vDesign Physical | I2S Physical  | 5               | —        | 5      |
| vMarketing Org   | M2L ABM       | 5               | —        | 5      |
| **Total**        |               | **40**          | **5**    | **45** |
