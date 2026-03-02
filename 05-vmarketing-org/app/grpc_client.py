# =============================================================
# vMarketing Org — gRPC Client (talks to vKernel)
# GovernanceID: vmarketing-org.0.5
# =============================================================
from __future__ import annotations

import logging
import os

import grpc

log = logging.getLogger("vmarketing-org.grpc")


class KernelGrpcClient:
    """Lightweight wrapper around the vKernel gRPC channel."""

    def __init__(self) -> None:
        host = os.environ.get("KERNEL_GRPC_HOST", "vkernel")
        port = os.environ.get("KERNEL_GRPC_PORT", "9090")
        self._target = os.environ.get("KERNEL_GRPC_URL", f"{host}:{port}")
        self._channel: grpc.aio.Channel | None = None

    async def _ensure_channel(self) -> grpc.aio.Channel:
        if self._channel is None:
            self._channel = grpc.aio.insecure_channel(self._target)
        return self._channel

    async def ping(self) -> dict:
        try:
            ch = await self._ensure_channel()
            return {"target": self._target, "state": str(ch.get_state())}
        except Exception as exc:
            log.warning("gRPC ping failed: %s", exc)
            return {"target": self._target, "state": "UNREACHABLE"}

    async def publish_event(self, event_type: str, payload: dict) -> dict:
        log.info("[grpc] publish %s from vmarketing-org", event_type)
        return {"status": "queued", "event_type": event_type, "source": "vmarketing-org"}

    async def get_installed_apps(self) -> list[str]:
        log.info("[grpc] fetching installed apps from vKernel")
        return ["vstrategy", "vfinacc", "vdesign-physical", "vmarketing-org"]

    async def close(self) -> None:
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
            log.info("gRPC channel closed")
