# =============================================================
# vFinacc — Application Configuration (Pydantic Settings)
# GovernanceID: vfinacc.0.0-CONFIG
# =============================================================
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralised config — reads from env vars or .env."""

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "vkernel"
    db_user: str = "vkernel"
    db_pass: str = "vkernel"

    # Kernel IPC
    kernel_url: str = "http://localhost:8080"

    # Server
    port: int = 8082

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
