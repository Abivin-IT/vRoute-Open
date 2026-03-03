# =============================================================
# alignment/controllers/routes.py — Alignment Tree REST endpoints
# @GovernanceID vstrategy.2.0
# =============================================================
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.alignment.models.schema import NodeCreate, NodeOut, NodeUpdate
from app.alignment.controllers import service

router = APIRouter(prefix="/api/v1/vstrategy", tags=["vstrategy – alignment"])


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
