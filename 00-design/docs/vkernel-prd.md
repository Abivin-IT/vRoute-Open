# PRODUCT REQUIREMENTS DOCUMENT: vRoute Core OS (vKernel)

> **Document ID:** `0.0.0-C4-SPEC-CPO-platform-kernel-prd`
> **Version:** 1.0
> **Status:** APPROVED
> **Owner:** CPO (Chief Product Officer)
> **Tech Stack:** React (FE) | Java Spring (BE) | PostgreSQL (DB) | Kubernetes
> **Policy Ref:** [EARTH] A1-POL-EARTH | [FIRE] A1-POL-FIRE

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Scope](#12-scope)
   - 1.3 [Definitions](#13-definitions)
   - 1.4 [Problem & Opportunity + User Personas & Key Journeys](#14-problem--opportunity--user-personas--key-journeys)
2. [System Architecture Overview](#2-system-architecture-overview)
   - 2.1 [Architecture Diagram](#21-architecture-diagram)
   - 2.2 [Architecture Explanation](#22-architecture-explanation)
3. [System Requirements](#3-system-requirements)
   - 3.1 [Requirements Traceability Matrix](#31-requirements-traceability-matrix)
   - 3.2 [SyR-PLAT-00 — The Dynamic App Engine](#32-syr-plat-00--the-dynamic-app-engine)
   - 3.3 [SyR-PLAT-01 — Identity & Access Management (IAM)](#33-syr-plat-01--identity--access-management-iam)
   - 3.4 [SyR-PLAT-02 — Universal Data Backbone](#34-syr-plat-02--universal-data-backbone)
   - 3.5 [SyR-PLAT-03 — Inter-process Communication (IPC)](#35-syr-plat-03--inter-process-communication-ipc)
   - 3.6 [SyR-PLAT-04 — Adaptive UI Shell](#36-syr-plat-04--adaptive-ui-shell)
4. [Technical Specifications](#4-technical-specifications)
   - 4.1 [API Contracts (Core APIs)](#41-api-contracts-core-apis)
   - 4.2 [Manifest.json Definition](#42-manifestjson-definition)
   - 4.3 [Development Conventions](#43-development-conventions)
   - 4.4 [Deployment & Observability (Kubernetes-ready)](#44-deployment--observability-kubernetes-ready)
5. [Non-Functional Requirements (NFRs)](#5-non-functional-requirements-nfrs)
6. [Acceptance Criteria](#6-acceptance-criteria)

---

## 1. Introduction

### 1.1. Purpose

To define the requirements for **vKernel**, the underlying operating system of the Corporation. vKernel does **not** contain business logic (e.g., Finance, HR); instead, it provides the infrastructure to run Business Apps (Modules) in a unified, secure, and integrated environment.

> _Dinh nghia yeu cau cho vKernel — he dieu hanh nen tang. No khong chua nghiep vu, ma cung cap ha tang de chay cac Ung dung nghiep vu mot cach thong nhat va an toan._

### 1.2. Scope

- **In Scope:** Core Engine, Identity Management, Global Data, Event Bus, UI Shell.
- **Out of Scope:** Specific logic for the 12 Apps (Finance, Sales, HR, etc.) — These are defined in separate App PRDs.

### 1.3. Definitions

| Term              | Definition                                                                   |
| ----------------- | ---------------------------------------------------------------------------- |
| Platform (The OS) | The vKernel code                                                             |
| App (The Module)  | A pluggable package (e.g., vFinance, vHR) containing logic and UI            |
| Tenant            | A single organization instance (Multi-tenancy support)                       |
| Golden Record     | Master data entity (stakeholder, currency) managed by Data Backbone          |
| Event Bus         | Internal Pub/Sub system for cross-app communication with immutable audit log |
| Manifest          | JSON descriptor for a vApp — permissions, events, dependencies               |
| Alignment Tree    | Hierarchical goal structure (Vision > BSC > OKR > Initiative > Task)         |

### 1.4. Problem & Opportunity + User Personas & Key Journeys

#### 1.4.1 Problem & Opportunity

**Problem:** Doanh nghiep Viet Nam (trong tam SME quy mo 30-200 nguoi) dang ket trong bay van hanh:

- **Data silos & Tool sprawl:** Mot cong ty dung trung binh 5-8 tool roi rac (MISA cho ke toan, Zalo OA cho khach hang, Google Sheets quan ly kho, CRM tu che) → Du lieu khong khop, ton nhan su doi soat thu cong.
- **Scaling Pain:** Khi mo rong quy mo, viec tich hop them module moi (VD: them HR vao quy trinh Sales) thuong gay gian doan he thong hoac ton chi phi integration dat do.
- **Phap ly dia phuong (Local Compliance):** Ap luc tu Hoa don dien tu (ND123), Bao mat du lieu (ND13/PDPA) khien cac phan mem quoc te (Odoo, Salesforce) kho dap ung hoac ton kem de customize.
- **Low Executive Visibility:** CEO "mu" so lieu real-time. Phai cho bo phan ke toan chot so (ngay 5-10 thang sau) moi biet lai/lo thuc te → Mat co hoi ra quyet dinh.

**Opportunity:** vKernel dinh vi la "**Composable Enterprise OS**" (He dieu hanh doanh nghiep thao lap) dau tien tai VN:

- **Unified Core:** Mot tai khoan, mot database chuan (Golden Records) cho moi ung dung.
- **True Hot-swapping:** Cai dat/Go bo module nghiep vu nhu cai app dien thoai, zero-downtime.
- **Vietnam-First:** Tich hop san chuan ke toan/thue/bao mat Viet Nam ngay tu Kernel.
- **Cost Efficiency:** Mo hinh "vua van" (pay-as-you-grow), giam 50% TCO so voi trien khai ERP truyen thong.

> Muc tieu: 50 SME (Tier 50+ user) adopt trong 12 thang dau, ARR 5-8 ty VND.

#### 1.4.2 User Personas

| Persona            | Age/Profile       | Need                                                       | Pain                                                        |
| ------------------ | ----------------- | ---------------------------------------------------------- | ----------------------------------------------------------- |
| CEO/Founder        | 35-50, Non-tech   | Dashboard "tho" theo nhip song cong ty (Cashflow, Revenue) | So so lieu bao cao sai lech hoac cham tre                   |
| Admin/ITM          | 25-35, Tech-savvy | He thong on dinh, de debug, phan quyen chat che            | He thong sap khi update hoac user reo ten khi quen pass     |
| CFO/Ke toan truong | 30-45, Can trong  | So lieu chinh xac tuyet doi, tuan thu thue                 | Mat thoi gian doi soat du lieu giua CRM va phan mem ke toan |
| Operational Staff  | 22-30 (Sales/HR)  | Nhap lieu nhanh, tim kiem tien loi, UI muot                | Phai nhap lai thong tin khach hang ma bo phan khac da co    |

#### 1.4.3 Key User Journeys

**Journey 1: Install new App (vSales — L2O-01)**

1. **Context:** vStrategy da duoc cai san (Default). Du lieu ve Cau truc phong ban va mot so Doi tac chien luoc da co san.
2. **Action:** Admin vao App Store > Search vSales > Click [Install].
3. **Dependency Check:** He thong kiem tra thay vStrategy da active (Pass).
4. **Auto-Configuration:** vSales tu dong:
   - Pull danh sach "Sales Department" tu vStrategy de gan quyen.
   - Pull danh sach "Existing Stakeholders" (loai Khach hang) tu vStrategy de nap vao danh sach Account.
5. **Result:** vSales icon xuat hien. Admin khong can cai them vContact hay setup lai phong ban. (Time: < 10s).

**Journey 2: The "God View" (CEO checks health)**

1. CEO mo may buoi sang. Dashboard hien: "Runway: 8 thang" (Du lieu tu vFinance) va "Lead moi: 15" (Du lieu tu vSales).
2. Thay canh bao do: "Hop dong ABC sap het han".
3. Bam Cmd+K, go "ABC". He thong trich xuat toan bo: Hop dong (vLegal), Cong no (vFinance), Lich su cham soc (vSales).
4. Go lenh vao Command Palette: "Nhac Sales Manager gia han hop dong ABC" → He thong tu ban task.

---

## 2. System Architecture Overview

### 2.1. Architecture Diagram

```
+------------------------------------------------------------------------------------------------------------+
|  TIER 1: BUSINESS APPS (PLUGGABLE MODULES)                                                                 |
|  +---------------------+   +---------------------+   +---------------------+   +---------------------+     |
|  | vFinance Backend    |   | vFinance Frontend   |   | vSales Module       |   | vHR Module          |     |
|  +----------+----------+   +----------+----------+   +---------------------+   +---------------------+     |
+-------------|-------------------------|--------------------------------------------------------------------+
              | (1. API Call)           | (Render/Nav)
              v                         v
+------------------------------------------------------------------------------------------------------------+
|  TIER 2: vKERNEL CORE PLATFORM (THE OS)                                                                    |
|  +---------------------------+               +---------------------------+                                 |
|  |   API Gateway / Router    |<--------------|      UI Shell Service     |                                 |
|  |   (Traffic Controller)    |               |      (SyR-PLAT-04)        |                                 |
|  +-------------+-------------+               +---------------------------+                                 |
|                +-------------------------+----------------------+----------------------+                   |
|                | (2. Verify)             | (3. Route Req)       | (3. Route Req)       | (3. Route Req)    |
|                v                         v                      v                      v                   |
|  +-------------+-------------+  +------------------+   +------------------+   +------------------+         |
|  | IAM Service (Security)    |  | Data Service     |   | Event & Workflow |   | App Engine Serv. |         |
|  | (SyR-PLAT-01)             |  | (SyR-PLAT-02)    |   | Svc (SyR-PLAT-03)|   | (SyR-PLAT-00)    |         |
|  +-------------+-------------+  +--------+---------+   +---------+--------+   +---------+--------+         |
|                | (4. Access)             |                       ^ (Support vFlow)      |                  |
+----------------|-------------------------|-----------------------|----------------------|------------------+
                 v                         v                       v                      v
+------------------------------------------------------------------------------------------------------------+
|  TIER 3: CORE STORAGE & INFRASTRUCTURE                                                                     |
|  +-------------+-------------+  +--------+---------+   +---------+--------+   +---------+--------+         |
|  | Auth DB (L3/L4 Security)  |  | Core Entities DB |   | Workflow/Evt Log |   | App Registry     |         |
|  +---------------------------+  +------------------+   +------------------+   +------------------+         |
+------------------------------------------------------------------------------------------------------------+
```

### 2.2. Architecture Explanation

#### A. Purpose

So do nay mo ta kien truc 3 tang (3-tier architecture) cua vKernel, dong vai tro la he dieu hanh nen tang (Platform Core). No cho phep cac ung dung nghiep vu (Business Apps) hoat dong nhu nhung module co the lap ghep (Pluggable), chia se du lieu chung va ke thua cac tinh nang bao mat tap trung.

#### B. Layer Breakdown

**1. Tang Business Apps (Lop Ung dung Nghiep vu)**

- Chua cac ung dung doc lap nhu vFinance, vSales, vHR.
- Cac ung dung nay tuan thu chuan giao tiep cua vKernel va khong tu quan ly nguoi dung hay du lieu goc.

**2. Tang vKernel Core Platform (Lop Nen tang loi)**

Day la "trung tam dieu khien" bao gom cac dich vu he thong quan trong:

- **API Gateway / Router:** Cong tiep nhan duy nhat cho moi yeu cau API tu Backend cac ung dung.
- **UI Shell Service:** Cung cap khung giao dien thong nhat (Shell), quan ly cac menu va thanh dieu huong dong cho Frontend.
- **IAM Service (Identity & Access Management):** Xu ly xac thuc tap trung (SSO) va phan quyen dua tren vai tro (RBAC).
- **Data Service:** Quan ly truy cap vao cac thuc the du lieu goc (Golden Records) de tranh tinh trang phan manh du lieu (Data Silos).
- **Event Bus Service:** He than kinh trung uong giup cac ung dung giao tiep voi nhau (IPC) thong qua cac su kien.
- **App Engine Service:** Quan ly vong doi ung dung (Cai dat, cap nhat, manifest).

**3. Tang Core Storage & Infrastructure (Lop Luu tru & Ha tang)**

- **Auth DB:** Luu tru thong tin dinh danh va quyen han (Security L3/L4).
- **Core Entities DB:** Luu tru cac bang dung chung nhu Users, Companies, Currencies.
- **Event Store:** Luu tru nhat ky su kien de phuc vu tu dong hoa va truy vet (Audit Trail).
- **App Registry:** Danh muc cac ung dung da cai dat va cau hinh he thong.

#### C. Key Flows

1. **Goi API Kernel:** Cac ung dung gui yeu cau thong qua API Gateway.
2. **Xac thuc & Dieu huong (AuthZ & Routing):** Gateway yeu cau IAM Service kiem tra quyen truy cap truoc khi chuyen tiep yeu cau den cac dich vu ben duoi.
3. **Truy cap Du lieu/Su kien:** Dua tren ket qua xac thuc, IAM cap quyen cho Data Service hoac Event Bus thuc hien thao tac tren co so du lieu tuong ung.

---

## 3. System Requirements

We use the **1 Defining + 4 MECE Supporting** framework. Tracing Code: `SyR-PLAT-[GROUP]-[ID]`

### 3.1. Requirements Traceability Matrix

| Req ID      | Requirement Name                        | Source Policy           | Verification Method                           | Notes                      |
| ----------- | --------------------------------------- | ----------------------- | --------------------------------------------- | -------------------------- |
| SyR-PLAT-00 | App Lifecycle                           | [WATER] 3.2 Code First  | System Test (Install/Uninstall)               | Core defining requirement  |
| SyR-PLAT-01 | Unified IAM                             | [AIR] 3. Agent Identity | Security Test (Pen-test)                      | Security & SSO baseline    |
| SyR-PLAT-02 | Data Backbone                           | [EARTH] 6. Database     | Data Integrity Check                          | No silos — critical        |
| SyR-PLAT-03 | Event Bus & Automation                  | [WATER] 3. Process Arch | Integration Test                              | Automation foundation      |
| SyR-PLAT-04 | Adaptive UI Shell (Micro-Frontend Host) | [AIR] 6. Standards      | UAT (User Acceptance)                         | 3-layer horizontal slicing |
| NFR-PLAT-01 | Performance                             | —                       | Benchmark                                     | <10s install, <300ms query |
| NFR-PLAT-02 | Reliability & Availability              | [WATER]                 | Chaos testing                                 | Zero-downtime              |
| NFR-PLAT-03 | Security & Compliance                   | [WATER]                 | Pen-test + compliance check                   | —                          |
| NFR-PLAT-04 | Scalability                             | —                       | Load test                                     |                            |
| NFR-PLAT-05 | Data Isolation                          | [EARTH] 6 + [AIR] 3     | Security Audit + RLS Test + Cross-Tenant Test |                            |

### 3.2. SyR-PLAT-00 | The Dynamic App Engine

**Goal:** Provide a complete ecosystem for installing, running, maintaining, and upgrading both Business Modules and the Core OS.

| Req ID         | Component Name                               | Definition & Key Functions                                                                                                                                              |
| -------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SyR-PLAT-00.00 | App Launcher (Trinh khoi chay Ung dung)      | Central Dashboard & Access Control: Provides a unified workspace. Automatically displays only the Apps a user is authorized to see based on their role.                 |
| SyR-PLAT-00.01 | App Store (Cho Ung dung)                     | Trusted Corporate App Store: A "One-click" hub featuring verified Publishers and mandatory security scans. Automatically manages dependencies to prevent system errors. |
| SyR-PLAT-00.02 | Installation Manager (Trinh Quan ly Cai dat) | Safe Upgrade & Recovery Engine: Ensures risk-free updates. Automatically creates "save points" for instant rollback and performs silent, zero-downtime upgrades.        |

**Wireframes:**

```
App Launcher (Dashboard):
+----------------------------------------------------------------------------------------------------------+
| vRoute OS  |           Search (Cmd+K)                    |  Notif (3) |      [CEO]                       |
+----------------------------------------------------------------------------------------------------------+
|   Good Morning, Administrator                                                                            |
|   YOUR INSTALLED APPS (Business Modules)                                                                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   | vStrategy        |  | vHR              |  | vDesign          |  | vMarketing       |                 |
|   | Plan: Q1 Active  |  | Headcount: 10    |  | Active Specs: 8  |  | Leads: 120 New   |                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   | vFinance         |  | vProcure         |  | vDev (Build)     |  | vSales           |                 |
|   | Status: Healthy  |  | POs: 5 Open      |  | Sprint: 60%      |  | KPI: 92%         |                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   | vAsset           |  | vIT (Infra)      |  | vOps             |  | vSupport         |                 |
|   | Devices: 15      |  | Tickets: 2 Open  |  | Uptime: 99.98%   |  | CSAT: 4.8/5      |                 |
|   +------------------+  +------------------+  +------------------+  +------------------+                 |
|   SYSTEM UTILITIES (Core Admin)                                                                          |
|   +--------------+  +--------------+  +------------+  +--------------+  +------------+  +--------------+ |
|   | App Store    |  | Settings     |  | vData      |  | vFlow        |  | vAudit     |  | vMonitor     | |
|   | (Installer)  |  | (Config/IAM) |  | (MDM Core) |  | (Automation) |  | (Logs/Sec) |  | (Health)     | |
|   +--------------+  +--------------+  +------------+  +--------------+  +------------+  +--------------+ |
+----------------------------------------------------------------------------------------------------------+
```

Wireframe Explanation:

- **Top Bar:** vRoute OS logo, Global Search (Cmd+K), Notification Center, User Profile.
- **Center Canvas:** App Grid showing installed apps with live widget summaries (real-time KPIs).
- **System Utilities:** Core admin apps (App Store, Settings, vData, vFlow, vAudit, vMonitor).

```
App Store + Dependency Resolution Modal:
+-----------------------------------------------------------------------------------------------------------------------+
| vRoute OS | Search Industry/Module...                                        | Notif | [Admin] | T30 JAN 2026 17:58   |
+-----------------------------------------------------------------------------------------------------------------------+
| EXPLORE | INSTALLED | UPDATES | INDUSTRY PACKAGES (GICS/ISIC Standard)                                                |
|                                                                                                                       |
| [ INDUSTRY BUNDLES ]                                                                                                  |
| +-------------------------+  +-------------------------+  +-------------------------+  +-------------------------+    |
| | LOGISTICS (ISIC-H)      |  | MANUFACTURING (ISIC-C)  |  | RETAIL (GICS-45)        |  | HEALTHCARE (ISIC-Q)     |    |
| | Pre-config: vOps, vAsset|  | Pre-config: vProc, vDev |  | Pre-config: vSales, vMkt|  | Pre-config: vHR, vAsset |    |
| | [ INSTALL BUNDLE ]      |  | [ INSTALL BUNDLE ]      |  | [ INSTALL BUNDLE ]      |  | [ INSTALL BUNDLE ]      |    |
| +-------------------------+  +-------------------------+  +-------------------------+  +-------------------------+    |
|                                                                                                                       |
| [ DEPENDENCY RESOLUTION POPUP ]                                                                                       |
| +---------------------------------------------------------------------------------------------------------------+     |
| | INSTALLATION MANAGER (SyR-PLAT-00.01)                                                                    [X] |     |
| |                                                                                                               |     |
| | WARNING: MISSING DEPENDENCY DETECTED                                                                          |     |
| | You are trying to install "vSupport (v2.1)"                                                                   |     |
| | This requires: vSales (Front) — Needs Customer Records, Active Deals & SLA targets.                          |     |
| |                                                                                                               |     |
| | [   Cancel   ]                                               [ INSTALL vSALES & vSUPPORT ]                   |     |
| +---------------------------------------------------------------------------------------------------------------+     |
+-----------------------------------------------------------------------------------------------------------------------+
```

### 3.3. SyR-PLAT-01 | Identity & Access Management (IAM)

**Goal:** A single "Key" (User ID) opens all authorized "Doors" (Apps).

| Req ID         | Component Name                   | Definition & Key Functions                                                                                                                                                     |
| -------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SyR-PLAT-01.00 | Unified Authentication (AuthN)   | Centralized Single Sign-On (SSO): A secure login gateway where users authenticate once to gain seamless access to all authorized Apps without repeated prompts.                |
| SyR-PLAT-01.01 | Role-Based Authorization (AuthZ) | Global Role Governance (WHO Codes): Maintains a central registry of Roles (e.g., CEO, Manager) mapped strictly to Organization Policy, ensuring consistent access rights.      |
| SyR-PLAT-01.02 | Dynamic Permission Injection     | Modular Capability Registration: Apps do not create users; they "inject" specific functional rights (e.g., "Approve Invoice") into the central AuthZ system upon installation. |

**Wireframe: Permission Matrix**

```
+-----------------------------------------------------------------------------------------------------------------------+
| vRoute OS  |  Settings > Identity & Access > Permission Matrix                                    [Admin: ITM-01]     |
+-----------------------------------------------------------------------------------------------------------------------+
|  ROLE & PERMISSION MATRIX (WHO-Based AuthZ)                                                                           |
|  Configure [C]reate, [R]ead, [U]pdate, [D]elete, [L]ist, [I]mport, [E]xport, [A]pprove rights per Role.              |
|                                                                                                                       |
|  [ Search "Invoice"... ]    Filter: [ All Apps ]                         [ Reset ]  [ Cancel ] [ SAVE CHANGES ]       |
|                                                                                                                       |
|  +-------------------------------+------------+------------+------------+------------+------------+------------+       |
|  | PERMISSIONS (Action)          | CEO        | CAO        | FAM        | ITM        | BDM        | HRM        |       |
|  |                               | (Vision)   | (Ops)      | (Finance)  | (Sec/IT)   | (Sales)    | (People)   |       |
|  +===============================+============+============+============+============+============+============+       |
|  | vKERNEL (System Core)         |            |            |            |            |            |            |       |
|  |   [L] List/View Dashboard     |   [x]      |   [x]      |   [x]      |   [x]      |   [x]      |   [x]      |       |
|  |   [U] Update Global Settings  |   [ ]      |   [ ]      |   [ ]      |   [x]      |   [ ]      |   [ ]      |       |
|  |   [A] Install/Remove Apps     |   [A]      |   [ ]      |   [ ]      |   [x]      |   [ ]      |   [ ]      |       |
|  +-------------------------------+------------+------------+------------+------------+------------+------------+       |
|  | vFINANCE (Bookkeeping)        |            |            |            |            |            |            |       |
|  |   [L] List General Ledger     |   [x]      |   [x]      |   [x]      |   [ ]      |   [ ]      |   [ ]      |       |
|  |   [C] Create Purchase Order   |   [ ]      |   [x]      |   [x]      |   [ ]      |   [x]      |   [x]      |       |
|  |   [U] Update Records          |   [ ]      |   [ ]      |   [x]      |   [ ]      |   [ ]      |   [ ]      |       |
|  |   [D] Delete Transactions     |   [ ]      |   [ ]      |   [x]      |   [Lock]   |   [ ]      |   [ ]      |       |
|  |   [I] Import Bank Data        |   [ ]      |   [ ]      |   [x]      |   [ ]      |   [ ]      |   [ ]      |       |
|  |   [E] Export Tax Reports      |   [x]      |   [x]      |   [x]      |   [ ]      |   [ ]      |   [ ]      |       |
|  |   [A] Approve Payment (>5k)   |   [x]      |   [x]      |   [ ]      |   [ ]      |   [ ]      |   [ ]      |       |
|  +-------------------------------+------------+------------+------------+------------+------------+------------+       |
|  | vSALES (GTM Strategy)         |            |            |            |            |            |            |       |
|  |   [C] Create Leads/Deals      |   [ ]      |   [ ]      |   [ ]      |   [ ]      |   [x]      |   [ ]      |       |
|  |   [R] View Customer Data      |   [x]      |   [x]      |   [x]      |   [ ]      |   [x]      |   [ ]      |       |
|  |   [A] Approve Discount        |   [x]      |   [x]      |   [ ]      |   [ ]      |   [x]      |   [ ]      |       |
|  +-------------------------------+------------+------------+------------+------------+------------+------------+       |
|                                                                                                                       |
|  LEGEND: [x] Granted, [ ] Denied, [Lock] System Lock, [A] Accountable                                                |
+-----------------------------------------------------------------------------------------------------------------------+
```

**Wireframe: SSO Login Gateway**

```
+----------------------------------------------------------------------------------------------------------+
|  vRoute OS  |  Secure Identity Gateway (SSO)                                         256-bit SSL         |
+----------------------------------------------------------------------------------------------------------+
|                                                                                                          |
|   WELCOME TO vROUTE ENTERPRISE PLATFORM                                                                  |
|   One Account. Unlimited Access.                                                                         |
|                                                                                                          |
|   +---------------------------------------------+      +---------------------------------------------+   |
|   |  SIGN IN (Existing User)                    |      |  SIGN UP (New User)                         |   |
|   |                                             |      |                                             |   |
|   |  Identifier (Email or Phone Number)         |      |  Organization / Company Name                |   |
|   |  [ admin@abivin.com                   ]     |      |  [ Abivin Vietnam JSC                 ]     |   |
|   |                                             |      |                                             |   |
|   |  Password                                   |      |  Tax ID / VAT Number (Required)             |   |
|   |  [ *******************                ]     |      |  [ 0101234567                         ]     |   |
|   |                                             |      |                                             |   |
|   |  [x] Remember me on this device             |      |  Country / Region                           |   |
|   |                                             |      |  [ Vietnam (+84)                      ]     |   |
|   |  +---------------------------------------+  |      |                                             |   |
|   |  |                SIGN IN                |  |      |  Admin Email (Will be Super User)           |   |
|   |  +---------------------------------------+  |      |  [ contact@abivin.com                 ]     |   |
|   |                                             |      |                                             |   |
|   |  Or verify without password:                |      |  Create Password                            |   |
|   |  [ Send Magic AuthN Link to Email    ]      |      |  [ ********** ] Confirm: [ ********** ]     |   |
|   |                                             |      |                                             |   |
|   |  -----------------------------------------  |      |  +---------------------------------------+  |   |
|   |  [ ? Forgot Password? ]                     |      |  |              SIGN UP                 |  |   |
|   |  [ SSO with Microsoft/Google          ]     |      |  +---------------------------------------+  |   |
|   +---------------------------------------------+      +---------------------------------------------+   |
|                                                                                                          |
|   By logging in, you agree to our Terms of Service & Privacy Policy.                                     |
|   Powered by vKernel Identity Service (OIDC/OAuth2)                                                      |
+----------------------------------------------------------------------------------------------------------+
```

Wireframe Explanation:

- **Split-Pane Layout:** Left (Sign In) for daily access, Right (Register) for Day 0 tenant setup.
- **Flexible Identifier:** Email or Phone Number.
- **Magic AuthN Link:** Passwordless login via email link.
- **Enterprise SSO:** Microsoft/Google OIDC integration.
- **Business Verification:** Tax ID / VAT required for B2B KYC.
- **Localization:** Country/Region auto-configures currency and accounting standards.

### 3.4. SyR-PLAT-02 | Universal Data Backbone

**Goal:** A shared database layer so Apps don't create data silos. "Company A" in Sales is the same "Company A" in Finance.

| Req ID         | Component Name                         | Definition & Key Functions                                                                                                                                           |
| -------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SyR-PLAT-02.00 | Core Entities & Stakeholder Management | The System shall own "Golden Records" for: Users, Stakeholders (managed by vStrategy), Currencies, Countries. Apps must reference via Foreign Keys, never duplicate. |
| SyR-PLAT-02.01 | Dynamic JSONB Fields                   | Allow Apps to extend Core Entities using metadata (JSONB) column without altering schema. Example: vMarketing adds "facebook_url", vFinance adds "tax_code".         |
| SyR-PLAT-02.02 | Universal Search                       | Index text data from all Apps into a central Search Engine (Postgres FTS) for global retrieval.                                                                      |

**Wireframe: Universal Search (Cmd+K)**

```
+----------------------------------------------------------+
|  Search  [Abivin|                               ] [Esc]  |
+----------------------------------------------------------+
|                                                          |
|  PARTNERS (Core Entities)                                |
|  +----------------------------------------------------+  |
|  | Abivin Vietnam                      [View Detail]  |  |  <--- SELECTED
|  |    Tax ID: 0101234567 | Hanoi, VN                  |  |
|  +----------------------------------------------------+  |
|                                                          |
|  vSALES (Leads & Opportunities)                          |
|  | Abivin Deal Q3 - Logistics System                   |  |
|  |    Stage: Negotiation | Value: $50,000              |  |
|                                                          |
|  vFINANCE (Documents)                                    |
|  | INV-2026-001: Software License Fee                  |  |
|  |    Status: Unpaid | Due: 30/01/2026                 |  |
|                                                          |
|  vHR (Personnel)                                         |
|  | Nguyen Van A (Account Manager for Abivin)           |  |
|  |    Dept: Sales Team 1                               |  |
|                                                          |
+----------------------------------------------------------+
|  Up/Down Navigate   Enter Open Record   Cmd+C Copy Link  |
+----------------------------------------------------------+
```

Wireframe Explanation:

- **Overlay Context:** Dimmed background when Cmd+K is pressed.
- **Grouped Results:** Results grouped by source App (Partners, vSales, vFinance, vHR).
- **Visual Hierarchy:** App titles in dim, record names in bold.
- **Keyboard Navigation:** Arrow keys + Enter for power users.

### 3.5. SyR-PLAT-03 | Inter-process Communication (IPC)

**Goal:** Apps must talk to each other to automate workflows. (Sales closes Deal → Finance creates Invoice).

| Req ID         | Component Name      | Definition & Key Functions                                                                                                            |
| -------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| SyR-PLAT-03.01 | Event Registry      | Maintain a registry of standard events (e.g., DOC_SIGNED, RECORD_CREATED). Apps publish events here.                                  |
| SyR-PLAT-03.02 | Subscription Engine | Allow App A to subscribe to events from App B. When vSales publishes ORDER_CONFIRMED, vFinance automatically triggers CREATE_INVOICE. |
| SyR-PLAT-03.03 | Audit Trail Logging | Record every IPC transaction with Timestamp, Source App, Target App, and Payload for debugging and audit (ISO 9001).                  |

**Wireframe: Workflow Automation Builder**

```
+-----------------------------------------------------------------------------------------------+
| vRoute OS  |  System > Automation > Workflow: Auto-Invoice Generation             [Live Mode] |
+-----------------------------------------------------------------------------------------------+
|  TOOLS    |                                                                                   |
|           |   Last Run: Just now (Trace ID: #IPC-8821)                                        |
|           |                                                                                   |
| [Trigger] |        +------------------------+                     +------------------------+  |
|           |        | vSALES (Trigger)       |                     | vFINANCE (Action)      |  |
| [Action]  |        |                        |  [Success]          |                        |  |
|           |        | Event: ORDER_CONFIRMED |====================>| Cmd: CREATE_INV_DRAFT  |  |
| [Logic]   |        | Source: Deal #9021     |      150ms          | Target: Inv #D-2026-01 |  |
|           |        +------------------------+                     +------------------------+  |
| [Timer]   |                     |                                              |              |
|           |                     v                                              v              |
+-----------+            +------------------+                           +------------------+    |
|  HISTORY  |            | OUTPUT PAYLOAD   |                           | INPUT PAYLOAD    |    |
|           |            | {                |                           | {                |    |
| #8821     |            |   "deal_id": 9021|                           |   "ref_id": 9021,|    |
| 10:25 AM  |            |   "amt": 5000,   |                           |   "amount": 5000,|    |
| Success   |            |   "cust": "Abivin"|                          |   "cust": "Abivin"|   |
|           |            | }                |                           | }                |    |
| #8820     |            +------------------+                           +------------------+    |
| 10:00 AM  |                                                                                   |
| Error     |                                                                                   |
+-----------+-----------------------------------------------------------------------------------+
```

Wireframe Explanation:

- **Canvas:** Trigger Node (vSales) → Action Node (vFinance) connected by status/latency line.
- **History Panel:** Audit trail of runs with color-coded status (Success/Error).
- **Data Inspector:** JSON payloads showing data flow between Apps.
- **Toolbar:** Drag-and-drop tools (Trigger, Action, Logic, Timer).

### 3.6. SyR-PLAT-04 | Adaptive UI Shell — Micro-Frontend Host

**Goal:** Users feel they are using ONE software, not 12 different tools. The "Shell" wraps all Apps using a **3-layer horizontal slicing** layout.

| Req ID         | Component Name     | Definition & Key Functions                                                                                                                                                                                                                                         |
| -------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SyR-PLAT-04.01 | Top Navigation Bar | Persistent horizontal bar. **Left:** Logo + brand. **Center:** Menu categories (Master Data · Transactions · Reporting · Configurations) — each category aggregates items from all installed Apps. **Right:** Status indicators, Notifications bell, User profile. |
| SyR-PLAT-04.02 | Control Bar        | Context-sensitive toolbar below Top Nav. **Left:** CREATE button (primary action). **Center:** Entity name + Smart Search (Ctrl+K). **Right:** View Switcher — toggle between 7 view types (List, Kanban, Form, Calendar, Graph, Pivot, Map).                      |
| SyR-PLAT-04.03 | View Display Area  | Dynamic rendering area occupying the main viewport. **Default:** List View with sortable columns. Supports 7 view types, each with 3 defining features. View state persists per-entity per-user. Content loaded from installed vApps via micro-frontend isolation. |

#### Wireframe — 3-Layer Horizontal Slicing

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo]   Master Data ▾  Transactions ▾  Reporting ▾  Configs ▾   🔔  👤 Admin  │  ← Top Navigation Bar
├──────────────────────────────────────────────────────────────────────────────────┤
│ [+ CREATE]    Sales Orders          🔍 Search...          ☰ List │▦ Kanban│📊  │  ← Control Bar
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ☐  Name              Customer         Amount      Status     Date              │
│  ───────────────────────────────────────────────────────────────────────────     │
│  ☐  SO-001             Abivin JSC       $12,400     ● Confirmed  2026-03-15    │
│  ☐  SO-002             TechViet Ltd     $8,750      ○ Draft      2026-03-14    │
│  ☐  SO-003             GreenCo          $23,100     ● Confirmed  2026-03-13    │
│  ☐  SO-004             Mekong Corp      $5,200      ◐ Pending    2026-03-12    │
│                                                                                  │  ← View Display Area
│  ─────────────────────────────────────────────────────────────────────────       │
│  ◄ 1  2  3  ... 12 ►        Showing 1-20 of 234 records                        │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

#### View Types (7)

| #   | View Type | 3 Defining Features                                                                 |
| --- | --------- | ----------------------------------------------------------------------------------- |
| 1   | List View | Sortable columns · Bulk actions (select all) · Inline edit                          |
| 2   | Kanban    | Drag-and-drop cards · Stage columns (e.g., Draft → Confirmed → Done) · Color coding |
| 3   | Form View | Single-record detail · Field validation · Chatter/activity log                      |
| 4   | Calendar  | Day/Week/Month toggle · Drag to reschedule · Color by status                        |
| 5   | Graph     | Bar/Line/Pie chart · Dimension selector (X/Y axis) · Export PNG/CSV                 |
| 6   | Pivot     | Row/Column grouping · Measure aggregation (Sum/Avg/Count) · Drill-down              |
| 7   | Map       | Geolocation pins · Cluster zoom · Route overlay (for logistics)                     |

---

## 4. Technical Specifications

### 4.1. API Contracts (Core APIs)

#### 4.1.1. App Lifecycle API (SyR-PLAT-00)

```
POST /api/v1/apps/install — Install a new Business App

Headers:
  X-Request-ID: string (required, for tracing)
  Authorization: Bearer <admin_token>

Body:
  {
    "app_id": "com.vcorp.vfinance",
    "version": "2.1.0",
    "manifest_url": "https://repo.vcorp.com/vfinance/manifest_v2.1.json"
  }

Responses:
  202 Accepted:
    {
      "job_id": "install_aj38dh",
      "status": "pending",
      "message": "Dependency check in progress",
      "next": "/api/v1/jobs/install_aj38dh"
    }
  400 Bad Request:
    {
      "error": "MISSING_DEPENDENCY",
      "message": "Required app 'com.vcorp.vcontacts:^1.4.0' is not installed.",
      "details": { "missing": ["com.vcorp.vcontacts"], "required_version": "^1.4.0" }
    }
```

#### 4.1.2. Permission Injection API (SyR-PLAT-01)

```
POST /api/v1/iam/permissions/inject — Inject new permissions from an App into AuthZ System

Headers:
  X-App-ID: string (required, e.g., "vfinance")
  X-App-Secret: string (required)

Body:
  {
    "permissions": [
      {
        "code": "finance.invoice.approve",
        "name": "Approve Invoice",
        "description": "Can approve invoices above delegated threshold",
        "category": "finance"
      },
      {
        "code": "finance.report.export",
        "name": "Export Financial Reports",
        "description": "Can export P&L, Balance Sheet reports",
        "category": "finance"
      }
    ]
  }

Responses:
  201 Created:
    {
      "status": "injected",
      "injected_count": 2,
      "warning": "Permissions are inactive until mapped to Roles."
    }
  409 Conflict:
    {
      "error": "PERMISSION_EXISTS",
      "message": "Permission code 'finance.invoice.approve' already registered by 'vpayables'."
    }
```

#### 4.1.3. Data Entity Extension API (SyR-PLAT-02)

```
PATCH /api/v1/data/entities/company/{id}/extend — Extend a Core Entity with custom fields

Headers:
  X-App-ID: string (required)
  X-User-ID: string (required, for audit)

Parameters:
  id: string (required, UUID of the Company)

Body:
  {
    "fields": {
      "facebook_url": {
        "type": "string",
        "value": "https://facebook.com/acme",
        "label": "Facebook Page",
        "visibility": ["vmarketing", "vsales"]
      },
      "tax_code": {
        "type": "string",
        "value": "TAX-789-XYZ",
        "label": "Local Tax Identifier",
        "visibility": ["vfinance", "vcompliance"]
      }
    }
  }

Responses:
  200 OK:
    {
      "entity_id": "co_abc123",
      "extended_by": "vmarketing",
      "version": 3,
      "custom_fields": ["facebook_url"]
    }
```

#### 4.1.4. Event Publishing API (SyR-PLAT-03)

```
POST /api/v1/events/publish — Publish an event to the Event Bus

Headers:
  X-App-ID: string (required)
  X-Correlation-ID: string (required)

Body:
  {
    "event_type": "SALES_ORDER_CONFIRMED",
    "event_version": "1.0",
    "source_app": "vsales",
    "payload": {
      "order_id": "ord_2024_78901",
      "customer_id": "cus_abc123",
      "amount": 15000.00,
      "currency": "USD",
      "confirmed_at": "2024-01-20T10:30:00Z"
    },
    "metadata": {
      "priority": "HIGH",
      "ttl_seconds": 86400
    }
  }

Responses:
  202 Accepted:
    {
      "event_id": "evt_kd83hd93",
      "status": "queued",
      "subscribers_notified": ["vfinance", "vlogistics"]
    }
```

### 4.2. Manifest.json Definition (SyR-PLAT-00)

Required structure for all vApps:

```json
{
  "$schema": "https://schema.vcorp.com/app-manifest/v1",
  "app": {
    "id": "com.vcorp.vfinance",
    "name": "vFinance",
    "version": "2.1.0",
    "min_kernel_version": "1.4.0"
  },
  "dependencies": [
    {
      "app_id": "com.vcorp.vcontacts",
      "version_range": "^1.4.0",
      "reason": "Needs Customer & Vendor entities"
    }
  ],
  "permissions": [
    {
      "code": "finance.invoice.read",
      "default_roles": ["FAM", "CFO"]
    }
  ],
  "ui": {
    "entry_point": "https://cdn.vcorp.com/vfinance/main.js",
    "menu_icon": "finance-icon",
    "menu_label": "Finance",
    "route": "/finance"
  },
  "apis": {
    "provided": [
      {
        "name": "InvoiceService",
        "version": "v1",
        "endpoint": "/finance/api/v1/invoices"
      }
    ],
    "consumed": [
      {
        "name": "CompanyService",
        "source_app": "vcontacts",
        "version": "v1"
      }
    ]
  },
  "events": {
    "published": ["INVOICE_CREATED", "PAYMENT_RECEIVED"],
    "subscribed": ["SALES_ORDER_CONFIRMED"]
  }
}
```

### 4.3. Development Conventions

#### 4.3.1. Naming Conventions

| Element         | Pattern                        | Example                 |
| --------------- | ------------------------------ | ----------------------- |
| App ID          | `com.[company].[appname]`      | `com.vcorp.vhr`         |
| Permission Code | `[domain].[resource].[action]` | `sales.lead.delete`     |
| Event Type      | `[DOMAIN]_[ENTITY]_[ACTION]`   | `HR_EMPLOYEE_ONBOARDED` |
| API Versioning  | `api/v[major]` in URL          | `/api/v1/...`           |

#### 4.3.2. Error Handling

All error responses must follow this format:

```json
{
  "error": "ERROR_CODE_IN_CAPS",
  "message": "Human readable message",
  "details": {},
  "correlation_id": "req_123456"
}
```

#### 4.3.3. Logging & Observability

- Every request must carry `X-Correlation-ID` header.
- Structured JSON logging with required fields:

```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "level": "INFO",
  "service": "vfinance",
  "correlation_id": "req_123456",
  "user_id": "usr_789",
  "event": "API_CALL",
  "duration_ms": 150
}
```

### 4.4. Deployment & Observability (Kubernetes-ready)

#### 4.4.1. Helm Chart Structure (Sample)

```yaml
# values.yaml sample
replicaCount: 3
image:
  repository: registry.vcorp.com/vkernel
  tag: "1.0.0"
service:
  type: ClusterIP
  port: 8080
ingress:
  enabled: true
  host: kernel.vroute.vn
resources:
  limits:
    cpu: 1000m
    memory: 2Gi
postgres:
  enabled: true
redis:
  enabled: true
```

#### 4.4.2. Kubernetes Manifest Snippet

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vkernel-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vkernel
  template:
    metadata:
      labels:
        app: vkernel
    spec:
      containers:
        - name: backend
          image: registry.vcorp.com/vkernel:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              value: "jdbc:postgresql://postgres:5432/vkernel"
          resources:
            limits:
              cpu: "1"
              memory: "2Gi"
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: vkernel-service
spec:
  selector:
    app: vkernel
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
```

Expose Prometheus metrics: `install_duration_seconds`, `cross_query_latency_ms`, `event_pubsub_success_rate`.

---

## 5. Non-Functional Requirements (NFRs)

### NFR-PLAT-01 | Performance

- App installation/hot-swap in under **10 seconds** (95th percentile).
- Cross-App queries shall return in under **300ms** (99th percentile).

### NFR-PLAT-02 | Reliability & Availability

- Zero-downtime during App install/update/remove.
- Platform uptime >= **99.9%** monthly.

### NFR-PLAT-03 | Security & Compliance

- All IPC events must be logged immutably (append-only).
- RBAC enforcement must be validated on every request (no bypass).
- Compliance: Ready for ISO 27001, VN hoa don dien tu Nghi dinh 123.

### NFR-PLAT-04 | Scalability

- Support **1,000 concurrent users** with < 1s average response time.
- Horizontal scaling via Kubernetes.

### NFR-PLAT-05 | Multi-Tenancy & Data Isolation

- **Separate Database per Tenant:** Moi khach hang (Business/Tenant) phai su dung mot database rieng biet hoan toan. Khong thiet ke multi-tenant trong cung mot database. Dam bao isolation vat ly tuyet doi.
- **API-Centric Access Only:** Cac App chi duoc truy cap du lieu/chuc nang cua App khac qua Public APIs duoc khai bao ro rang trong manifest.json (apis.provided). Cam hoan toan truy cap truc tiep database.
- **Re-Auth & Re-Authz on Inter-App Calls:** Moi API call giua cac App phai duoc IAM layer xac thuc va uy quyen lai dua tren X-App-ID va permission cu the.
- **Visibility Control on Data Extensions:** Cac truong mo rong (JSONB) phai duoc scope visibility theo App (vi du: chi vMarketing thay facebook_url).

**Validation Methods:**

- Security audit & automated scanning API gateway / data access patterns.
- Penetration testing: thu privilege escalation va data leakage cross-App/tenant.
- Review manifest declarations (apis.provided/consumed) theo nguyen tac least-privilege.

---

## 6. Acceptance Criteria

Acceptance Criteria dang **Gherkin** (Given-When-Then), viet theo chuan BDD (Behavior-Driven Development).

### SyR-PLAT-00: Dynamic App Engine

```gherkin
Feature: App Manifest Parsing
  Scenario: Parse valid manifest.json when installing an App
    Given a valid manifest.json file exists for "vSales" with name, version 2.1.0,
          dependencies ["vContacts"], and menu structure
    When the system parses the manifest during installation
    Then the App metadata is stored correctly
    And dependencies are registered
    And menu items are queued for injection into the Adaptive UI Shell

  Scenario: Reject invalid manifest.json
    Given a manifest.json missing required field "name"
    When the system attempts to parse it
    Then installation fails with error "Invalid manifest: missing name"
    And no partial installation occurs
    And error is logged in audit trail

Feature: Dependency Resolution
  Scenario: Auto-prompt for missing dependencies
    Given vSales manifest requires "vContacts" which is not installed
    When admin clicks "Install vSales" in App Store
    Then system detects missing dependency
    And displays popup: "vSales requires vContacts. Install both?"
    And offers [Cancel] and [Install Both] buttons

  Scenario: Install both when confirmed
    Given dependency popup is shown for vSales requiring vContacts
    When admin clicks [Install Both]
    Then vContacts installs first (successfully)
    And vSales installs after vContacts completes
    And total time < 15 seconds (performance)
    And success notification appears

Feature: Version Control & Rollback
  Scenario: Successful rollback to previous version
    Given vFinance v2.0 is installed and running
    And vFinance v2.1 is installed but causes error
    When admin selects "Rollback to v2.0" from App details
    Then system reverts to v2.0 manifest and code
    And previous version becomes active in < 5 seconds
    And data integrity is preserved
    And rollback event is logged with timestamp and admin ID

  Scenario: Rollback fails due to incompatible data
    Given rollback to v1.0 would break schema compatibility
    When admin attempts rollback
    Then system blocks action
    And shows warning: "Rollback to v1.0 incompatible with current data schema"
    And suggests migration path or cancel
```

### SyR-PLAT-01: Unified IAM

```gherkin
Feature: Centralized AuthN
  Scenario: Successful SSO login across Apps
    Given user "nguyenvana" with role FAM logs in via OIDC
    When user navigates to vFinance then vSales
    Then no additional login is required
    And session token is propagated correctly
    And access is granted based on global role

  Scenario: Session expiration and re-auth
    Given user is idle for > 30 minutes (configurable)
    When user tries to access vHR
    Then system redirects to login page
    And previous session is invalidated

Feature: Granular AuthZ
  Scenario: New role created and propagated
    Given admin creates role "Sales Lead" in AuthZ System
    When a new vSales App is installed
    Then "Sales Lead" appears in Permission Matrix for vSales
    And default permissions are applied (e.g., read-only for new roles)

Feature: Permission Injection
  Scenario: App injects permissions on install
    Given vFinance is being installed
    When installation completes
    Then permissions like "finance.invoice.approve" are added to AuthZ System
    And existing roles (CEO, FAM) can be granted these permissions via matrix
    And no duplicate permissions are created

  Scenario: Permission removal on uninstall
    Given vFinance is uninstalled
    When uninstall completes
    Then all vFinance-specific permissions are removed from registry
    And roles retain only core permissions
```

### SyR-PLAT-02: Data Backbone

```gherkin
Feature: Core Entities
  Scenario: Reference Golden Record without duplication
    Given Company "Abivin" exists in core entities
    When vSales creates a new Deal for Abivin
    Then it references the same core Company ID
    And no duplicate Company record is created in vSales

Feature: Dynamic JSONB Fields
  Scenario: Extend core entity with JSONB
    Given Company table has metadata JSONB column
    When vMarketing installs and adds field "facebook_url"
    Then new Company records can store facebook_url in metadata
    And existing records remain intact
    And vFinance can add "tax_code" independently without conflict

  Scenario: Query extended field cross-App
    Given a Company with metadata {"facebook_url": "fb.com/abivin"}
    When user searches "facebook_url:fb.com/abivin" in Global Search
    Then result returns the Company record correctly

Feature: Universal Search
  Scenario: Global search returns cross-App results
    Given data exists in vSales, vFinance, vHR for "Abivin"
    When user types "Abivin" in Cmd+K search
    Then results are grouped by App (Partners, Deals, Invoices, Personnel)
    And top result is highlighted
    And search time < 500ms
```

### SyR-PLAT-03: IPC (Event Bus)

```gherkin
Feature: Event Registry
  Scenario: Publish standard event
    Given vSales publishes "ORDER_CONFIRMED"
    When event is emitted
    Then it is registered in Event Registry with payload schema validation
    And event is persisted for audit

Feature: Subscription Engine
  Scenario: Successful event subscription and trigger
    Given vFinance subscribes to "ORDER_CONFIRMED"
    When vSales publishes ORDER_CONFIRMED with payload {deal_id: 9021, amount: 5000}
    Then vFinance receives event within < 1s
    And CREATE_INV_DRAFT command is triggered
    And new Invoice draft is created with ref_id: 9021

Feature: Audit Trail Logging
  Scenario: Log every IPC transaction
    Given an event is published and consumed
    When processing completes
    Then audit log records: timestamp, source App, target App, event type,
         payload hash, status (success/fail)
    And log is immutable and queryable by admin
```

### SyR-PLAT-04: Adaptive UI Shell — Micro-Frontend Host

```gherkin
Feature: Top Navigation Bar
  Scenario: Menu categories aggregate installed Apps
    Given vFinance and vSales are installed
    When user opens the Top Navigation Bar
    Then "Transactions" category shows both vFinance and vSales menu items
    And categories reflect only Apps the user has permission to access

Feature: Control Bar
  Scenario: View Switcher toggles between view types
    Given user is on Sales Orders (List View)
    When user clicks "Kanban" in the View Switcher
    Then the View Display Area renders Kanban cards grouped by status
    And the selected view persists for this entity on next visit

Feature: View Display Area
  Scenario: Default List View with sorting
    Given user navigates to any entity (e.g., Invoices)
    When the View Display Area loads
    Then records are shown in List View by default with sortable columns
    And user can select multiple records for bulk actions
```
