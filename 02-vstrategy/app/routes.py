# =============================================================
# vStrategy — REST API Routes (FastAPI Router)
# Plans, Alignment Tree, Scorecard, S&OP, Pivot Signals.
#
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    PlanCreate, PlanOut, PlanUpdate,
    NodeCreate, NodeOut, NodeUpdate,
    SignalCheck, SignalOut,
)
from app import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy"])


# ===================== PLANS =====================

@router.get("/plans")
async def list_plans(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    plans = await service.list_plans(db, status)
    return {"count": len(plans), "plans": [PlanOut.model_validate(p) for p in plans]}


@router.post("/plans", status_code=201)
async def create_plan(body: PlanCreate, db: AsyncSession = Depends(get_db)):
    plan = await service.create_plan(db, body)
    return PlanOut.model_validate(plan)


@router.get("/plans/{plan_id}")
async def get_plan(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    plan = await service.get_plan(db, plan_id)
    return PlanOut.model_validate(plan)


@router.put("/plans/{plan_id}")
async def update_plan(plan_id: uuid.UUID, body: PlanUpdate, db: AsyncSession = Depends(get_db)):
    plan = await service.update_plan(db, plan_id, body)
    return PlanOut.model_validate(plan)


# ===================== ALIGNMENT TREE =====================

@router.get("/plans/{plan_id}/tree")
async def get_tree(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    nodes = await service.get_tree(db, plan_id)
    return {"plan_id": str(plan_id), "count": len(nodes), "nodes": [NodeOut.model_validate(n) for n in nodes]}


@router.post("/plans/{plan_id}/nodes", status_code=201)
async def add_node(plan_id: uuid.UUID, body: NodeCreate, db: AsyncSession = Depends(get_db)):
    node = await service.add_node(db, plan_id, body)
    return NodeOut.model_validate(node)


@router.put("/nodes/{node_id}")
async def update_node(node_id: uuid.UUID, body: NodeUpdate, db: AsyncSession = Depends(get_db)):
    node = await service.update_node(db, node_id, body)
    return NodeOut.model_validate(node)


@router.post("/nodes/{node_id}/propagate")
async def propagate_status(node_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    changed = await service.propagate_status(db, node_id)
    return {"propagated_count": len(changed), "changed_nodes": changed}


# ===================== SCORECARD =====================

@router.get("/plans/{plan_id}/scorecard")
async def get_scorecard(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await service.get_scorecard(db, plan_id)


# ===================== S&OP VALIDATION =====================

@router.get("/plans/{plan_id}/sop/validate")
async def validate_sop(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await service.validate_sop(db, plan_id)


# ===================== PIVOT SIGNALS =====================

@router.get("/plans/{plan_id}/signals")
async def get_signals(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    signals = await service.get_signals(db, plan_id)
    return {"count": len(signals), "signals": [SignalOut.model_validate(s) for s in signals]}


@router.post("/plans/{plan_id}/signals/check")
async def check_signal(plan_id: uuid.UUID, body: SignalCheck, db: AsyncSession = Depends(get_db)):
    signal = await service.check_pivot_signal(db, plan_id, body.rule_code, body.actual_value, body.description)
    return SignalOut.model_validate(signal)


# ===================== HEALTH =====================

@router.get("/health")
async def health():
    return {"app": "vStrategy", "version": "1.0.0", "status": "UP"}
