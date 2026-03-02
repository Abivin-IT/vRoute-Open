# =============================================================
# vMarketing Org — FastAPI Application Entry-point
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.grpc_client import KernelGrpcClient
from app.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
log = logging.getLogger("vmarketing-org")

grpc_client = KernelGrpcClient()


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa: ARG001 – required by FastAPI
    cfg = settings
    log.info("vMarketing-Org starting on :%s …", cfg.port)
    ping = await grpc_client.ping()
    log.info("gRPC → vKernel: %s", ping)
    yield
    await grpc_client.close()
    log.info("vMarketing-Org stopped.")


app = FastAPI(
    title="vMarketing-Org  ·  M2L ABM Engine",
    version="0.5.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
async def health():
    return {"app": "vmarketing-org", "status": "ok"}


@app.get("/vmarketing-org", response_class=HTMLResponse)
async def ui_root(request: Request):  # noqa: ARG001
    with open("static/index.html") as fh:
        return HTMLResponse(fh.read())
