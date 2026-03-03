# User Personas

> Source: vKernel PRD Section 1.4.2 + Business App PRDs.

| # | Persona | Role Code | Age/Profile | Primary Apps | Need | Pain Point |
|---|---------|-----------|-------------|--------------|------|------------|
| 1 | CEO / Founder | CEO | 35-50, Non-tech | vKernel, vStrategy, vFinacc | Dashboard "tho" theo nhip song cong ty (Cashflow, Revenue) | So so lieu bao cao sai lech hoac cham tre |
| 2 | Admin / IT Manager | ITM | 25-35, Tech-savvy | vKernel (Settings, App Store) | He thong on dinh, de debug, phan quyen chat che | He thong sap khi update hoac user reo ten khi quen pass |
| 3 | CFO / Ke toan truong | FAM | 30-45, Can trong | vFinacc, vKernel (Audit) | So lieu chinh xac tuyet doi, tuan thu thue | Mat thoi gian doi soat du lieu giua CRM va phan mem ke toan |
| 4 | Operational Staff (Sales/HR) | BDM / HRM | 22-30 | vMarketing Org, vDesign Physical | Nhap lieu nhanh, tim kiem tien loi, UI muot | Phai nhap lai thong tin khach hang ma bo phan khac da co |
| 5 | Product Design Lead | CAO | 30-40, Technical | vDesign Physical, vStrategy | Quan ly mau vat ly, theo doi prototype version | Spec drift khong duoc phat hien som, handover thieu thong tin |
| 6 | Marketing Manager | BDM | 28-40, Data-driven | vMarketing Org, vStrategy | ABM campaign orchestration, lead scoring | Khong biet buying intent cua account, content het han |

## Key User Journeys

| # | Journey Name | Primary Persona | Primary Apps | Steps | Expected Outcome |
|---|-------------|-----------------|--------------|-------|------------------|
| 1 | Install new App (vSales) | Admin/ITM | vKernel | App Store → Search → Install → Dep Check → Auto-Config | vSales icon appears; pulls Sales Dept + Stakeholders from vStrategy; < 10s |
| 2 | The "God View" (CEO checks health) | CEO | vKernel, vFinacc, vStrategy | Open Dashboard → See KPIs → Cmd+K search "ABC" → Issue command | Cross-app data retrieved (vFinacc, vStrategy); auto-create task |
| 3 | Record-to-Report cycle | CFO/FAM | vFinacc | Ingest txn → Auto-reconcile → Post journal → Export tax report | Bank transactions matched to POs; ledger balanced; compliance checked |
| 4 | Strategy alignment check | CEO | vStrategy | View plan → Check alignment tree → Review scorecard → Validate S&OP | Status propagation shows Red → Pivot Signal triggered → CEO notified |
| 5 | Physical design review | Design Lead/CAO | vDesign Physical | Create golden sample → Run lab test → Advance handover kit | Convergence % validated; spec drift detected; tooling dispatched |
| 6 | ABM campaign launch | Marketing/BDM | vMarketing Org | Create campaign → Attach content → Define segment → Launch → Track intent | Multi-channel campaign live; tracking events captured; leads scored |
