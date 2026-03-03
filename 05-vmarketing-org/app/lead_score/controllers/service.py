# =============================================================
# vMarketing Org — LeadScore Service Layer
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.lead_score.models.entity import LeadScore

log = logging.getLogger("vmarketing-org.service")

TENANT = uuid.UUID("00000000-0000-0000-0000-000000000001")


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
