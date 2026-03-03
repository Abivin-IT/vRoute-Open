# =============================================================
# vFinacc — Combined REST API Router (backward-compat shim)
# Includes all 5 feature routers + health endpoint.
#
# @GovernanceID vfinacc.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter

from app.ledger.controllers.routes import router as ledger_router
from app.transaction.controllers.routes import router as transaction_router
from app.reconciliation.controllers.routes import router as reconciliation_router
from app.cost_center.controllers.routes import router as cost_center_router
from app.compliance.controllers.routes import router as compliance_router

router = APIRouter()
router.include_router(ledger_router)
router.include_router(transaction_router)
router.include_router(reconciliation_router)
router.include_router(cost_center_router)
router.include_router(compliance_router)


# ===================== HEALTH =====================

@router.get("/api/v1/vfinacc/health", tags=["vfinacc"])
async def health():
    return {"app": "vFinacc", "version": "1.0.0", "status": "UP"}

