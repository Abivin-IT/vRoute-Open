# =============================================================
# vFinacc — Shared FlexibleJSON Type
# GovernanceID: vfinacc.0.0
# =============================================================
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator


class FlexibleJSON(TypeDecorator):
    """Use JSONB on PostgreSQL, plain JSON on SQLite/other dialects."""
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())
