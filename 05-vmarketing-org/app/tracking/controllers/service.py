# =============================================================
# vMarketing Org — TrackingEvent Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.tracking.models.entity import TrackingEvent

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")

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
