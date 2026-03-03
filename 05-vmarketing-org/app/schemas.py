# vMarketing Org — Pydantic Schema Re-exports (backward-compat shim)
from app.campaign.models.schema import CampaignCreate, CampaignUpdate, CampaignOut        # noqa: F401
from app.tracking.models.schema import TrackingEventCreate, TrackingEventOut               # noqa: F401
from app.segment.models.schema import AudienceSegmentCreate, AudienceSegmentOut            # noqa: F401
from app.content_asset.models.schema import ContentAssetCreate, ContentAssetOut             # noqa: F401
from app.lead_score.models.schema import LeadScoreCreate, LeadScoreOut                     # noqa: F401

__all__ = [
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignOut",
    "TrackingEventCreate",
    "TrackingEventOut",
    "AudienceSegmentCreate",
    "AudienceSegmentOut",
    "ContentAssetCreate",
    "ContentAssetOut",
    "LeadScoreCreate",
    "LeadScoreOut",
]
