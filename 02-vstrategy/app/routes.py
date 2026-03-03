# =============================================================
# vStrategy — Combined Router (backward-compat shim)
# Includes all feature-module routers + top-level health.
#
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter

from app.str_01_baseline_objectives.controllers.routes import router as plan_router
from app.str_00_alignment_tree.controllers.routes import router as alignment_router
from app.str_04_performance_review.controllers.scorecard_routes import router as scorecard_router
from app.str_03_sop_allocation.controllers.routes import router as sop_router
from app.str_04_performance_review.controllers.signal_routes import router as pivot_signal_router
from app.sample_routes import router as sample_router

router = APIRouter()
router.include_router(plan_router)
router.include_router(alignment_router)
router.include_router(scorecard_router)
router.include_router(sop_router)
router.include_router(pivot_signal_router)
router.include_router(sample_router)


# ===================== HEALTH =====================

@router.get("/api/v1/vstrategy/health", tags=["vstrategy – health"])
async def health():
    return {"app": "vStrategy", "version": "1.0.0", "status": "UP"}
