# Product Requirements Document: vFinance (R2R Module)

> **Document ID:** 0.0.0-C4-SPEC-CPO-vapp-vfinance-prd
> **Version:** 1.0 (Aligned with R2R Policy v1.0)
> **Status:** APPROVED
> **Owner:** CPO / Head of Finance
> **Tech Stack:** React (FE) | Python FastAPI (BE) | vKernel AI Agent (Anomaly Detection)
> **Policy Ref:** [R2R] Record-to-Report Cycle

---

## 1. Introduction

### 1.1. Purpose

vFinance thực thi quy trình Record-to-Report (R2R), đảm bảo sức khỏe tài chính của doanh nghiệp được ghi nhận minh bạch và báo cáo tức thời. Hệ thống chuyển dịch từ mô hình kế toán truyền thống "chờ cuối tháng chốt sổ" sang mô hình **Continuous Accounting** (Kế toán liên tục), nơi mọi giao dịch được xử lý real-time.

### 1.2. Scope

- **In Scope:** 5 thành phần cốt lõi của R2R — Continuous Ledger, Transaction Ingestion, Reconciliation, Cost Allocation, Tax/Compliance.
- **Out of Scope:** Lập kế hoạch ngân sách (thuộc vStrategy), Quản lý kho bãi vật lý (thuộc vOps).

### 1.3. Problem & Opportunity

- **Vấn đề:** Doanh nghiệp bị "mù thông tin tài chính" trong suốt tháng do độ trễ của việc nhập liệu và đối soát thủ công. Quyết định chiến lược thường dựa trên dữ liệu quá khứ (lagging indicators).
- **Cơ hội:** Tự động hóa 95% tác vụ nhập liệu và đối soát bằng AI, cung cấp "Real-time Financial Signal" để ban lãnh đạo điều chỉnh chiến lược ngay lập tức.

---

## 2. System Architecture Overview

```
+--------------------------------------------------------------------------------------------------------------+
|                                     VFINANCE MODULE (RECORD-TO-REPORT)                                       |
+--------------------------------------------------------------------------------------------------------------+
|       +---------------------------- [DF] CONTINUOUS LEDGER ENGINE ----------------------------+              |
|       | (Real-time General Ledger & Sub-ledgers with Draft/Posted/Flagged states)             |              |
|       +---------------------------------------------------------------------------------------+              |
|                ^                       ^                        ^                       ^                    |
|      +----------------------+ +----------------------+ +----------------------+ +----------------------+     |
|      | [SR1] Transaction    | | [SR2] AI             | | [SR3] Cost Center    | | [SR4] Tax & Compliance|    |
|      | Ingestor Engine      | | Reconciliation Eng.  | | Management Engine    | | Guard (ML Powered)    |    |
|      +----------------------+ +----------------------+ +----------------------+ +----------------------+     |
+--------------------------------------------------------------------------------------------------------------+
|                                           VKERNEL CORE PLATFORM                                              |
|      +-----------------------------------+              +------------------------------------------+         |
|      | Data Service (Golden Records)     | <----------> | Event Bus Service (IPC & Pub/Sub)        |         |
|      +-----------------------------------+              +------------------------------------------+         |
+--------------------------------------------------------------------------------------------------------------+
```

**Kiến trúc vFinance** được thiết kế theo hướng Event-Driven (Hướng sự kiện) để xử lý lượng lớn giao dịch tài chính với độ trễ thấp nhất.

---

## 3. System Requirements

### 3.1. Requirements Traceability Matrix

| Req ID     | Requirement Name       | Source Policy                      | Priority |
| ---------- | ---------------------- | ---------------------------------- | -------- |
| SyR-FIN-00 | Continuous Ledger (DF) | R2R Policy - Real-time Reporting   | Must     |
| SyR-FIN-01 | Transaction Ingestor   | R2R Policy - Auto Data Entry       | Must     |
| SyR-FIN-02 | Reconciliation Engine  | R2R Policy - 3-Way Matching        | Must     |
| SyR-FIN-03 | Cost Center Manager    | R2R Policy - Automated Allocation  | Must     |
| SyR-FIN-04 | Tax & Compliance Guard | R2R Policy - Regulatory Compliance | Must     |

### 3.2. [DF] SyR-FIN-00: Continuous Ledger Engine

**Goal:** Xây dựng Sổ cái liên tục: Transaction → Journal Entry → General Ledger → Financial Reports.

- Hệ thống hỗ trợ liên kết: Transaction (A1) → Journal Entry (A2) → General Ledger (A3) → Financial Reports (A4).
- Thay đổi trạng thái (ví dụ: Giao dịch bị Flag) phải kích hoạt sự kiện `STATUS_CHANGED` lan truyền ngược lên báo cáo tổng hợp.
- Dashboard hiển thị % hoàn thành đối soát, góc nhìn tài chính, tín hiệu Pivot chiến lược.

### 3.3. [SR-01] SyR-FIN-01: Transaction Ingestor Engine

**Goal:** Cổng tiếp nhận dữ liệu từ External API (Bank) → Raw Transaction → Data Buffer → Draft Entry.

- Kích hoạt thu thập baseline theo lịch trình (Scheduled) hoặc khi Runway < 6 tháng.
- Dashboard hiển thị trạng thái kết nối các cảm biến dữ liệu, cảnh báo mất kết nối.

### 3.4. [SR-02] SyR-FIN-02: AI-Powered Reconciliation Engine

**Goal:** Đối soát 3 chiều: Purchase Order (P1) → Goods Receipt Note (P2) → Invoice (P3).

- Khi phát hiện sai lệch (Gap), hệ thống tự động đề xuất 4 phương án MECE.
- Dashboard hiển thị tỷ lệ đối soát tự động thành công và phân tích khoảng cách.

### 3.5. [SR-03] SyR-FIN-03: Cost Center Manager

**Goal:** Thực thi phân bổ chi phí theo GROW (68%), RUN (27%), TRANSFORM (5%), GIVE (~0.1%).

- Mọi khoản chi được phê duyệt phải tự động trừ vào ngân sách Cost Center tương ứng.
- Dashboard hiển thị Master Allocation Matrix, so sánh chi tiêu thực tế với định mức.

### 3.6. [SR-04] SyR-FIN-04: Tax & Compliance Guard

**Goal:** Transaction Stream → Compliance Rule → Tax Accrual → Variance Report.

- Biến động doanh thu phải đối soát với kế hoạch; sai lệch vượt ngưỡng phát tín hiệu Pivot Signal.
- Dashboard hiển thị báo cáo Variance, tín hiệu đèn giao thông, xuất báo cáo định kỳ.

---

## 4. Non-Functional Requirements (NFRs)

### NFR-FIN-00 | Security

- RBAC + Re-Auth trên mọi API liên ứng dụng.
- AES-256 encryption cho dữ liệu tài chính nhạy cảm.

### NFR-FIN-01 | Reliability & Safety

- Data Integrity với sai số Zero Drift.
- Uptime ≥ 99.9% hàng tháng.

### NFR-FIN-02 | Performance

- Truy vấn đối soát chéo < 300ms (p99).
- Hot-swap nâng cấp < 10 giây (p95).

### NFR-FIN-03 | Interaction Capability

- Truy cập dữ liệu tài chính chỉ qua Public APIs trong manifest.json.
- Scope visibility cho trường mở rộng (tax_code) chỉ cho vFinance.

### NFR-FIN-04 | Maintainability

- Sẵn sàng tuân thủ hóa đơn điện tử theo Nghị định 123.
- Horizontal scaling qua Kubernetes.

---

## 5. Technical Specifications

```json
{
  "app": { "id": "com.vcorp.vfinacc", "name": "vFinance", "version": "1.0.0" },
  "dependencies": ["com.vcorp.vkernel:^1.0.0", "com.vcorp.vsales:^1.0.0"],
  "permissions": [
    { "code": "finance.ledger.view", "default_roles": ["CEO", "CFO"] },
    { "code": "finance.ledger.post", "default_roles": ["CFO", "ACC_MGR"] },
    {
      "code": "finance.transaction.approve",
      "default_roles": ["CFO", "ACC_MGR"]
    },
    { "code": "finance.compliance.manage", "default_roles": ["CFO", "TAX_MGR"] }
  ],
  "events": {
    "published": [
      "TRANSACTION_POSTED",
      "BUDGET_OVERRUN_ALERT",
      "RECON_COMPLETED",
      "COMPLIANCE_VIOLATION"
    ],
    "subscribed": ["SALES_INVOICE_CREATED", "PROCUREMENT_PO_APPROVED"]
  }
}
```

## 6. Acceptance Criteria (Sample Gherkin)

```gherkin
Scenario: Giao dịch mua hàng được tự động đối soát và ghi nhận
  Given Một PO đã được duyệt cho AWS với giá trị $2,400.
  When Hệ thống Ingestor nhận được Invoice điện tử từ AWS với cùng giá trị.
  And Reconciliation Engine xác nhận 3-way match hợp lệ.
  Then Giao dịch chuyển trạng thái từ "Draft" sang "Posted" trong Continuous Ledger.
  And Chi phí $2,400 phân bổ vào Cost Center "R&D - Infrastructure".
  And Hệ thống tính toán thuế nhà thầu liên quan (nếu có).
```
