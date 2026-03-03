# vDesign Physical — Combined Router Re-export (backward-compat shim)
from __future__ import annotations

from fastapi import APIRouter

from app.golden_sample.controllers.routes import router as golden_sample_router
from app.material.controllers.routes import router as material_router
from app.prototype.controllers.routes import router as prototype_router
from app.lab_test.controllers.routes import router as lab_test_router
from app.handover_kit.controllers.routes import router as handover_kit_router

router = APIRouter()
router.include_router(golden_sample_router)
router.include_router(material_router)
router.include_router(prototype_router)
router.include_router(lab_test_router)
router.include_router(handover_kit_router)


_health_router = APIRouter(prefix="/api/v1/vdesign-physical", tags=["vdesign-physical"])


@_health_router.get("/health")
async def health():
    return {"app": "vDesign Physical", "version": "1.0.0", "status": "UP"}


router.include_router(_health_router)
