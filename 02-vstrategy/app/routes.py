# =============================================================
# vStrategy — Combined Router (backward-compat shim)
# Includes all feature-module routers + top-level health.
#
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter

from app.plan.controllers.routes import router as plan_router
from app.alignment.controllers.routes import router as alignment_router
from app.scorecard.controllers.routes import router as scorecard_router
from app.sop.controllers.routes import router as sop_router
from app.pivot_signal.controllers.routes import router as pivot_signal_router

router = APIRouter()
router.include_router(plan_router)
router.include_router(alignment_router)
router.include_router(scorecard_router)
router.include_router(sop_router)
router.include_router(pivot_signal_router)


# ===================== HEALTH =====================

@router.get("/api/v1/vstrategy/health", tags=["vstrategy – health"])
async def health():
    return {"app": "vStrategy", "version": "1.0.0", "status": "UP"}
