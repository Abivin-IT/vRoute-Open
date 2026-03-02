# =============================================================
# vMarketing Org — Business-Logic Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Campaign, TrackingEvent, AudienceSegment, ContentAsset, LeadScore

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")


# ===== Campaign ====================================================

async def list_campaigns(db: AsyncSession, status: Optional[str] = None):
    stmt = select(Campaign).where(Campaign.tenant_id == TENANT)
    if status:
        stmt = stmt.where(Campaign.status == status.upper())
    stmt = stmt.order_by(Campaign.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    return await db.get(Campaign, campaign_id)


async def create_campaign(db: AsyncSession, data: dict):
    row = Campaign(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Campaign created: %s", row.campaign_code)
    return row


async def update_campaign(db: AsyncSession, campaign_id: uuid.UUID, data: dict):
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    for k, v in data.items():
        if v is not None:
            setattr(row, k, v)
    await db.commit()
    await db.refresh(row)
    return row


async def launch_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition DRAFT → ACTIVE."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status != "DRAFT":
        raise ValueError(f"Cannot launch campaign in status {row.status}")
    row.status = "ACTIVE"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign launched: %s", row.campaign_code)
    return row


async def pause_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition ACTIVE → PAUSED."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status != "ACTIVE":
        raise ValueError(f"Cannot pause campaign in status {row.status}")
    row.status = "PAUSED"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign paused: %s", row.campaign_code)
    return row


async def complete_campaign(db: AsyncSession, campaign_id: uuid.UUID):
    """Transition ACTIVE|PAUSED → COMPLETED."""
    row = await db.get(Campaign, campaign_id)
    if not row:
        return None
    if row.status not in ("ACTIVE", "PAUSED"):
        raise ValueError(f"Cannot complete campaign in status {row.status}")
    row.status = "COMPLETED"
    await db.commit()
    await db.refresh(row)
    log.info("Campaign completed: %s", row.campaign_code)
    return row


# ===== Tracking Event ==============================================

VALID_ACTIONS = {"PAGE_VIEW", "DOWNLOAD_PDF", "PRICING_COMPARE", "VIDEO_WATCH", "EXIT_INTENT"}


async def list_tracking_events(db: AsyncSession, organization: Optional[str] = None):
    stmt = select(TrackingEvent).where(TrackingEvent.tenant_id == TENANT)
    if organization:
        stmt = stmt.where(TrackingEvent.organization == organization)
    stmt = stmt.order_by(TrackingEvent.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_tracking_event(db: AsyncSession, event_id: uuid.UUID):
    return await db.get(TrackingEvent, event_id)


async def ingest_event(db: AsyncSession, data: dict):
    action = data.get("action_type", "").upper()
    if action not in VALID_ACTIONS:
        raise ValueError(f"Invalid action_type: {action}. Must be one of {VALID_ACTIONS}")
    data["action_type"] = action
    row = TrackingEvent(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Tracking event ingested: %s (%s)", row.event_code, action)
    return row


async def intent_summary(db: AsyncSession, organization: str):
    """Aggregate intent signals for an organization."""
    stmt = (
        select(
            func.count(TrackingEvent.id).label("total_events"),
            func.avg(TrackingEvent.intent_score).label("avg_intent"),
            func.sum(TrackingEvent.dwell_seconds).label("total_dwell"),
        )
        .where(TrackingEvent.tenant_id == TENANT)
        .where(TrackingEvent.organization == organization)
    )
    result = (await db.execute(stmt)).one()
    return {
        "organization": organization,
        "total_events": result.total_events or 0,
        "avg_intent_score": round(float(result.avg_intent or 0), 2),
        "total_dwell_seconds": result.total_dwell or 0,
    }


# ===== Audience Segment ============================================

async def list_segments(db: AsyncSession, tier: Optional[str] = None):
    stmt = select(AudienceSegment).where(AudienceSegment.tenant_id == TENANT)
    if tier:
        stmt = stmt.where(AudienceSegment.tier == tier.upper())
    stmt = stmt.order_by(AudienceSegment.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_segment(db: AsyncSession, segment_id: uuid.UUID):
    return await db.get(AudienceSegment, segment_id)


async def create_segment(db: AsyncSession, data: dict):
    row = AudienceSegment(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Segment created: %s", row.segment_code)
    return row


async def archive_segment(db: AsyncSession, segment_id: uuid.UUID):
    row = await db.get(AudienceSegment, segment_id)
    if not row:
        return None
    row.status = "ARCHIVED"
    await db.commit()
    await db.refresh(row)
    log.info("Segment archived: %s", row.segment_code)
    return row


# ===== Content Asset ================================================

VALID_ASSET_TYPES = {"WHITEPAPER", "CASE_STUDY", "VIDEO", "INFOGRAPHIC", "BLOG"}


async def list_assets(db: AsyncSession, asset_type: Optional[str] = None):
    stmt = select(ContentAsset).where(ContentAsset.tenant_id == TENANT)
    if asset_type:
        stmt = stmt.where(ContentAsset.asset_type == asset_type.upper())
    stmt = stmt.order_by(ContentAsset.created_at.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_asset(db: AsyncSession, asset_id: uuid.UUID):
    return await db.get(ContentAsset, asset_id)


async def create_asset(db: AsyncSession, data: dict):
    at = data.get("asset_type", "").upper()
    if at not in VALID_ASSET_TYPES:
        raise ValueError(f"Invalid asset_type: {at}. Must be one of {VALID_ASSET_TYPES}")
    data["asset_type"] = at
    row = ContentAsset(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Asset created: %s", row.asset_code)
    return row


async def publish_asset(db: AsyncSession, asset_id: uuid.UUID):
    row = await db.get(ContentAsset, asset_id)
    if not row:
        return None
    if row.status != "DRAFT":
        raise ValueError(f"Cannot publish asset in status {row.status}")
    row.status = "PUBLISHED"
    await db.commit()
    await db.refresh(row)
    log.info("Asset published: %s", row.asset_code)
    return row


async def archive_asset(db: AsyncSession, asset_id: uuid.UUID):
    row = await db.get(ContentAsset, asset_id)
    if not row:
        return None
    row.status = "ARCHIVED"
    await db.commit()
    await db.refresh(row)
    log.info("Asset archived: %s", row.asset_code)
    return row


# ===== Lead Score ===================================================

def _compute_grade(score: int) -> str:
    if score >= 70:
        return "HOT"
    if score >= 40:
        return "WARM"
    return "COLD"


async def list_leads(db: AsyncSession, grade: Optional[str] = None):
    stmt = select(LeadScore).where(LeadScore.tenant_id == TENANT)
    if grade:
        stmt = stmt.where(LeadScore.grade == grade.upper())
    stmt = stmt.order_by(LeadScore.score.desc())
    return (await db.execute(stmt)).scalars().all()


async def get_lead(db: AsyncSession, lead_id: uuid.UUID):
    return await db.get(LeadScore, lead_id)


async def upsert_lead(db: AsyncSession, data: dict):
    score = data.get("score", 0)
    data["grade"] = _compute_grade(score)
    row = LeadScore(tenant_id=TENANT, **data)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    log.info("Lead scored: %s → %s (score=%d)", row.organization, row.grade, row.score)
    return row


async def qualify_lead(db: AsyncSession, lead_id: uuid.UUID):
    """Move lead from NEW → QUALIFIED."""
    row = await db.get(LeadScore, lead_id)
    if not row:
        return None
    if row.status != "NEW":
        raise ValueError(f"Cannot qualify lead in status {row.status}")
    row.status = "QUALIFIED"
    await db.commit()
    await db.refresh(row)
    log.info("Lead qualified: %s", row.organization)
    return row


async def handoff_lead(db: AsyncSession, lead_id: uuid.UUID, handed_off_to: str):
    """Hand off a QUALIFIED lead to sales."""
    row = await db.get(LeadScore, lead_id)
    if not row:
        return None
    if row.status != "QUALIFIED":
        raise ValueError(f"Cannot hand off lead in status {row.status}")
    row.status = "HANDED_OFF"
    row.handed_off_to = handed_off_to
    await db.commit()
    await db.refresh(row)
    log.info("Lead handed off: %s → %s", row.organization, handed_off_to)
    return row


async def disqualify_lead(db: AsyncSession, lead_id: uuid.UUID):
    row = await db.get(LeadScore, lead_id)
    if not row:
        return None
    row.status = "DISQUALIFIED"
    await db.commit()
    await db.refresh(row)
    log.info("Lead disqualified: %s", row.organization)
    return row
