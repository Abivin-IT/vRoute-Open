# =============================================================
# vStrategy — FastAPI Application Entry Point
# @GovernanceID vstrategy.0.0-BOOT
# =============================================================
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.grpc_client import kernel_client

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    # Ping vKernel gRPC on startup — non-fatal if unavailable
    try:
        result = kernel_client.ping()
        logger.info("Kernel gRPC ping: %s", result)
    except Exception as exc:
        logger.warning("Kernel gRPC ping failed (non-fatal): %s", exc)
    yield
    # Graceful shutdown — close gRPC channel
    try:
        kernel_client.close()
    except Exception as exc:
        logger.warning("Kernel gRPC shutdown failed (non-fatal): %s", exc)


app = FastAPI(
    title="vStrategy — S2P2R Strategy Execution",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — dev mode (gateway handles auth in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(router)

# Static files
static_dir = Path(__file__).parent.parent / "static"

# Explicit UI catch-all: serves index.html for /vstrategy and /vstrategy/
@app.get("/vstrategy", include_in_schema=False)
@app.get("/vstrategy/", include_in_schema=False)
async def vstrategy_ui_root():
    return FileResponse(str(static_dir / "index.html"))

if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
