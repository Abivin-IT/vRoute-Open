# vMarketing Org — Combined Router Re-export (backward-compat shim)
# NOTE: /health lives on `app` in main.py, NOT on this router.
from __future__ import annotations

from fastapi import APIRouter

from app.campaign.controllers.routes import router as campaign_router
from app.tracking.controllers.routes import router as tracking_router
from app.segment.controllers.routes import router as segment_router
from app.content_asset.controllers.routes import router as content_asset_router
from app.lead_score.controllers.routes import router as lead_score_router

router = APIRouter()
router.include_router(campaign_router)
router.include_router(tracking_router)
router.include_router(segment_router)
router.include_router(content_asset_router)
router.include_router(lead_score_router)
