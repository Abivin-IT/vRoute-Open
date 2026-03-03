# =============================================================
# vMarketing Org — FastAPI Application Entry-point
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

static_dir = Path(__file__).parent.parent / "static"

# Shared UI from vKernel (dev-mode fallback; in prod, Gateway serves /ui/*)
_ui_dir = Path(__file__).resolve().parent.parent.parent / "01-vkernel" / "src" / "main" / "resources" / "static" / "ui"
if _ui_dir.is_dir():
    app.mount("/ui", StaticFiles(directory=str(_ui_dir)), name="kernel-ui")

app.include_router(router)


@app.get("/health")
async def health():
    return {"app": "vmarketing-org", "status": "ok"}


@app.get("/", include_in_schema=False)
@app.get("/vmarketing-org", include_in_schema=False)
@app.get("/vmarketing-org/", include_in_schema=False)
async def ui_root() -> FileResponse:
    return FileResponse(str(static_dir / "index.html"))


if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
