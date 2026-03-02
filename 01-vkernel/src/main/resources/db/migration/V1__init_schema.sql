-- =============================================================
-- V1__init_schema.sql — vKernel Core OS Schema
-- GovernanceID: 0.0.0-SCHEMA
-- Creates all core tables: users, tenants, stakeholders,
-- currencies, countries. Replaces JPA ddl-auto.
-- =============================================================

-- ---- g1_iam: kernel_users (existing, now Flyway-managed) ----
CREATE TABLE IF NOT EXISTS kernel_users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    roles       VARCHAR(255) NOT NULL DEFAULT 'STAFF',
    tenant_id   VARCHAR(100),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON kernel_users(email);
CREATE INDEX idx_users_tenant ON kernel_users(tenant_id);

-- ---- g2_data: tenants ----
CREATE TABLE IF NOT EXISTS kernel_tenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code            VARCHAR(50)  NOT NULL UNIQUE,
    name            VARCHAR(255) NOT NULL,
    tax_id          VARCHAR(50),
    country_code    VARCHAR(2)   DEFAULT 'VN',
    status          VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE',
    metadata        JSONB        DEFAULT '{}',
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- ---- g2_data: stakeholders (Golden Records — SyR-PLAT-02.00) ----
CREATE TABLE IF NOT EXISTS kernel_stakeholders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID         NOT NULL REFERENCES kernel_tenants(id),
    type            VARCHAR(30)  NOT NULL DEFAULT 'CUSTOMER',
    code            VARCHAR(100) NOT NULL,
    name            VARCHAR(255) NOT NULL,
    email           VARCHAR(255),
    phone           VARCHAR(50),
    address         TEXT,
    metadata        JSONB        DEFAULT '{}',
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    UNIQUE(tenant_id, code)
);

CREATE INDEX idx_stakeholders_tenant ON kernel_stakeholders(tenant_id);
CREATE INDEX idx_stakeholders_type ON kernel_stakeholders(type);
CREATE INDEX idx_stakeholders_name ON kernel_stakeholders USING gin(to_tsvector('simple', name));
CREATE INDEX idx_stakeholders_metadata ON kernel_stakeholders USING gin(metadata);

-- ---- g2_data: currencies ----
CREATE TABLE IF NOT EXISTS kernel_currencies (
    code        VARCHAR(3)   PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    symbol      VARCHAR(10)  NOT NULL,
    decimals    SMALLINT     NOT NULL DEFAULT 2,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ---- g2_data: countries ----
CREATE TABLE IF NOT EXISTS kernel_countries (
    code        VARCHAR(2)   PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    phone_code  VARCHAR(10),
    currency    VARCHAR(3)   REFERENCES kernel_currencies(code),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);
