# TODO — vRoute-Open Platform

> Danh sách task cho các prompt tiếp theo. Mỗi Step = 1 prompt session.
> Lịch sử các step đã hoàn thành xem tại [CHANGELOG.md](CHANGELOG.md).

## Step 12: Fifth vApp — vSales Org (SyR-SLS-ORG-00 through SyR-SLS-ORG-04)

> Policy: [L2C] Lead-to-Close cycle | depends on vMarketing Org (lead handover events)

- [ ] PRD: `00-design/docs/vsales-org-prd.md` — 5 SyRs, NFRs, manifest sample, Gherkin scenarios
- [ ] Design sheets: `00-design/sheets/vsales-org/{api-contract,acceptance-criteria,data-model}.md`
- [ ] Scaffold `06-vsales-org/` — Python 3.12 / FastAPI (port 8085, shared PostgreSQL DB)
- [ ] ORM models: `Deal`, `SalesActivity`, `Quote`, `Forecast`, `WinLossRecord`
- [ ] Business logic: Pipeline stage engine, quota tracking, CPQ (Configure-Price-Quote), forecast rollup, win/loss analysis
- [ ] Full REST API + TypeScript frontend + dark dashboard
- [ ] 25+ integration tests (pytest-asyncio + httpx + aiosqlite)
- [ ] Dockerfile 2-stage, docker-compose, Makefile target, CI job, gateway routes
- [ ] vKernel Flyway `V11__register_vsales_org.sql`
- [ ] `06-vsales-org/README.md` — cross-references to vMarketing Org, vKernel
