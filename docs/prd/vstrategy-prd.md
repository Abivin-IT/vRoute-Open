# vStrategy PRD — S2P2R Module

> **Document ID:** `0.0.0-C4-SPEC-CPO-vapp-vstrategy-prd`
> **Version:** 1.1 (aligned with FIRE Policy v1.0)
> **Status:** APPROVED
> **Owner:** CPO
> **Tech Stack:** React (FE) | Java Spring (BE) | PostgreSQL (via Kernel Data Backbone)
> **Policy Ref:** [FIRE] A1-POL-FIRE-STRATEGY (S2P2R Cycle)

---

## 1. Introduction

### 1.1. Purpose

vStrategy thực thi quy trình Strategy-to-Plan-to-Report (S2P2R) theo FIRE Policy, đảm bảo tầm nhìn công ty được chuyển hóa thành kế hoạch đo lường được (OKR/BSC), phân bổ nguồn lực (68/27/5), và báo cáo variance real-time với pivot signal khi vượt ngưỡng.

### 1.2. Scope

- **In Scope:** 5 bước S2P2R, Alignment Tree, OKR/BSC, Resource Allocation, Scorecard & Pivot Triggers.
- **Out of Scope:** Detailed project execution (vBuild), financial actuals & close (vAccounting).

### 1.3. Definitions

| Term             | Definition                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| S2P2R Cycle      | 13-week Quarterly Rhythm + Monthly Pulse + Threshold triggers (Runway <6 tháng, Revenue drop >20%) |
| BSC Perspectives | Finance, Customer, Internal Process, Org Capacity                                                  |
| Traffic Light    | Green (>90%), Yellow (70–90%), Red (<70%)                                                          |

### 1.4. Problem & Opportunity

**Problem:**

- **Strategic Drift:** Chiến lược nằm trên giấy, không liên kết với execution
- **Vertical Silos:** Phòng ban tự đặt KPI riêng
- **Blind Execution:** Không có cơ chế phát hiện sớm
- **Resource Misallocation:** Ngân sách chi tiêu theo cảm tính

**Opportunity:**

- Real-time Alignment Tree: Vision → Targets → Task, status tự động propagate
- Threshold-driven Pivot Signals
- 68/27/5 Auto-enforcement
- MECE Decision Framework (Growth/Profit/Pivot/Survival)

### 1.5. User Personas

| Persona             | Role         | Needs                                                   | Pain Points                      |
| ------------------- | ------------ | ------------------------------------------------------- | -------------------------------- |
| CEO (The Architect) | WHO: CEO     | "God Mode" view toàn bộ Alignment Tree và Pivot Signals | Chậm ra quyết định Pivot         |
| CAO (The Conductor) | WHO: CAO     | Công cụ điều phối 13 tuần, enforce 68/27/5              | Chase status update từ phòng ban |
| CPO/CMO (Executors) | WHO: CPO/CMO | Clear OKRs, theo dõi tiến độ real-time                  | Không rõ daily work đóng góp gì  |

---

## 2. System Architecture

vStrategy = Business App chạy trên vKernel. Không tự quản lý DB riêng — sử dụng Core Entities DB.

```
vSTRATEGY MODULE
├── Alignment Tree Engine (FE)
├── S&OP Planning Service (BE)
└── Scorecard & Analytics (BE)
         │
    VKERNEL CORE PLATFORM
    ├── Data Service (Core Entities)
    └── Event Bus Service (IPC)
         │
    CORE STORAGE
    ├── PostgreSQL (shared DB)
    └── Event Store (audit trail)
```

---

## 3. System Requirements

### 3.1. Requirements Traceability Matrix

| Req ID     | Name                                    | FIRE Step | Priority |
| ---------- | --------------------------------------- | --------- | -------- |
| SyR-STR-00 | Alignment Tree & Goal Establishment     | Step 3    | Must     |
| SyR-STR-01 | Contextual Baseline & Objectives        | Step 1    | Must     |
| SyR-STR-02 | Strategic Analysis & Solution Selection | Step 2    | Must     |
| SyR-STR-03 | Integrated S&OP & Resource Allocation   | Step 4    | Must     |
| SyR-STR-04 | Performance Review & Variance Analysis  | Step 5    | Must     |

### 3.2. SyR-STR-00: Alignment Tree Engine

- Vision (A1) ↔ OKR/BSC (A2) ↔ Key Initiatives (A3) ↔ Tasks (A4)
- Status change propagates upward to Vision
- Tree view: % completion, BSC perspectives, traffic light, Pivot Signal

### 3.3. SyR-STR-01: Contextual Baseline & Objectives

- Trigger: Scheduled (Dec 15, Quarterly 20th, Monthly 25th) + Threshold
- Baseline: Fiscal Constraints, Hard Cap
- Objectives: Market Hypothesis, ICP, USP

### 3.4. SyR-STR-02: Strategic Analysis & Solution Selection

- Gap Analysis (As-Is vs To-Be) + PESTLE/ADHR
- 4 MECE Options: Growth, Profit, Pivot, Survival
- CEO Decision Log

### 3.5. SyR-STR-03: S&OP & Resource Allocation

- Enforce 68% GROW (CMO), 27% RUN (CAO), 5% TRANSFORM (CPO), ~0.1% GIVE (CEO)
- Key Initiatives, Budget Allocation, Headcount Plan
- Validation with ±2% tolerance

### 3.6. SyR-STR-04: Performance Review & Variance

- Variance Actual vs Plan
- Traffic Light status
- Pivot Signal: Runway <6 months, Revenue drop >20%

---

## 4. NFRs

- **Performance:** Tree render <1.5s, variance calculation <2s
- **Reliability:** 100% propagation via Kernel Event Bus
- **Security:** Vision/Objectives edit chỉ CEO, full audit trail

---

## 5. Acceptance Criteria (Gherkin Sample)

```gherkin
Scenario: Task Red propagates to Vision & triggers Pivot Signal
  Given OKR-001 (Finance) → Initiative-01 → Task-002 (Green)
  And current revenue drop 22% (threshold triggered)
  When Task-002 status changed to Red
  Then Initiative-01 → Yellow, OKR-001 → Red, Vision → Red
  And event OKR_STATUS_CHANGED published upward
  And CEO notified: "Critical Pivot Trigger: Revenue drop >20%"
  And Strategic Analysis auto-triggered (Step 2)
```

---

## 6. Manifest.json

```json
{
  "app": {
    "id": "com.vcorp.vstrategy",
    "name": "vStrategy",
    "version": "1.0.0"
  },
  "permissions": [
    { "code": "strategy.vision.edit", "default_roles": ["CEO"] },
    {
      "code": "strategy.scorecard.view",
      "default_roles": ["CEO", "CAO", "CMO", "CPO"]
    }
  ],
  "events": {
    "published": [
      "OKR_STATUS_CHANGED",
      "PIVOT_SIGNAL_RAISED",
      "SOP_PLAN_APPROVED"
    ],
    "subscribed": ["MONTHLY_CLOSE_COMPLETED"]
  }
}
```
