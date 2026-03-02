# PRODUCT REQUIREMENTS DOCUMENT: vMarketing Organization (M2L Module)

## Meta-Data

| Field       | Value                                                         |
| ----------- | ------------------------------------------------------------- |
| Document ID | 0.0.0-C4-SPEC-CPO-vapp-vmark-prd                              |
| Version     | 1.0 (Aligned with M2L Policy v1.0)                            |
| Status      | DRAFTING                                                      |
| Owner       | CPO / Head of Marketing                                       |
| Tech Stack  | React (FE) · Python/Go (BE) · vKernel AI Agent (Lead Scoring) |
| Policy Ref  | [M2L] Marketing-to-Lead Cycle                                 |

---

## Table of Contents

- [Meta-Data](#meta-data)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. System Architecture Overview](#2-system-architecture-overview)
- [3. System Requirements](#3-system-requirements)
- [4. Non-Functional Requirements (NFRs)](#4-non-functional-requirements-nfrs)
- [5. Technical Specifications (Manifest Sample)](#5-technical-specifications-manifest-sample)
- [6. Acceptance Criteria (Gherkin)](#6-acceptance-criteria-gherkin)

---

## 1. Introduction

### 1.1. Purpose

vMarketing Organization thực thi quy trình Marketing-to-Lead (M2L) chuyên sâu cho khối doanh nghiệp và chính phủ. Hệ thống tập trung vào chiến lược Account-Based Marketing (ABM), nhận diện tín hiệu mua sắm của tổ chức và nuôi dưỡng mối quan hệ với "Hội đồng quyết định" (Buying Committee) để tạo ra các cơ hội kinh doanh (Opportunities) giá trị lớn.

### 1.2. Scope

- **In Scope:** 5 thành phần cốt lõi: Campaign Orchestrator, Tracking Pixel, Audience Segment, Content Asset, và Lead Scorer.
- **Out of Scope:** Trực tiếp thực hiện chốt đơn hàng (thuộc vSales), Quản lý dịch vụ sau bán hàng (thuộc vService).

### 1.3. Definitions

| Term                      | Definition                                                                                            |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| **M2L**                   | Marketing-to-Lead — Chu kỳ từ khi bắt đầu các hoạt động marketing đến khi thu được Lead.              |
| **Campaign Orchestrator** | Trung tâm điều phối các hoạt động quảng cáo, email, và nội dung trên nhiều nền tảng.                  |
| **Lead Scoring**          | Quy trình gán giá trị số cho khách hàng dựa trên hành vi và mức độ tương quan với chân dung mục tiêu. |

### 1.4. Problem & Opportunity + User Personas & Key Journeys

#### 1.4.1. Problem & Opportunity

**Vấn đề (Problem):**

1. **Dữ liệu phân mảnh:** Các kênh Marketing (Ads, Email, Content) hoạt động rời rạc, khó đo lường hiệu quả tổng thể.
2. **Chất lượng Lead thấp:** Sales lãng phí thời gian xử lý các Lead không có nhu cầu thực tế do thiếu bộ lọc chuẩn.

**Cơ hội (Opportunity):**

1. **Hợp nhất kênh:** Điều phối đa kênh tập trung giúp tối ưu hóa ngân sách và thông điệp.
2. **Tự động hóa phễu:** Sử dụng AI để chấm điểm và phân loại Lead tự động, tăng tỷ lệ chuyển đổi sang Sales.

#### 1.4.2. User Personas (Role-based)

| Persona                  | Vai trò                                                                                 |
| ------------------------ | --------------------------------------------------------------------------------------- |
| **ABM Manager**          | Người lập kế hoạch tấn công các tài khoản chiến lược (Target Accounts).                 |
| **Partnership Director** | Người quản lý các tài liệu chuyên sâu và Case Study để xây dựng uy tín thương hiệu.     |
| **Account Analyst**      | Người theo dõi "Tín hiệu ý định" (Intent Signals) từ các tập đoàn và tổ chức chính phủ. |

#### 1.4.3. Key User Journeys

1. **Hành trình Tạo Chiến dịch:** Khởi tạo tài nguyên nội dung (Content Asset) → Thiết lập phân khúc mục tiêu (Audience Segment) → Điều phối đa kênh qua Campaign Orchestrator.
2. **Hành trình Phân loại Lead:** Người dùng tương tác (Tracking Pixel) → AI chấm điểm dựa trên hành vi (Lead Scorer) → Chuyển giao Lead đạt chuẩn (Hot Lead) sang vSales.

---

## 2. System Architecture Overview

### 2.1. Sơ đồ Kiến trúc vMarketing trên vKernel

```
+------------------------------------------------------------------------------------------------------------------------------+
|                                     VMARKETING MODULE (MARKETING-TO-LEAD)                                                    |
+------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                              |
|       +---------------------------- [DF] CAMPAIGN ORCHESTRATOR (M2L Logic) -------------------+                              |
|       | (Multi-channel Coordination: Ads, Email, Content, Budget Allocation)                  |                              |
+-------+---------------------------------------------------------------------------------------+------------------------------+
|                                          ^                       ^                                                           |
|       +----------------------+ +----------------------+ +----------------------+ +----------------------+                    |
|       | [SR1] Tracking Pixel | | [SR2] Audience Seg.  | | [SR3] Content Asset  | | [SR4] Lead Scorer   |                    |
|       | (Behavioral Data)    | | (Target Groups)      | | (Media Management)   | | (AI Qualification)  |                    |
|       +----------------------+ +----------------------+ +----------------------+ +----------------------+                    |
|                                          ^                       ^                                                           |
+----------------|-------------------------|-----------------------|-------------------------|---------------------------------+
|                | (Consumer Events)       |                       | (Conversion Data)       |                                 |
|        ( External Channels )      ( vKernel Core Customer Data Backbone )           ( vSales Handover )                      |
+------------------------------------------------------------------------------------------------------------------------------+
```

### 2.2. Giải thích Kiến trúc

- **Mục đích:** Kiến trúc vMarketing là "động cơ tăng trưởng" của vKernel, đảm bảo dòng chảy dữ liệu từ hành vi người dùng (Tracking) đến khi trở thành cơ hội kinh doanh (Lead) diễn ra mượt mà và có định lượng.
- **Tầng Tiếp nhận (Ingestion):** Thu thập dữ liệu hành vi từ Tracking Pixel trên các nền tảng số.
- **Tầng Điều phối (Orchestration):** Campaign Orchestrator đóng vai trò bộ não, phân bổ nội dung và ngân sách dựa trên phân khúc khách hàng từ Audience Segment.
- **Tầng Xử lý & Phê duyệt (Execution):** Lead Scorer sử dụng AI Agent để lọc và chấm điểm Lead dựa trên dữ liệu MECE.
- **Luồng chính:** Dữ liệu hành vi → [SR1] ghi nhận → [SR2] phân loại → [SR3] đẩy nội dung phù hợp qua [DF] → [SR4] chấm điểm → bàn giao vSales.

---

## 3. System Requirements

### 3.1. Requirements Traceability Matrix

| Req ID         | Feature Name          | Source Policy         | Verification Method                        | Notes                                 |
| -------------- | --------------------- | --------------------- | ------------------------------------------ | ------------------------------------- |
| SyR-MKT-ORG-00 | Campaign Orchestrator | [M2L] 1. Coordination | System Test: triển khai đa kênh đồng thời  | Trung tâm điều phối Ads/Email/Content |
| SyR-MKT-ORG-01 | Tracking Pixel        | [M2L] 2. Tracking     | UAT: ghi nhận event người dùng thực tế     | Thu thập dữ liệu hành vi              |
| SyR-MKT-ORG-02 | Audience Segment      | [M2L] 3. Segment      | Logic Test: xác thực bộ lọc phân nhóm      | Phân nhóm khách hàng mục tiêu         |
| SyR-MKT-ORG-03 | Content Asset         | [M2L] 4. Asset        | System Test: quản lý tài nguyên media      | Quản lý tài nguyên media/bài viết     |
| SyR-MKT-ORG-04 | Lead Scorer           | [M2L] 5. Scoring      | Benchmark: đo độ chính xác AI Lead Grading | Chấm điểm Lead → Sales                |

### 3.2. [DF] SyR-MKT-ORG-00 | Campaign Orchestrator: Trung tâm điều phối đa kênh

**Goal:** Trung tâm chỉ huy chiến lược ABM, điều phối các điểm chạm đa kênh (LinkedIn, Webinar, Direct Email, Sự kiện) để xây dựng và tối ưu hóa Pipeline Value.

```
+-------------------------------------------------------------------------------------------------------------------+
| 🏢 vMarketing | ORG > CAMPAIGNS > ABM ORCHESTRATOR                                          [⚡ LIVE] [CORP_ADMIN] |
+-------------------------------------------------------------------------------------------------------------------+
| [ PIPELINE VALUE ] : $2,500,000 / $5,0M (🟢 50%) | [ TARGET ACCOUNTS ] : 500 | [ AVG ACQ COST ] : $1,200/Acc      |
+-------------------------------------------------------------------------------------------------------------------+
| [ ACCOUNT ENGAGEMENT & PIPELINE VELOCITY ]                                                [ ENGINE: 🧠 vKERNEL ]  |
| CAMPAIGN NAME        | TARGET SEGMENT       | STAGE         | ENGAGED ACCOUNTS | MQLs  | INTENT HEATMAP           |
|----------------------|----------------------|---------------|------------------|-------|--------------------------|
| Bank_Digital_2026    | Tier-1 Banking       | Consideration | 45 / 50 (90%)    | 12    | 🔥🔥🔥 High (Decision)   |
| Gov_Smart_City_Proj  | Ministry / G-Office  | Awareness     | 120 / 200 (60%)  | 5     | 🟦⬜⬜ Low (Education)    |
| Tech_SaaS_Expansion  | IT Services > $10M   | Closing       | 15 / 20 (75%)    | 8     | 🔥🔥🔥 High (Bidding)    |
| Manufacturing_Smart  | SME Factory (North)  | Nurturing     | 85 / 150 (56%)   | 20    | 🟧🟧⬜ Mid (Research)     |
+-------------------------------------------------------------------------------------------------------------------+
| [ vKERNEL AI ABM OPTIMIZER ]                                                                                      |
| > "Opportunity: 4 C-level từ 'Vietcombank' vừa tải báo cáo ROI. Đề xuất chuyển sang chế độ chốt."               |
| > "Alert: Chiến dịch 'Gov_Smart_City' có tỷ lệ phản hồi email thấp (2%). Đề xuất thay đổi sang Case Study."     |
| > "Forecast: Pipeline dự kiến đạt $4.2M vào cuối Q3. Cần thêm 20% Lead từ Tech Segment."                        |
+-------------------------------------------------------------------------------------------------------------------+
| [ 🔄 SYNC LINKEDIN ]  [ 🔍 ACCOUNT DRILL-DOWN ]  [ 📝 ADJUST CONTENT ]  [ 📊 VIEW ROI ]  [ ⚙️ CONFIG RULES ]     |
+-------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Account-Based Orchestration:** Báo cáo dựa trên Engaged Accounts (tổ chức tương tác) thay vì Clicks/Impressions. Chiến dịch thành công khi "phủ sóng" nhiều người trong Buying Committee.
2. **Pipeline Value Tracking:** Tổng giá trị hợp đồng tiềm năng Marketing mang lại cho Sales. Tự động ước tính dựa trên quy mô Account.
3. **Journey Stage Management:** Awareness → Consideration → Nurturing → Closing. Nội dung khác nhau theo giai đoạn.
4. **vKernel AI ABM Optimizer:** Nhận diện tín hiệu mua hàng tập thể, dự báo Pipeline, đề xuất chiến thuật.
5. **High-Value Actions:** Sync LinkedIn Sales Navigator, Account Drill-down chi tiết.

### 3.3. [SyR-MKT-ORG-01] Tracking Pixel: Thu thập dữ liệu hành vi tổ chức

**Goal:** Nhận diện tổ chức ẩn danh (Anonymous Accounts) thông qua địa chỉ IP, theo dõi hành vi "Buying Committee" và thu thập Intent Signals.

```
+-------------------------------------------------------------------------------------------------------------------+
| 🔍 vMarketing | DATA > PIXEL > ACCOUNT INTENT SENSING                                      [📡 ACTIVE] [ANALYST] |
+-------------------------------------------------------------------------------------------------------------------+
| [ IDENTIFIED ORGS ] : 450 | [ LIVE VISITS ] : 15 Orgs | [ TOP INTENT ] : Fintech | [ STATUS ] : 🛡️ B2B COMPLIANT  |
+-------------------------------------------------------------------------------------------------------------------+
| [ ACCOUNT ENGAGEMENT STREAM ]                                                             [ SYNC: 🟢 REAL-TIME ]  |
| VIETCOMBANK (HQ) --> [3 USERS] --> [VIEWED: CYBERSECURITY] --(5m)--> [DOWNLOADED: TECH-SPEC] --(NOW)--> [HOT 🔥]  |
+-------------------------------------------------------------------------------------------------------------------+
| EVENT ID       | ORGANIZATION / FIRM     | ACTION TYPE        | PAGE / RESOURCE       | DWELL TIME | INTENT SCORE |
|----------------|-------------------------|--------------------|-----------------------|------------|--------------|
| EV-MKT-ORG-01  | Vietcombank (HQ)        | Download_PDF       | Whitepaper-Sec-2026   | 15m 30s    | 92 🔥 (Hot)  |
| EV-MKT-ORG-02  | FPT Software            | Pricing_Compare    | Cloud-Enterprise-Plan | 08m 45s    | 75 🟢 (Warm) |
| EV-MKT-ORG-03  | VinGroup (Corp)         | Video_Watch (80%)  | Case-Study-Logistics  | 05m 12s    | 60 🟢 (Warm) |
| EV-MKT-ORG-04  | Ministry of Finance     | Article_Read       | Gov-Cloud-Regulation  | 02m 00s    | 35 🟡 (Cold) |
| EV-MKT-ORG-05  | Samsung Vina            | Exit_Intent        | Contact-Us-Form       | 00m 15s    | 40 🟡 (Cold) |
+-------------------------------------------------------------------------------------------------------------------+
| [ vKERNEL AI BEHAVIORAL AUDIT ]                                                                                   |
| > "Detection: 3 IP khác nhau thuộc dải 'Vietcombank' cùng truy cập Tech-Spec. Hot Signal!"                       |
| > "Intent Map: 'FPT Software' đang nghiên cứu sâu bảng giá. Dấu hiệu so sánh đối thủ."                         |
| > "Privacy: Dữ liệu ẩn danh hóa cá nhân, chỉ hiển thị thông tin cấp Tổ chức (Organization-Level)."              |
+-------------------------------------------------------------------------------------------------------------------+
| [ 🧪 TEST PIXEL ]  [ 🔍 REVERSE IP LOG ]  [ 📊 VIEW INTENT MAP ]  [ ⚙️ CONFIG WEBHOOKS ]  [ 📜 EXPORT B2B DATA ] |
+-------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **IP-to-Company Mapping:** Reverse IP nhận diện tổ chức đang truy cập (Dark Funnel) ngay cả khi chưa để lại thông tin.
2. **Collective Behavior Tracking:** 3 người khác nhau từ cùng 1 công ty xem 1 trang = CỰC NÓNG. Tính điểm Collective Intent.
3. **High-Value Action Detection:** Download Tech-Spec (thẩm định), Pricing Compare (cân đối ngân sách), Dwell Time > 5m (đọc trình sếp).
4. **vKernel AI Behavioral Audit:** Nhận diện Buying Committee, cảnh báo đối thủ đang "dò giá".
5. **Data Backbone Integration:** Đầu vào sống cho Lead Scorer; khi chạm ngưỡng → thông báo vSales.

### 3.4. [SyR-MKT-ORG-02] Audience Segment: Phân nhóm Tổ chức mục tiêu

**Goal:** Tự động phân loại tổ chức vào phân khúc chiến lược dựa trên Firmographics và tín hiệu thị trường, phục vụ ABM và cá nhân hóa giải pháp theo ngành dọc.

```
+-------------------------------------------------------------------------------------------------------------------+
| 👥 vMarketing | DATA > AUDIENCE > FIRMOGRAPHIC SEGMENTS                                     [➕ CREATE] [STRATEGY] |
+-------------------------------------------------------------------------------------------------------------------+
| [ TOTAL ACCOUNTS ] : 5,200 | [ TARGET LISTS ] : 15 | [ REACHABLE ORGS ] : 4,800 | [ MODE ] : 🤖 DYNAMIC SYNC    |
+-------------------------------------------------------------------------------------------------------------------+
| [ SEGMENTATION ENGINE & COVERAGE ]                                                        [ ENGINE: 🧠 vKERNEL ]  |
| ACTIVE RULES: 24 | COVERAGE: [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 96% ]                     |
+-------------------------------------------------------------------------------------------------------------------+
| SEGMENT NAME         | CRITERIA (Firmographics + Tech)               | ACCOUNTS| ENGAGEMENT | SYNC TARGET         |
|----------------------|-----------------------------------------------|---------|------------|---------------------|
| Tier-1_Banking       | Revenue > $1B + Tech: Legacy Oracle/SAP       | 45      | 🟢 18.5%   | LinkedIn + vSales   |
| SME_Manufacturing    | Staff 200-500 + Region: Northern Vietnam      | 1,200   | 🟡 5.2%    | Direct Email        |
| Gov_Digital_Gov      | Rank: Ministry/Provincial + Project: SmartCity| 32      | 🟢 12.0%   | Bidding Team        |
| Tech_Unicorns_SEA    | Valuation > $1B + Cloud-Native + Growth > 30% | 20      | 🔥 28.5%   | Founder Network     |
| Logistics_Legacy     | Industry: Transport + No Digital Presence      | 850     | ⚪ 2.1%    | Cold Outreach       |
+-------------------------------------------------------------------------------------------------------------------+
| [ vKERNEL AI SEGMENT INSIGHTS ]                                                                                   |
| > "Lookalike Discovery: 150 DN mới có đặc điểm tương đồng tệp 'Tier-1_Banking'."                                |
| > "Trend Alert: 'SME_Manufacturing' đang tăng cường tìm giải pháp 'ERP'. Ưu tiên nội dung."                     |
| > "Data Gap: 15% tài khoản 'Logistics' thiếu thông tin C-level. Đề xuất Data Enrichment."                        |
+-------------------------------------------------------------------------------------------------------------------+
| [ 📊 SEGMENT REPORT ]  [ 🔄 REFRESH ACCOUNTS ]  [ 🔍 OVERLAP ANALYSIS ]  [ 📡 PUSH TO ADS ]  [ ⚙️ DEFINE RULES ] |
+-------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Firmographic & Technographic Segmentation:** Lọc theo Revenue, Headcount, Industry, Location + công nghệ đang dùng (Oracle/SAP → giải pháp nâng cấp).
2. **Tiering Strategy:** Tier-1 (High Touch 1-1), Tier-2/3 (Scale qua Email/Ads). Tự động gán nhãn Tier.
3. **Dynamic Account Sync:** Khi công ty thay đổi trạng thái (gọi vốn → Unicorn), AI tự chuyển nhóm. Danh sách mục tiêu real-time.
4. **vKernel AI Lookalike & Discovery:** Phân tích khách hàng thành công → quét market database → tìm "sinh đôi" chưa biết.
5. **Buying Committee Identification:** Nhóm chức danh trong cùng 1 tổ chức (CEO Decision Maker, IT Influencer, End-user).

### 3.5. [SyR-MKT-ORG-03] Content Asset: Quản lý tài nguyên chuyên sâu (Knowledge Hub)

**Goal:** Quản trị và tối ưu hóa các tài nguyên nội dung giá trị cao (Expertise-driven), đảm bảo tính chính xác thông số kỹ thuật và pháp lý để nuôi dưỡng trust trong hành trình mua hàng dài hạn.

```
+-------------------------------------------------------------------------------------------------------------------+
| 📄 vMarketing | CONTENT > ASSETS > B2B KNOWLEDGE HUB                                        [📤 UPLOAD] [MARKETER]|
+-------------------------------------------------------------------------------------------------------------------+
| [ TOTAL ASSETS ] : 250 | [ STORAGE ] : 45% | [ TOP ASSET ] : Cloud_Banking_ROI_2026 | [ AVG READ TIME ] : 12m 45s |
+-------------------------------------------------------------------------------------------------------------------+
| [ CONTENT PERFORMANCE & ABM ENGAGEMENT ]                                                  [ MODE: 🛡️ COMPLIANCE ] |
| ASSET NAME           | TYPE           | TARGET STAGE  | READS (Unique) | CONV. RATE | KEY ACCOUNTS ENGAGED        |
|----------------------|----------------|---------------|----------------|------------|-----------------------------|
| 2026-Banking-Report  | Whitepaper     | Awareness     | 1,200          | 15.2%      | Vietcombank, Techcom, BIDV  |
| ROI-Calculator-v2    | Interactive    | Consideration | 350            | 42.0%      | FPT, Viettel, CMC           |
| Case-GovCloud-Hanoi  | Case Study     | Closing       | 85             | 65.5%      | Ministry of Finance, MoT    |
| Tech-Spec-API-v4     | Documentation  | Consideration | 520            | 28.1%      | Samsung, LG, Foxconn        |
| Bidding-Compliance   | Legal Doc      | Closing       | 40             | 80.0%      | Gov-Office, Dept of Plan    |
+-------------------------------------------------------------------------------------------------------------------+
| [ vKERNEL AI CONTENT AUDIT & INSIGHTS ]                                                                           |
| > "Alert: Whitepaper '2026-Banking' đang có tỷ lệ đọc 90% tại C-Level. Đề xuất tạo thêm bản tóm tắt cho CEO."  |
| > "Compliance: Case-GovCloud-Hanoi đã hết hạn ISO. Yêu cầu cập nhật tài liệu trước khi gửi."                    |
| > "Content Gap: Thiếu Case Study cho ngành 'Logistics' tại SEA. Đề xuất phỏng vấn khách hàng X."                 |
+-------------------------------------------------------------------------------------------------------------------+
| [ 🔄 SYNC FROM vDESIGN ]  [ 🔍 TRACE TO SPEC ]  [ 🛡️ APPROVAL HUB ]  [ 📊 VIEW ANALYTICS ]  [ ⚙️ CONFIG GATING ] |
+-------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **High-Value Asset Categorization:** Whitepaper (Thought Leadership), ROI Calculator (Business Case), Case Study (bằng chứng triển khai). Gắn thẻ Target Stage.
2. **Gated Content & Lead Capture:** Tài liệu chuyên sâu "khóa" — phải để lại Business Email, Chức vụ, Quy mô dự án → nguồn MQL chất lượng nhất.
3. **Content-to-Capability Convergence:** Đối soát tài liệu ↔ System Capabilities + SLA thực tế. Triệt tiêu "hứa hươu hứa vượn".
4. **vKernel AI Content Audit:** Đo lường Read Time thực tế, phát hiện hot spot (trang nào được đọc lâu nhất), Compliance Check (ISO hết hạn → cảnh báo).
5. **ABM Engagement Mapping:** Hiển thị KEY ACCOUNTS ENGAGED — xác nhận trend ngành.

### 3.6. [SyR-MKT-ORG-04] Lead Scorer: Chấm điểm & Phân loại Tổ chức (Account Scoring)

**Goal:** Sử dụng vKernel AI để định lượng Account Readiness dựa trên Firmographics + Collective Intent, tự động phân loại và chuyển giao MQL cho Sales dự án.

```
+-------------------------------------------------------------------------------------------------------------------+
| 🎯 vMarketing | PROCESS > LEAD SCORER > ACCOUNT QUALIFICATION                               [🛡️ SECURE] [CORP_ADMIN]|
+-------------------------------------------------------------------------------------------------------------------+
| [ TARGET ACCOUNTS ] : 1,200 | [ HOT ACCOUNTS ] : 45 (MQL) | [ AVG INTENT ] : 62/100 | [ SYNC ] : 🟢 vSALES ORG  |
+-------------------------------------------------------------------------------------------------------------------+
| [ ACCOUNT QUALIFICATION PIPELINE ]                                                        [ MODE: 🧠 AI-POWERED ] |
| DISCOVERY (450) --> ENGAGED (280) --> INTENT (120) --> MQL (45) --> [ HANDOVER TO KEY ACCOUNT MANAGERS ]            |
+-------------------------------------------------------------------------------------------------------------------+
| ACCOUNT NAME         | INDUSTRY      | SIGNALS (Buying Committee Actions)    | SCORE | NEXT BEST ACTION           |
|----------------------|---------------|---------------------------------------|-------|----------------------------|
| Samsung Vina         | Manufacturing | CEO (ROI Calc) + CTO (Tech Spec)      | 95 🔥 | [🚀 Pass to Bidding Team]  |
| Vietcombank (HQ)     | Banking       | 5x Users (Viewed Cloud Security)      | 88 🟢 | [📞 Schedule Consult]      |
| FPT Software         | IT Services   | HR (Viewed Career) + IT (Viewed API)  | 45 🟡 | [🤖 Email Nurture]         |
| Grab SEA             | Tech/Trans    | Pricing View 3x (from HQ IP)          | 78 🟢 | [📩 Send Proposal Draft]   |
| Ministry of Finance  | Government    | Anonymous (Viewed GovCloud Case Study) | 30 ⚪ | [📖 Push Whitepaper]       |
+-------------------------------------------------------------------------------------------------------------------+
| [ SCORING WEIGHTS ]                                                                  [ MECE VALIDITY: 🟢 100% ]   |
| > [FIRMOGRAPHICS: 40%] : Revenue, Industry, Employee Count.                                                       |
| > [INTENT/BEHAVIOR: 60%] : Collective Downloads, Pricing Views, Role Diversity.                                    |
+-------------------------------------------------------------------------------------------------------------------+
| [ vKERNEL AI SCORING INSIGHTS ]                                                                                   |
| > "Urgency: 'Samsung Vina' đạt 95đ do CEO thực hiện tính ROI. Tỷ lệ thắng thầu dự kiến 80%."                    |
| > "Alert: 'FPT Software' có điểm hành vi cao từ nhân viên nhưng thiếu quản lý. Cần thêm nội dung ABM."           |
| > "Logic: Tự động trừ -20đ cho Account truy cập 'Tuyển dụng' để tránh nhiễu dữ liệu Sales."                      |
+-------------------------------------------------------------------------------------------------------------------+
| [ 🔄 RE-SCORE ALL ]  [ ⚡ AUTO-HANDOVER ]  [ 📊 VIEW SCORE REPORT ]  [ 🔍 TRACE TO PIXEL ]  [ ⚙️ CONFIG WEIGHTS ] |
+-------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Account Scoring vs. Individual Scoring:** Cộng dồn điểm từ mọi nhân sự cùng tổ chức.
   - Công thức: $Score(Account) = \omega_f \cdot S(Firmographics) + \omega_i \cdot \sum_j S(Intent_j)$
   - Multiplier: Nhiều vai trò (CEO + IT Manager) đồng thời → nhân hệ số.
2. **Buying Committee Identification:** AI phân tích trang truy cập → dự đoán vai trò (ROI → Decision Maker, API → Influencer, Features → End-user). "Hot" khi đủ thành phần.
3. **BANT & Intent Mapping:** Need (download pain-point docs), Authority (IP cao cấp/LinkedIn), Budget & Timeline (ROI calc + pricing views).
4. **Auto-Handover Pipeline:** DISCOVERY → ENGAGED → INTENT → MQL → vSales ORG API.
5. **vKernel AI Insights:** Urgency alerts, noise reduction (-20đ cho Tuyển dụng visits), win probability forecast.

---

## 4. Non-Functional Requirements (NFRs)

### 4.1. NFR-MKT-00 | Security

- Ép buộc RBAC + Re-Auth trên mọi API call để truy xuất Target Accounts chiến lược hoặc thay đổi ngân sách > $10,000.
- Dữ liệu Intent Signals và Buying Committee mã hóa AES-256 At Rest + In Transit qua Event Bus.
- Data Anonymization cho báo cáo phân tích xu hướng — tuân thủ GDPR và chính sách B2G.

### 4.2. NFR-MKT-01 | Reliability & Safety (Mission-Critical)

- Data Integrity: Zero Drift giữa dữ liệu Pixel thô và Lead Score. Mọi thay đổi quy tắc chấm điểm → nhật ký append-only.
- Uptime ≥ 99.9%/tháng, không gián đoạn trong đợt chiến dịch trọng điểm / kỳ đấu thầu.
- **Anti-Manipulation Guard:** Phát hiện và khóa nguồn Bot/Spam trong ≤ 30 giây.

### 4.3. NFR-MKT-02 | Performance

- Truy vấn đối soát Lead (vSales ↔ vMarketing) < 300ms (p99).
- Re-scoring tài khoản khi có sự kiện real-time < 1 giây.
- Hot-swap module AI Agent < 10 giây.

### 4.4. NFR-MKT-03 | Interaction Capability

- Các App khác chỉ truy cập Intent + Segment data qua Public APIs khai báo trong `manifest.json`; cấm truy cập DB trực tiếp.
- Trường mở rộng Data Backbone (`intent_score`, `account_tier`) chỉ visible cho app có thẩm quyền (vSales, vStrategy).
- 100% Convergence: Mọi Handover Lead phải thông qua vKernel Event Bus Service.

### 4.5. NFR-MKT-04 | Maintainability, Flexibility & Compatibility

- Sẵn sàng tuân thủ ISO 27001 và chính sách bảo mật dữ liệu cấp bộ ngành (B2G).
- Horizontal scaling qua Kubernetes — tiếp nhận hàng triệu sự kiện Pixel toàn cầu.
- **Pluggable Architecture:** Tích hợp kênh Marketing mới (WhatsApp Business, Webinar platform) trong < 3 ngày làm việc qua hệ thống Connector chuẩn hóa.

---

## 5. Technical Specifications (Manifest Sample)

```json
{
  "app": {
    "id": "com.vcorp.vmarketing.org",
    "name": "vMarketing ABM Engine",
    "version": "1.0.0",
    "policy_ref": "M2L-ORG-V1"
  },
  "dependencies": ["com.vcorp.vkernel:^1.0.0", "com.vcorp.vsales.org:^1.0.0"],
  "permissions": [
    { "code": "mkt.abm.orchestrate", "default_roles": ["ABM_MANAGER"] },
    { "code": "mkt.pixel.configure", "default_roles": ["ACCOUNT_ANALYST"] },
    { "code": "mkt.lead.handover", "default_roles": ["CORP_ADMIN"] }
  ],
  "events": {
    "published": [
      "ACCOUNT_INTENT_HOT_SIGNAL",
      "ABM_CAMPAIGN_GOAL_REACHED",
      "MQL_READY_FOR_HANDOVER",
      "ACCOUNT_SEGMENT_UPDATED"
    ],
    "subscribed": [
      "SALES_OPPORTUNITY_CLOSED",
      "CUSTOMER_DATA_ENRICHED",
      "MARKETING_BUDGET_ALLOCATED"
    ]
  }
}
```

---

## 6. Acceptance Criteria (Gherkin)

### 6.1. Scenario 1: Tự động nhận diện "Buying Committee" tập thể

> **Given** Module Tracking Pixel đang ghi nhận tương tác từ dải IP của "Vietcombank".
> **When** AI phát hiện đồng thời 01 CEO xem ROI và 01 CTO tải Tech-Spec trong 10 phút.
> **Then** Hệ thống phải nhân hệ số Multiplier và gán nhãn HOT 🔥 cho tài khoản.
> **And** Tín hiệu `ACCOUNT_INTENT_HOT_SIGNAL` phải được bắn sang vSales ngay lập tức.

### 6.2. Scenario 2: Chặn triển khai nội dung chưa đạt chuẩn Compliance

> **Given** ABM Manager đang thiết lập chiến dịch "Gov_Smart_City".
> **When** Tài nguyên Case-GovCloud-Hanoi được đính kèm nhưng đã hết hạn ISO.
> **Then** AI Content Audit phải khóa nút "START CAMPAIGN" và hiển thị cảnh báo.
> **And** Yêu cầu cập nhật phải được gửi tới Partnership Director.

### 6.3. Scenario 3: Chuyển giao Lead tự động (Auto-Handover)

> **Given** Tài khoản "Samsung Vina" đạt Lead Score 95/100.
> **When** Hệ thống xác thực tính toàn vẹn dữ liệu (Business Email, Chức vụ, Quy mô) đạt 100%.
> **Then** Trạng thái chuyển từ INTENT → MQL và thực hiện Auto-Handover sang vSales ORG API.
> **And** Nhật ký bàn giao ghi nhận vào Data Backbone phục vụ báo cáo ROI.
