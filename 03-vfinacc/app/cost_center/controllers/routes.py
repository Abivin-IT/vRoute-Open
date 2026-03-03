# =============================================================
# vFinacc — Cost Center REST API Routes
# GovernanceID: vfinacc.2.0
# =============================================================
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.cost_center.controllers import service
from app.cost_center.models.schema import CostAllocationCreate, CostAllocationOut

router = APIRouter(prefix="/api/v1/vfinacc", tags=["vfinacc – cost_center"])


@router.get("/cost-centers")
async def list_cost_centers(category: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    allocations = await service.list_cost_allocations(db, category)
    return {"count": len(allocations), "allocations": [CostAllocationOut.model_validate(a) for a in allocations]}


@router.post("/cost-centers", status_code=201)
async def create_cost_center(body: CostAllocationCreate, db: AsyncSession = Depends(get_db)):
    alloc = await service.create_cost_allocation(db, body)
    return CostAllocationOut.model_validate(alloc)


@router.get("/cost-centers/summary")
async def cost_center_summary(db: AsyncSession = Depends(get_db)):
    return await service.get_cost_center_summary(db)
