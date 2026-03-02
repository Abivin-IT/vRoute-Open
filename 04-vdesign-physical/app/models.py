# =============================================================
# vDesign Physical — SQLAlchemy ORM Models
# GovernanceID: vdesign-physical.0.0 (GoldenSample),
#   vdesign-physical.0.1 (MaterialInbox),
#   vdesign-physical.0.2 (Prototype),
#   vdesign-physical.0.3 (LabTest),
#   vdesign-physical.0.4 (HandoverKit)
# =============================================================
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, DateTime, ForeignKey, Index, Numeric, String, Text,
    JSON, Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

from app.database import Base


class FlexibleJSON(TypeDecorator):
    """Use JSONB on PostgreSQL, plain JSON on SQLite/other dialects."""
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())


# ---------- Golden Sample (Spec Master — The Vault) ----------
# @GovernanceID vdesign-physical.0.0
class GoldenSample(Base):
    __tablename__ = "vdesign_golden_samples"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    sample_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    material = Column(String(255), nullable=True)
    weight_actual = Column(Numeric(10, 3), nullable=True)
    weight_spec = Column(Numeric(10, 3), nullable=True)
    dimension_x_mm = Column(Numeric(10, 3), nullable=True)
    dimension_y_mm = Column(Numeric(10, 3), nullable=True)
    dimension_z_mm = Column(Numeric(10, 3), nullable=True)
    convergence_pct = Column(Numeric(5, 2), nullable=False, default=0)
    status = Column(String(20), nullable=False, default="SEALED")  # SEALED | ACTIVE | COMPROMISED | EXPIRED
    storage_zone = Column(String(100), nullable=True)
    storage_shelf = Column(String(50), nullable=True)
    custodian = Column(String(255), nullable=True)
    seal_tag_id = Column(String(100), nullable=True)
    linked_spec_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lab_tests = relationship("LabTest", back_populates="golden_sample", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vdesign_gs_status", "status"),
        Index("idx_vdesign_gs_code", "sample_code"),
    )


# ---------- Material Inbox (Idea Inbox — Sample Ingestion) ----------
# @GovernanceID vdesign-physical.0.1
class MaterialInbox(Base):
    __tablename__ = "vdesign_material_inbox"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    item_code = Column(String(50), nullable=False)
    source_type = Column(String(50), nullable=False)   # SUPPLIER | COMPETITOR | RND_HANDMADE | MARKET
    supplier_name = Column(String(255), nullable=True)
    description = Column(String(500), nullable=False)
    material_type = Column(String(100), nullable=True)  # e.g. Carbon Fiber, PC-ABS, Clay
    initial_assessment = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING | TESTED | ARCHIVED | SCRAPPED
    qr_tag_id = Column(String(100), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    received_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vdesign_mat_source", "source_type"),
        Index("idx_vdesign_mat_status", "status"),
    )


# ---------- Prototype (Version Control — Mock-up Lifecycle) ----------
# @GovernanceID vdesign-physical.0.2
class Prototype(Base):
    __tablename__ = "vdesign_prototypes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    proto_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    version_label = Column(String(50), nullable=False)  # V1, V2, V3...
    fabrication_method = Column(String(100), nullable=True)  # 3D_PRINT | CNC | INJECTION | HANDMADE
    rfid_tag_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE | IN_TRANSIT | OBSOLETE | DESTROYED
    location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lab_tests = relationship("LabTest", back_populates="prototype", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vdesign_proto_status", "status"),
        Index("idx_vdesign_proto_code", "proto_code"),
    )


# ---------- Lab Test (Feasibility Checker — Stress/Drop Testing) ----------
# @GovernanceID vdesign-physical.0.3
class LabTest(Base):
    __tablename__ = "vdesign_lab_tests"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    test_code = Column(String(50), nullable=False)
    test_type = Column(String(50), nullable=False)  # STRESS | DROP | THERMAL | CHEMICAL | HARDNESS
    golden_sample_id = Column(Uuid, ForeignKey("vdesign_golden_samples.id", ondelete="SET NULL"), nullable=True)
    prototype_id = Column(Uuid, ForeignKey("vdesign_prototypes.id", ondelete="SET NULL"), nullable=True)
    result = Column(String(20), nullable=False, default="RUNNING")  # RUNNING | PASSED | FAILED | CONDITIONAL
    measured_value = Column(String(255), nullable=True)
    threshold_value = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    tested_by = Column(String(255), nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    golden_sample = relationship("GoldenSample", back_populates="lab_tests")
    prototype = relationship("Prototype", back_populates="lab_tests")

    __table_args__ = (
        Index("idx_vdesign_lab_type", "test_type"),
        Index("idx_vdesign_lab_result", "result"),
    )


# ---------- Handover Kit (Tooling Handover → vBuild) ----------
# @GovernanceID vdesign-physical.0.4
class HandoverKit(Base):
    __tablename__ = "vdesign_handover_kits"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(Uuid, nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    kit_code = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    contents_summary = Column(Text, nullable=False)   # e.g. "1x Mold, 2x Jig, 1x Color Sample"
    destination = Column(String(255), nullable=True)   # Factory name / vBuild target
    status = Column(String(20), nullable=False, default="PACKING")  # PACKING | READY | DISPATCHED | RECEIVED
    dispatched_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    packed_by = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column(FlexibleJSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vdesign_hk_status", "status"),
        Index("idx_vdesign_hk_code", "kit_code"),
    )
