"""vdesign_physical_init — Schema + Seed Data

Revision ID: 0001
Revises: None
Create Date: 2026-03-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# Alembic migration metadata — used by Alembic runtime
revision: str = "0001"  # noqa: F841
down_revision: Union[str, None] = None  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    # ---- Golden Samples (Spec Master Vault) ----
    op.create_table(
        "vdesign_golden_samples",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("sample_code", sa.String(50), nullable=False),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("material", sa.String(255), nullable=True),
        sa.Column("weight_actual", sa.Numeric(10, 3), nullable=True),
        sa.Column("weight_spec", sa.Numeric(10, 3), nullable=True),
        sa.Column("dimension_x_mm", sa.Numeric(10, 3), nullable=True),
        sa.Column("dimension_y_mm", sa.Numeric(10, 3), nullable=True),
        sa.Column("dimension_z_mm", sa.Numeric(10, 3), nullable=True),
        sa.Column("convergence_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="SEALED"),
        sa.Column("storage_zone", sa.String(100), nullable=True),
        sa.Column("storage_shelf", sa.String(50), nullable=True),
        sa.Column("custodian", sa.String(255), nullable=True),
        sa.Column("seal_tag_id", sa.String(100), nullable=True),
        sa.Column("linked_spec_id", sa.String(100), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vdesign_gs_status", "vdesign_golden_samples", ["status"])
    op.create_index("idx_vdesign_gs_code", "vdesign_golden_samples", ["sample_code"])

    # ---- Material Inbox (Idea Inbox) ----
    op.create_table(
        "vdesign_material_inbox",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("item_code", sa.String(50), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("supplier_name", sa.String(255), nullable=True),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("material_type", sa.String(100), nullable=True),
        sa.Column("initial_assessment", sa.String(500), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("qr_tag_id", sa.String(100), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("received_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vdesign_mat_source", "vdesign_material_inbox", ["source_type"])
    op.create_index("idx_vdesign_mat_status", "vdesign_material_inbox", ["status"])

    # ---- Prototypes (Version Control) ----
    op.create_table(
        "vdesign_prototypes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("proto_code", sa.String(50), nullable=False),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("version_label", sa.String(50), nullable=False),
        sa.Column("fabrication_method", sa.String(100), nullable=True),
        sa.Column("rfid_tag_id", sa.String(100), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vdesign_proto_status", "vdesign_prototypes", ["status"])
    op.create_index("idx_vdesign_proto_code", "vdesign_prototypes", ["proto_code"])

    # ---- Lab Tests (Feasibility Checker) ----
    op.create_table(
        "vdesign_lab_tests",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("test_code", sa.String(50), nullable=False),
        sa.Column("test_type", sa.String(50), nullable=False),
        sa.Column("golden_sample_id", UUID(as_uuid=True), sa.ForeignKey("vdesign_golden_samples.id", ondelete="SET NULL"), nullable=True),
        sa.Column("prototype_id", UUID(as_uuid=True), sa.ForeignKey("vdesign_prototypes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("result", sa.String(20), nullable=False, server_default="RUNNING"),
        sa.Column("measured_value", sa.String(255), nullable=True),
        sa.Column("threshold_value", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("tested_by", sa.String(255), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vdesign_lab_type", "vdesign_lab_tests", ["test_type"])
    op.create_index("idx_vdesign_lab_result", "vdesign_lab_tests", ["result"])

    # ---- Handover Kits (Tooling Handover) ----
    op.create_table(
        "vdesign_handover_kits",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000001'")),
        sa.Column("kit_code", sa.String(50), nullable=False),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("contents_summary", sa.Text, nullable=False),
        sa.Column("destination", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PACKING"),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("packed_by", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_vdesign_hk_status", "vdesign_handover_kits", ["status"])
    op.create_index("idx_vdesign_hk_code", "vdesign_handover_kits", ["kit_code"])

    # ---- Seed Data ----
    op.execute(sa.text("""
INSERT INTO vdesign_golden_samples (id, sample_code, product_name, material, weight_actual, weight_spec, dimension_x_mm, convergence_pct, status, storage_zone, storage_shelf, custodian, seal_tag_id, linked_spec_id, created_by)
VALUES
    ('40000000-0000-0000-0000-000000000001', 'GS-2026-TIT-01', 'VK-Watch Titanium', 'Ti-6Al-4V', 152.050, 152.000, 44.020, 98.50, 'SEALED', 'High-Security Vault A', 'Shelf-04 Bin-12', 'Nguyen Van A', 'TAG-9921', 'SPC-DIG-V2.1', 'system'),
    ('40000000-0000-0000-0000-000000000002', 'GS-2026-ALU-01', 'VK-Speaker Housing', 'Aluminum 6061', 320.100, 320.000, 120.000, 99.00, 'ACTIVE', 'Vault B', 'Shelf-02 Bin-05', 'Tran Thi B', 'TAG-9922', 'SPC-DIG-V1.0', 'system')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vdesign_material_inbox (id, item_code, source_type, supplier_name, description, material_type, initial_assessment, status, qr_tag_id, received_by)
VALUES
    ('41000000-0000-0000-0000-000000000001', 'RAW-MAT-01', 'SUPPLIER', 'Toray Industries', 'Carbon Fiber Sheet 2mm', 'Carbon Fiber', 'Weave: 3K Twill, Color: Pantone 446C', 'PENDING', 'QR-RAW-001', 'lab_tech_01'),
    ('41000000-0000-0000-0000-000000000002', 'MKT-SMP-02', 'COMPETITOR', NULL, 'Smart Band (Broken) for teardown', 'PC-ABS', 'Housing: PC-ABS, Screen: Gorilla Glass 3', 'TESTED', 'QR-MKT-002', 'lab_tech_02')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vdesign_prototypes (id, proto_code, product_name, version_label, fabrication_method, rfid_tag_id, status, location, created_by)
VALUES
    ('42000000-0000-0000-0000-000000000001', 'PROTO-WATCH-01', 'VK-Watch', 'V1', '3D_PRINT', 'RFID-PROTO-001', 'ACTIVE', 'Lab Room 3A', 'system'),
    ('42000000-0000-0000-0000-000000000002', 'PROTO-WATCH-02', 'VK-Watch', 'V2', 'CNC', 'RFID-PROTO-002', 'ACTIVE', 'Lab Room 3A', 'system'),
    ('42000000-0000-0000-0000-000000000003', 'PROTO-SPEAKER-01', 'VK-Speaker', 'V1', 'INJECTION', 'RFID-PROTO-003', 'OBSOLETE', 'Archive Room', 'system')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vdesign_lab_tests (id, test_code, test_type, golden_sample_id, prototype_id, result, measured_value, threshold_value, notes, tested_by)
VALUES
    ('43000000-0000-0000-0000-000000000001', 'LT-STRESS-001', 'STRESS', '40000000-0000-0000-0000-000000000001', NULL, 'PASSED', '450 MPa', '>400 MPa', 'Tensile strength test passed', 'lab_eng_01'),
    ('43000000-0000-0000-0000-000000000002', 'LT-DROP-001', 'DROP', NULL, '42000000-0000-0000-0000-000000000001', 'FAILED', 'Cracked at 1.2m', 'Survive 1.5m drop', 'Housing cracked on corner impact', 'lab_eng_02'),
    ('43000000-0000-0000-0000-000000000003', 'LT-THERMAL-001', 'THERMAL', NULL, '42000000-0000-0000-0000-000000000002', 'RUNNING', NULL, '-20°C to 60°C', 'Thermal cycling in progress', 'lab_eng_01')
ON CONFLICT (id) DO NOTHING
"""))
    op.execute(sa.text("""
INSERT INTO vdesign_handover_kits (id, kit_code, product_name, contents_summary, destination, status, packed_by)
VALUES
    ('44000000-0000-0000-0000-000000000001', 'HK-WATCH-2026-01', 'VK-Watch Production Kit', '1x Injection Mold (V2), 2x Jig Set, 1x Color Sample Card, 1x Golden Sample (sealed)', 'Factory Binh Duong', 'READY', 'logistics_01'),
    ('44000000-0000-0000-0000-000000000002', 'HK-SPEAKER-2026-01', 'VK-Speaker Production Kit', '1x Aluminum Die Cast Mold, 1x Assembly Jig, 1x Paint Reference', 'Factory Hai Phong', 'PACKING', 'logistics_02')
ON CONFLICT (id) DO NOTHING
"""))


def downgrade() -> None:
    op.drop_table("vdesign_handover_kits")
    op.drop_table("vdesign_lab_tests")
    op.drop_table("vdesign_prototypes")
    op.drop_table("vdesign_material_inbox")
    op.drop_table("vdesign_golden_samples")
