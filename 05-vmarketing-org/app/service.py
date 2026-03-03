# vMarketing Org — Service Re-exports (backward-compat shim)
from app.campaign.controllers.service import (  # noqa: F401
    TENANT,
    list_campaigns,
    get_campaign,
    create_campaign,
    update_campaign,
    launch_campaign,
    pause_campaign,
    complete_campaign,
)
from app.tracking.controllers.service import (  # noqa: F401
    VALID_ACTIONS,
    list_tracking_events,
    get_tracking_event,
    ingest_event,
    intent_summary,
)
from app.segment.controllers.service import (  # noqa: F401
    list_segments,
    get_segment,
    create_segment,
    archive_segment,
)
from app.content_asset.controllers.service import (  # noqa: F401
    VALID_ASSET_TYPES,
    list_assets,
    get_asset,
    create_asset,
    publish_asset,
    archive_asset,
)
from app.lead_score.controllers.service import (  # noqa: F401
    _compute_grade,
    list_leads,
    get_lead,
    upsert_lead,
    qualify_lead,
    handoff_lead,
    disqualify_lead,
)

__all__ = [
    "TENANT",
    # Campaign
    "list_campaigns", "get_campaign", "create_campaign", "update_campaign",
    "launch_campaign", "pause_campaign", "complete_campaign",
    # Tracking
    "VALID_ACTIONS",
    "list_tracking_events", "get_tracking_event", "ingest_event", "intent_summary",
    # Segment
    "list_segments", "get_segment", "create_segment", "archive_segment",
    # Content Asset
    "VALID_ASSET_TYPES",
    "list_assets", "get_asset", "create_asset", "publish_asset", "archive_asset",
    # Lead Score
    "_compute_grade",
    "list_leads", "get_lead", "upsert_lead", "qualify_lead", "handoff_lead", "disqualify_lead",
]
