# sheets/

Cross-app structured data tables extracted from all 5 PRD documents.
These sheets serve as the single source of truth for tabular reference data — every table covers **all apps** with an `App` column for filtering.

| Sheet File | Scope | Content |
|------------|-------|---------|
| [api-contract-summary.md](api-contract-summary.md) | All 5 apps | 103 REST API endpoints: method, path, auth, Req ID |
| [acceptance-criteria.md](acceptance-criteria.md) | All 5 apps | 36 Gherkin scenarios in flat table format |
| [requirements-traceability-matrix.md](requirements-traceability-matrix.md) | All 5 apps | 45 requirements (40 functional + 5 NFR) with policy refs |
| [data-model.md](data-model.md) | All 5 apps | 31 database entities: table names, column counts, key columns |
| [permission-matrix.md](permission-matrix.md) | All 5 apps | 27 permissions × 6 roles in unified flat table |
| [nfr-targets.md](nfr-targets.md) | All 5 apps | 17 NFR metrics with Scope column (Platform / per-app) |
| [user-personas.md](user-personas.md) | All 5 apps | 6 personas + 6 user journeys with Primary Apps column |
| [naming-conventions.md](naming-conventions.md) | Platform-wide | App ID, Permission, Event, API naming patterns |

**Apps covered:** vKernel (Platform), vStrategy (S2P2R), vFinacc (R2R), vDesign Physical (I2S), vMarketing Org (M2L ABM)
