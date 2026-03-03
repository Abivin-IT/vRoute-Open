# vMarketing Org — ORM Model Re-exports (backward-compat shim)
from app.database import Base  # noqa: F401 — conftest imports Base from here
from app.campaign.models._types import FlexibleJSON          # noqa: F401
from app.campaign.models.entity import Campaign               # noqa: F401
from app.tracking.models.entity import TrackingEvent          # noqa: F401
from app.segment.models.entity import AudienceSegment         # noqa: F401
from app.content_asset.models.entity import ContentAsset      # noqa: F401
from app.lead_score.models.entity import LeadScore            # noqa: F401

__all__ = [
    "Base",
    "FlexibleJSON",
    "Campaign",
    "TrackingEvent",
    "AudienceSegment",
    "ContentAsset",
    "LeadScore",
]
