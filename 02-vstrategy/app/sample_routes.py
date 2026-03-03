# =============================================================
# vStrategy — Sample Data Routes (fallback when DB unavailable)
# These routes mirror the real API endpoints but return hardcoded
# sample data from sample_data.py.  They are mounted under the
# same prefix and only reached if the DB-backed route returns 500.
#
# In production (with PostgreSQL), these routes are superseded
# by the real DB-backed routes because they are registered after
# the primary routers.
#
# @GovernanceID vstrategy.2.0-SAMPLE
# =============================================================
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.sample_data import (
    get_sample_plans,
    get_sample_plan,
    get_sample_tree,
    get_sample_scorecard,
    get_sample_sop,
    get_sample_signals,
)

router = APIRouter(prefix="/api/v1/vstrategy/sample", tags=["vstrategy – sample"])


@router.get("/plans")
async def list_plans_sample(status: str | None = None):
    """Return sample plan list (no DB required)."""
    return get_sample_plans(status)


@router.get("/plans/{plan_id}")
async def get_plan_sample(plan_id: str):
    """Return a sample plan by ID (no DB required)."""
    plan = get_sample_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Sample plan not found")
    return plan


@router.get("/plans/{plan_id}/tree")
async def get_tree_sample(plan_id: str):
    """Return sample alignment tree (no DB required)."""
    return get_sample_tree(plan_id)


@router.get("/plans/{plan_id}/scorecard")
async def get_scorecard_sample(plan_id: str):
    """Return sample BSC scorecard (no DB required)."""
    return get_sample_scorecard(plan_id)


@router.get("/plans/{plan_id}/sop/validate")
async def validate_sop_sample(plan_id: str):
    """Return sample S&OP validation (no DB required)."""
    return get_sample_sop(plan_id)


@router.get("/plans/{plan_id}/signals")
async def get_signals_sample(plan_id: str):
    """Return sample pivot signals (no DB required)."""
    return get_sample_signals(plan_id)
