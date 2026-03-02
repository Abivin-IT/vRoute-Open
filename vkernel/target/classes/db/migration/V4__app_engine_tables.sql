-- =============================================================
-- V4__app_engine_tables.sql — App Registry & Permissions
-- GovernanceID: 0.1.0-SCHEMA  (SyR-PLAT-00 + SyR-PLAT-01.02)
-- DB-backed app registry + permission injection registry
-- =============================================================

-- ---- App Registry (SyR-PLAT-00) ----
CREATE TABLE IF NOT EXISTS kernel_app_registry (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    app_id          VARCHAR(150) NOT NULL UNIQUE,     -- com.vcorp.vfinance
    name            VARCHAR(100) NOT NULL,
    version         VARCHAR(30)  NOT NULL,
    icon            VARCHAR(10)  DEFAULT '📦',
    status          VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE', -- ACTIVE | INACTIVE | FAILED
    manifest_json   JSONB        NOT NULL DEFAULT '{}',
    installed_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    installed_by    VARCHAR(255),
    uninstalled_at  TIMESTAMPTZ
);

CREATE INDEX idx_app_registry_status ON kernel_app_registry(status);

-- ---- Permission Registry (SyR-PLAT-01.02 Dynamic Permission Injection) ----
CREATE TABLE IF NOT EXISTS kernel_permissions (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    app_id          VARCHAR(150) NOT NULL,             -- owning app
    permission_code VARCHAR(150) NOT NULL UNIQUE,      -- finance.invoice.approve
    name            VARCHAR(150) NOT NULL,
    description     TEXT,
    category        VARCHAR(50),
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    registered_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_perms_app_id  ON kernel_permissions(app_id);
CREATE INDEX idx_perms_code    ON kernel_permissions(permission_code);

-- ---- Seed: vKernel built-in apps ----
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by) VALUES
    ('com.vcorp.kernel.settings', 'Settings',  '1.0.0', '⚙️', 'ACTIVE',
     '{"app":{"id":"com.vcorp.kernel.settings","name":"Settings","version":"1.0.0"}}', 'system'),
    ('com.vcorp.kernel.appstore', 'App Store',  '1.0.0', '🛒', 'ACTIVE',
     '{"app":{"id":"com.vcorp.kernel.appstore","name":"App Store","version":"1.0.0"}}',  'system')
ON CONFLICT (app_id) DO NOTHING;
