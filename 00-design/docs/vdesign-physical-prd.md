# PRODUCT REQUIREMENTS DOCUMENT: vDesign (Physical Layer)

## Meta-Data

| Field       | Value                                             |
| ----------- | ------------------------------------------------- |
| Document ID | 0.0.1-C4-SPEC-CPO-vdesign-phys-prd                |
| Version     | 1.0 (Physical Convergence)                        |
| Status      | DRAFTING                                          |
| Owner       | Head of R&D / Lab Manager                         |
| Tech Stack  | IoT Sensors · RFID/QR Mgmt · Lab Equipment (LIMS) |
| Policy Ref  | [I2S] Idea-to-Spec (Physical Verification Cycle)  |

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

vDesign Physical là phân hệ quản lý các thực thể hữu hình trong quy trình Idea-to-Spec. Trong khi vDesign Digital quản lý dữ liệu, vDesign Physical quản lý **Vật chất** (Mẫu vật liệu, Mẫu thử, Khuôn mẫu). Mục tiêu là đảm bảo mọi thông số trên bản vẽ đều được hiện thực hóa chính xác trên vật thể thật thông qua quy trình kiểm định và đối soát vật lý.

### 1.2. Scope

- **In Scope:** Quản lý kho mẫu chuẩn (Golden Samples), Tiếp nhận vật liệu thô, Quản lý các đời mẫu thử (Prototypes), Thử nghiệm phòng Lab, và Đóng gói công cụ sản xuất (Tooling).
- **Out of Scope:** Thiết kế bản vẽ CAD (thuộc vDesign Digital), Sản xuất hàng loạt (thuộc vBuild).

### 1.3. Definitions

| Term                     | Definition                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- |
| **Golden Sample**        | Mẫu vật lý hoàn hảo nhất đã được phê duyệt, dùng làm thước đo chuẩn để so sánh với sản phẩm sản xuất hàng loạt. |
| **Physical Convergence** | Trạng thái khi kích thước và tính chất của vật thể thật khớp 100% với bản vẽ số (Digital Twin).                 |

### 1.4. Problem & Opportunity + User Personas & Key Journeys

#### 1.4.1. Problem & Opportunity

**Vấn đề (Problem):**

1. **Đứt gãy giữa Ảo và Thực (Digital-Physical Gap):** Bản vẽ CAD (Digital) hoàn hảo, nhưng mẫu vật lý (Physical) khi ra lò bị sai lệch về màu sắc, kích thước hoặc độ bền mà không được ghi nhận lại hệ thống.
2. **Mất kiểm soát phiên bản vật lý:** Các đời mẫu thử (Mock-up V1, V2) nằm lộn xộn trong phòng Lab. Kỹ sư thường xuyên cầm nhầm mẫu cũ (đã hủy) để đi kiểm tra, dẫn đến kết quả sai lệch.
3. **Tranh chấp chất lượng:** Khi nhà máy sản xuất sai, không có "Mẫu chuẩn" (Golden Sample) được niêm phong để làm bằng chứng đối chiếu.

**Cơ hội (Opportunity):**

1. **Physical Convergence (Hội tụ vật lý):** Đảm bảo 100% mẫu vật lý khớp với thông số Digital. Nếu vật lý sai, Digital phải sửa và ngược lại.
2. **Truy xuất nguồn gốc (Traceability):** Biết chính xác từng mẫu thử, khuôn mẫu đang nằm ở đâu (Phòng Lab, Kho hay đang trên xe vận chuyển) nhờ định danh số (RFID/QR).

#### 1.4.2. User Personas (Role-based)

| Persona                        | Vai trò                                                                        | Nỗi đau                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Lab Manager / Material Eng** | Tiếp nhận vật liệu thô, vận hành máy kiểm thử, phê duyệt kết quả đo đạc        | Tốn thời gian tìm kiếm mẫu vật trong kho và nhập liệu thủ công kết quả đo vào Excel |
| **Chief Architect**            | Người duy nhất có quyền phê duyệt và niêm phong "Golden Sample"                | Lo sợ mẫu chuẩn bị đánh tráo, biến dạng hoặc thất lạc                               |
| **R&D Logistics Officer**      | Đóng gói (Handover Kit) và vận chuyển công cụ, khuôn mẫu sang nhà máy (vBuild) | Gửi thiếu đồ gá (Jig) hoặc gửi nhầm phiên bản khuôn cũ cho nhà máy                  |

#### 1.4.3. Key User Journeys

1. **Hành trình Nhập kho mẫu (Material Ingestion):** Nhận mẫu vật liệu thô từ nhà cung cấp → Quét phổ/Đo đạc → Gán mã QR định danh → Lưu vào Idea Inbox.
2. **Hành trình Kiểm định độ bền (Stress Test Loop):** Nhận mẫu thử (Prototype) từ máy in 3D/CNC → Thực hiện bài test phá hủy tại Feasibility Checker → Ghi nhận kết quả (Pass/Fail) → Nếu Fail, trả mẫu về để tái thiết kế.
3. **Hành trình Chuyển giao sản xuất (Tooling Handover):** Tập hợp đủ các công cụ (Khuôn, Đồ gá, Mẫu màu) → Kiểm tra hiệu chuẩn → Đóng gói vào Handover Kit → Kích hoạt lệnh vận chuyển sang vBuild.

---

## 2. System Architecture Overview

### 2.1. Sơ đồ Kiến trúc vDesign Physical

```
+--------------------------------------------------------------------------------------------------------------------------+
|                                  VDESIGN PHYSICAL: MATERIALIZATION ARCHITECTURE                                          |
+--------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                          |
|          +----------------------------------------------------------------------------------------------------+          |
|          | [DF] SPEC MASTER (The Golden Sample Vault)                                                         |          |
|          | > Functions: Physical Spec Archive | Reference Sample Mgmt | Metrology Verification Data          |          |
|          +----------------------------------------------------------------------------------------------------+          |
|                                     ^                         ^                         ^                                |
|                                     |                         |                         |                                |
|          +--------------------------+-------------------------+-------------------------+---------------------+          |
|          |                                                                                                    |          |
|          |    +-------------------+     +-------------------+     +-------------------+     +-------------------+        |
|          |    | [SR1] IDEA INBOX  |     | [SR2] VERSION     |     | [SR3] FEASIBILITY |     | [SR4] HANDOVER    |        |
|          |    | (Sample Ingest)   |     |   CONTROL (Proto) |     |   CHECKER (Lab)   |     |   KIT (Tooling)   |        |
|          |    +-------------------+     +-------------------+     +-------------------+     +-------------------+        |
|          |              ^                         ^                         ^                         ^                   |
|          +--------------|-------------------------|-------------------------|-------------------------|--------------+    |
|                         |                         |                         |                         |                   |
+-------------------------|-------------------------|-------------------------|-------------------------|------------------+
| [INPUTS]                | (Raw Materials)         | (Mock-ups)              | (Stress Test)           | [OUT]            |
| > Physical World        | > Supplier Samples      | > CNC/3D Print Models   | > Destructive Tests     | > Jigs & Molds   |
+--------------------------------------------------------------------------------------------------------------------------+
```

### 2.2. Giải thích Kiến trúc

- **[DF] Spec Master:** Thay vì chứa file PDF, nó là một "Kho" (Vault) chứa các mẫu vật lý chuẩn (Golden Samples).
- **[SR1] Idea Inbox:** Cổng tiếp nhận các mẫu vật liệu thô hoặc sản phẩm mẫu từ thị trường để phân tích.
- **[SR2] Version Control:** Quản lý vòng đời của các mẫu thử vật lý (Prototype V1, V2...) bằng mã định danh (QR/RFID).
- **[SR3] Feasibility Checker:** Hệ thống phòng Lab thực hiện các bài test phá hủy (bẻ, đốt, thả rơi) để kiểm tra giới hạn vật lý.
- **[SR4] Handover Kit:** Đóng gói các công cụ vật lý (đồ gá, khuôn, mẫu màu) để chuyển giao cho nhà máy.

---

## 3. System Requirements

### 3.1. Requirements Traceability Matrix

| Req ID     | Feature Name        | Physical Objective                | Verification Method      |
| ---------- | ------------------- | --------------------------------- | ------------------------ |
| SyR-PHY-00 | Spec Master (DF)    | Lưu trữ mẫu chuẩn (Golden Sample) | Metrology Scan (CMM)     |
| SyR-PHY-01 | Idea Inbox          | Nhập kho mẫu vật liệu thô         | Visual Inspection        |
| SyR-PHY-02 | Version Control     | Quản lý các đời Mock-up           | RFID Tracking            |
| SyR-PHY-03 | Feasibility Checker | Kiểm tra độ bền vật lý            | Stress/Drop Testing      |
| SyR-PHY-04 | Handover Kit        | Bàn giao khuôn/đồ gá              | Physical Inventory Check |

### 3.2. [DF] SyR-PHY-00 | Spec Master: Kho lưu trữ "Single Source of Truth" vật lý

**Goal:** Quản lý và bảo quản các mẫu vật lý chuẩn (Golden Samples) và mẫu tham chiếu (Reference Samples). Đây là bằng chứng vật chất duy nhất để giải quyết tranh chấp về chất lượng.

```
+--------------------------------------------------------------------------------------------------------------------------+
| 📐 vDesign | PHYSICAL > SPEC MASTER > GOLDEN SAMPLE VAULT                                [🔐 SEALED] [🔔 1] [LAB_ADMIN]    |
+--------------------------------------------------------------------------------------------------------------------------+
| [ PRODUCT: VK-WATCH-TITANIUM ]       | [ SAMPLE ID: GS-2026-TIT-01 ]             | [ PHYS. CONVERGENCE: 🟢 98.5% ]       |
+--------------------------------------------------------------------------------------------------------------------------+
| :::::: PHYSICAL ATTRIBUTE LEDGER ::::::       | :::::: STORAGE LOCATION ::::::         | :::::: DIGITAL TWIN SYNC :::::: |
| > Weight (Actual): 152.05g (Spec: 152g)       | Zone: High-Security Vault A            | Linked Spec: SPC-DIG-V2.1       |
| > Dim X (CMM): 44.02mm (Tol +/- 0.05mm)       | Shelf: 04 | Bin: 12                    | Hash Match: #a8f9...z221        |
| > Surface Roughness: Ra 0.8 (Verified)        | Condition: Temp 22°C | Hum 45%         | 3D Scan Overlay: 🟢 < 0.01mm   |
| > Material: Ti-6Al-4V (Spectrometer Cert)     | Custodian: Nguyen Van A                | Last Sync: 10 mins ago          |
|-----------------------------------------------|----------------------------------------|---------------------------------|
| [ PHYSICAL INTEGRITY AUDIT ]                                                                                             |
| > [SEALING] Sample sealed in anti-static bag. Tamper-evident tag ID: #TAG-9921 verified. Status: INTACT.                |
| > [CALIBRATION] Master Gauge Block used for verification. Next calibration due: 2026-06-01.                              |
| > [LIFECYCLE] This sample expires in 180 days (Oxidation risk). Action required: [SCHEDULE RE-VALIDATION].               |
+--------------------------------------------------------------------------------------------------------------------------+
| [ 🔓 BREAK SEAL ]   [ 🏷️ PRINT QR LABEL ]   [ 🔬 VIEW METROLOGY REPORT ]   [ 🧬 COMPARE W/ CAD ]   [ 📦 CHECK OUT ]    |
+--------------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Header & Convergence Metrics:** Sample ID (GS-2026-TIT-01) — mã định danh duy nhất in ra QR dán trực tiếp lên vật thể. Physical Convergence (98.5%) — mức độ trùng khớp giữa kích thước/trọng lượng đo được so với thông số lý thuyết CAD.
2. **Physical Attribute Ledger:** Hiển thị dữ liệu đo đạc thực tế (Actual) kèm phương pháp đo (CMM, Spectrometer) — chứng minh sự thật vật lý.
3. **Storage Location & Condition:** Định vị chính xác (Zone/Shelf/Bin) + cảm biến IoT theo dõi nhiệt độ/độ ẩm tủ Vault.
4. **Digital Twin Sync:** Liên kết ngược bản ghi Digital tại vDesign (Layer 1). 3D Scan Overlay — quét 3D định kỳ chồng lớp lên file CAD gốc.
5. **Physical Integrity Audit:** Quản lý niêm phong (Sealing), theo dõi hạn sử dụng mẫu chuẩn (Lifecycle), phát hiện mở dấu niêm phong trái phép → "Compromised".
6. **Action Footer:** Break Seal (cần phê duyệt), Check Out (mượn mẫu ra khỏi kho có ghi nhận).

### 3.3. [SyR-PHY-01] Idea Inbox: Phễu thu thập mẫu vật lý

**Goal:** Tiếp nhận và số hóa thông tin ban đầu của các mẫu vật liệu thô (vải, nhựa, kim loại) hoặc sản phẩm đối thủ từ thị trường.

```
+--------------------------------------------------------------------------------------------------------------------------+
| 📥 vDesign | PHYSICAL > IDEA INBOX > SAMPLE INGESTION                                    [📸 SCAN] [🔔 3] [MATERIAL_ENG]   |
+--------------------------------------------------------------------------------------------------------------------------+
| [ INTAKE QUEUE ] : 5 Physical Items Pending Analysis | [ LAB CAPACITY ] : 🟢 Available                                     |
+--------------------------------------------------------------------------------------------------------------------------+
| ITEM ID        | SOURCE TYPE           | PHYSICAL DESCRIPTION          | INITIAL ASSESSMENT    | ACTION                  |
|----------------|-----------------------|-------------------------------|-----------------------|-------------------------|
| RAW-MAT-01     | Supplier (Toray)      | Carbon Fiber Sheet (2mm)      | Weave: 3K Twill       | [🔬 LAB TEST REQUEST]   |
| MKT-SMP-02     | Competitor Product    | Smart Band (Broken)           | Housing: PC-ABS       | [🛠️ TEARDOWN]           |
| INT-MOD-03     | R&D Handmade          | Clay Model (Ergonomic)        | Scale: 1:1            | [📷 3D SCAN TO CAD]     |
|----------------|-----------------------|-------------------------------|-----------------------|-------------------------|
| [ vKERNEL SENSOR INPUT ]                                                                                                 |
| > "Spectrometer Reading: RAW-MAT-01 color matches Pantone 446C (Delta E = 1.2)."                                        |
| > "Hardness Test: MKT-SMP-02 screen is Gorilla Glass 3 (Mohs 6.5)."                                                    |
+--------------------------------------------------------------------------------------------------------------------------+
| [ ➕ NEW ITEM ]   [ 🏷️ PRINT TAG ]   [ 📤 SEND TO ARCHIVE ]   [ 🧬 LINK TO DIGITAL IDEA ]   [ 🗑️ SCRAP ITEM ]         |
+--------------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Header & Context:** User Role [MATERIAL_ENG] — dành riêng cho Kỹ sư Vật liệu. [📸 SCAN] — nhập liệu bằng chụp ảnh/quét mã.
2. **Status Bar:** Intake Queue (hàng đợi vật lý, quản lý không gian Lab), Lab Capacity (năng lực tiếp nhận — 🟢 Available / 🔴 Full).
3. **Main Data Table:** Phân loại "rác đầu vào" thành dữ liệu cấu trúc — Supplier Sample (lab test), Competitor Product (teardown), Handmade Model (3D scan to CAD).
4. **vKernel Sensor Input:** Tự động hóa — Spectrometer trả mã Pantone chính xác, Hardness Test trả thang Mohs.
5. **Footer Actions:** Print QR/RFID Tag → gán định danh cho vật thể; Link to Digital Idea → liên kết vật chất ↔ ý tưởng số.

### 3.4. [SyR-PHY-02] Version Control: Quản lý version mẫu thử (Mock-ups)

**Goal:** Quản lý các phiên bản vật lý (Mock-up V1, V2, V3). Đảm bảo không nhầm lẫn mẫu cũ (đã hủy) và mẫu mới (đang duyệt) trong quá trình cầm nắm, thử nghiệm.

```
+--------------------------------------------------------------------------------------------------------------------------+
| 🧬 vDesign | PHYSICAL > VERSION CONTROL > PROTOTYPE TRACKER                                [🔍 TRACK] [🔔 2] [PROJECT_MGR] |
+--------------------------------------------------------------------------------------------------------------------------+
| [ ACTIVE ITERATION: V2.1 (CNC Aluminum) ]   | [ PREVIOUS: V1.0 (3D Print) - SCRAPPED ]                                   |
+--------------------------------------------------------------------------------------------------------------------------+
| VERSION TAG    | MFG METHOD            | PHYSICAL STATUS               | LOCATION              | LINKED DIGITAL SPEC     |
|----------------|-----------------------|-------------------------------|-----------------------|-------------------------|
| PROTO-V2.1-A   | CNC (5-Axis)          | 🟢 Active / Under Review      | Meeting Room 2        | SPEC-MECH-V2.1          |
| PROTO-V2.1-B   | CNC (5-Axis)          | 🟡 In Transit                 | Ship to HQ            | SPEC-MECH-V2.1          |
| PROTO-V1.0-A   | SLA 3D Print          | 🔴 Destroyed (Obsolete)       | Recycling Bin         | SPEC-MECH-V1.0          |
|----------------|-----------------------|-------------------------------|-----------------------|-------------------------|
| [ CONVERGENCE CHECK ]                                                                                                    |
| > "Alert: PROTO-V2.1-A weight (45g) exceeds Digital Spec V2.1 (42g) by 7%. Check CNC wall thickness."                  |
| > "Tracking: RFID Signal for PROTO-V2.1-B detected at Logistics Gate 3."                                                |
+--------------------------------------------------------------------------------------------------------------------------+
| [ ➕ NEW PROTO ]   [ 🚫 MARK OBSOLETE ]   [ 📍 LOCATE ASSET ]   [ 📝 LOG FEEDBACK ]   [ 🧬 SYNC SPECS ]                |
+--------------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Iteration Status Bar:** Phân định Active Iteration (V2.1 CNC) vs Previous (V1.0 SCRAPPED) — cảnh báo "đừng dùng mẫu cũ".
2. **Main Tracking Table:** Mỗi cá thể mẫu thử (Instance) có Version Tag (QR/RFID), Mfg Method, Physical Status, Location, Linked Digital Spec.
3. **Convergence Check:** Tự động so sánh con số thực tế vs CAD (weight discrepancy 7%), RFID tracking qua các cổng từ.
4. **Footer Actions:** Mark Obsolete (dán tem SCRAPPED), Locate Asset (Find My Prototype — kích hoạt RFID), Log Feedback (đồng bộ ghi chú về team Design).

### 3.5. [SyR-PHY-03] Feasibility Checker: Quy trình duyệt tính khả thi (Lab Test)

**Goal:** Thực hiện các bài kiểm tra vật lý (Stress Test, Thermal, Waterproof) để xác nhận thiết kế có khả thi trong điều kiện thực tế.

```
+--------------------------------------------------------------------------------------------------------------------------+
| 🧪 vDesign | PHYSICAL > FEASIBILITY CHECKER > LAB STRESS TEST                              [⚡ RUNNING] [🔔 1] [TEST_ENG]   |
+--------------------------------------------------------------------------------------------------------------------------+
| [ SAMPLE: PROTO-V2.1-A ]   | [ TEST SUITE: DURABILITY STD-810G ]   | [ OVERALL RESULT: 🟡 CONDITIONAL PASS ]               |
+--------------------------------------------------------------------------------------------------------------------------+
| TEST TYPE          | EQUIPMENT             | ACTUAL RESULT                 | LIMIT / CRITERIA      | STATUS                |
|--------------------|-----------------------|-------------------------------|-----------------------|-----------------------|
| Drop Test (1.5m)   | High-Speed Cam        | No Crack, Minor Dent          | No Functional Loss    | 🟢 PASSED             |
| Water Submersion   | Pressure Tank         | Leaking at 2ATM               | 5ATM Required         | 🔴 FAILED             |
| Button Cycle       | Pneumatic Finger      | 100,000 Clicks                | > 50,000 Clicks       | 🟢 PASSED             |
| Salt Spray         | Corrosion Chamber     | No Oxidation (24h)            | No Oxidation (24h)    | 🟢 PASSED             |
|--------------------|-----------------------|-------------------------------|-----------------------|-----------------------|
| [ LAB REPORT INSIGHTS ]                                                                                                  |
| > "Failure Analysis: Water leakage detected at Button Seal. Physical gap measured 0.15mm (Spec requires 0.05mm)."        |
| > "Recommendation: Tighten tolerance on 'O-Ring Groove' in vDesign Digital before cutting next prototype."                |
+--------------------------------------------------------------------------------------------------------------------------+
| [ 🔄 RE-RUN TEST ]   [ 📸 ATTACH PHOTO ]   [ 🛡️ CERTIFY RESULT ]   [ 📤 SEND TO DESIGN ]   [ 📊 VIEW GRAPHS ]         |
+--------------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Test Suite Header:** Linked Sample (PROTO-V2.1-A), Test Standard (STD-810G), Overall Result (CONDITIONAL PASS — some tests failed).
2. **Test Table:** Actual Result vs Limit/Criteria cho từng bài test (Drop, Water, Button Cycle, Salt Spray). Color-coded status.
3. **Lab Report Insights:** Failure Analysis tự động (gap 0.15mm vs spec 0.05mm), Recommendation → feed back to Digital Design.
4. **Footer Actions:** Re-run Test, Attach Photo (bằng chứng), Certify Result, Send to Design (đồng bộ feedback).

### 3.6. [SyR-PHY-04] Handover Kit: Đóng gói tài liệu & Công cụ (Tooling)

**Goal:** Đóng gói các vật thể vật lý cần thiết (Đồ gá, Khuôn mẫu, Mẫu đối chứng màu sắc) để chuyển giao (Shipment) sang nhà máy sản xuất (vBuild).

```
+--------------------------------------------------------------------------------------------------------------------------+
| 📦 vDesign | PHYSICAL > HANDOVER KIT > TOOLING SHIPMENT                                    [🚚 READY] [🔔 0] [LOGISTICS]   |
+--------------------------------------------------------------------------------------------------------------------------+
| [ KIT ID: KIT-2026-TIT-PROD ]    | [ DESTINATION: vBuild Factory 1 ]    | [ CONTENTS: 12 PHYSICAL ITEMS ]                |
+--------------------------------------------------------------------------------------------------------------------------+
| ITEM NAME              | TYPE                  | PHYSICAL VERIFICATION         | PACKING STATUS        | QR CODE ID        |
|------------------------|-----------------------|-------------------------------|-----------------------|-------------------|
| Assembly Jig #01       | Fixture (Steel)       | Calibrated 2026-02-12         | 🟢 Boxed              | TOOL-JIG-01       |
| Color Master (Grey)    | Pantone Plastic Chip  | Visual Match OK               | 🟢 Sealed             | REF-COL-GR        |
| Go/No-Go Gauge         | QA Tool               | Tolerance Check OK            | 🟢 Boxed              | TOOL-GAUGE-05     |
| Golden Sample          | Reference Product     | Spec Master Signed            | 🟢 Sealed             | GS-2026-TIT-01    |
|------------------------|-----------------------|-------------------------------|-----------------------|-------------------|
| [ SHIPMENT MANIFEST CHECK ]                                                                                              |
| > "Weight Check: Total Kit Weight 45kg matches Logistics Manifest."                                                      |
| > "Safety: 'Assembly Jig' crates secured with shock-absorbent foam. Tilt-watch sensors applied."                         |
| > "Digital Link: Triggering Event 'TOOLING_DISPATCHED' to vBuild upon gate exit."                                        |
+--------------------------------------------------------------------------------------------------------------------------+
| [ 🚚 DISPATCH TRUCK ]   [ 🏷️ PRINT MANIFEST ]   [ 📸 PHOTO PROOF ]   [ 📧 NOTIFY FACTORY ]   [ 🛡️ LOCK CONTAINER ]    |
+--------------------------------------------------------------------------------------------------------------------------+
```

**Chức năng chính:**

1. **Header & Logistics Context:** Kit ID (KIT-2026-TIT-PROD) — mã kiện hàng duy nhất. Destination (vBuild Factory 1). Status [🚚 READY].
2. **Main Packing Table:** Physical Verification (Calibrated/Visual Match/Spec Master Signed) cho từng vật phẩm, Packing Status, QR Code ID.
3. **Shipment Manifest Check:** Weight Check (tổng trọng lượng khớp manifest), Safety Sensors (Tilt-watch), Digital Link (Event `TOOLING_DISPATCHED` → vBuild).
4. **Footer Actions:** Dispatch Truck, Photo Proof (bằng chứng ngoại phạm), Lock Container (kẹp chì).

---

## 4. Non-Functional Requirements (NFRs)

### 4.1. NFR-PHY-00 | Security (CIA Triad)

- **Confidentiality:** Dữ liệu 3D Scan (Point Cloud/Mesh) và công thức vật liệu mã hóa AES-256 cả At Rest và In Transit. Zero Trust Architecture cho thiết bị LIMS; xác thực qua vKernel IAM.
- **Integrity:** Chữ ký số cho lệnh "Niêm phong mẫu chuẩn" (Sealing). Sửa đổi dữ liệu đo đạc mà không phê duyệt → gắn cờ Compromised. Audit Trail append-only.
- **Availability:** Hệ thống quản lý kho mẫu chuẩn luôn sẵn sàng 24/7.

### 4.2. NFR-PHY-01 | Reliability & Safety (Mission-Critical)

- **Reliability:** Zero Drift khi đồng bộ dữ liệu từ thiết bị Metrology (CMM) về bản sao số. Tỷ lệ lỗi chuyển đổi 3D Scan → CAD < 0.001%.
- **Safety:** Khi cảm biến IoT phát hiện điều kiện môi trường tủ Vault vượt ngưỡng → cảnh báo Critical trong < 5 giây.

### 4.3. NFR-PHY-02 | Performance (L-T-C & USE)

| Metric     | Target                                                                                 |
| ---------- | -------------------------------------------------------------------------------------- |
| Latency    | 3D vs CAD Overlay phản hồi < 2s. Đồng bộ cảm biến < 5s.                                |
| Throughput | Xử lý cùng lúc dữ liệu từ 50 cảm biến IoT + 5 luồng quét mẫu song song.                |
| Capacity   | Lưu trữ lịch sử 100,000 thực thể vật lý (mẫu thử, khuôn, jig) mà không giảm hiệu năng. |

### 4.4. NFR-PHY-03 | Interaction Capability (E-E-S)

- **Effectiveness:** 100% kỹ sư hoàn thành bài test phòng Lab trên hệ thống mà không cần hỗ trợ kỹ thuật.
- **Efficiency:** Truy xuất dữ liệu Metrology của Golden Sample < 3 clicks.

### 4.5. NFR-PHY-04 | Maintainability & Flexibility (ISO 25010)

- **Modularity:** Tách biệt logic quản lý kho (Vault) và logic kiểm thử (Feasibility) — nâng cấp độc lập.
- **Testability:** Unit test coverage thuật toán Drift Calculation ≥ 85%.

---

## 5. Technical Specifications (Manifest Sample)

```json
{
  "app": {
    "id": "com.vcorp.vdesign.phys",
    "name": "vDesign Physical Layer",
    "version": "1.0.0"
  },
  "dependencies": ["com.vcorp.vkernel:^1.0.0", "com.vcorp.vdesign.digi:^1.0.0"],
  "permissions": [
    {
      "code": "phys.spec.seal",
      "default_roles": ["CHIEF_ARCHITECT", "LAB_ADMIN"]
    },
    {
      "code": "phys.inventory.audit",
      "default_roles": ["LAB_MGR", "LOGISTICS_OFFICER"]
    },
    {
      "code": "phys.lab.execute",
      "default_roles": ["TEST_ENG", "MATERIAL_ENG"]
    }
  ],
  "events": {
    "published": [
      "PHYSICAL_CONVERGENCE_UPDATED",
      "SPEC_DRIFT_DETECTED",
      "TOOLING_DISPATCHED",
      "ENVIRONMENTAL_ALARM_TRIGGERED"
    ],
    "subscribed": [
      "DIGITAL_SPEC_FROZEN",
      "PRODUCTION_ORDER_RELEASED",
      "MAINTENANCE_SCHEDULED"
    ]
  }
}
```

---

## 6. Acceptance Criteria (Gherkin)

| Req ID     | Scenario                  | Gherkin Steps                                                                                                                                        |
| ---------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| SyR-PHY-00 | Xác nhận độ hội tụ vật lý | **Given** mẫu thử CNC vừa được quét CMM. **When** hệ thống so sánh với Digital Twin. **Then** Convergence % hiển thị chính xác trong < 2s.           |
| SyR-PHY-04 | Bàn giao Handover Kit     | **Given** 12 hạng mục đã niêm phong + QR. **When** bấm DISPATCH và xe tải rời kho. **Then** Event `TOOLING_DISPATCHED` gửi sang vBuild ngay lập tức. |
| NFR-PHY-01 | Cảnh báo sai lệch Spec    | **Given** PROTO-V2.1-A đang duyệt. **When** trọng lượng lệch > 5% so với CAD. **Then** tự động phát `SPEC_DRIFT_DETECTED` tới Team Design.           |
| NFR-PHY-00 | Bảo vệ niêm phong số      | **Given** Golden Sample đã SEALED. **When** user không có quyền truy cập Metrology Report. **Then** chặn + ghi nhật ký vi phạm an ninh.              |
