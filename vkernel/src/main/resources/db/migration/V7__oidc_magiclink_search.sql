-- =============================================================
-- V7__oidc_magiclink_search.sql
-- Adds: OIDC provider links, magic link tokens, FTS search index.
-- GovernanceID: 1.6.0-SCHEMA
-- =============================================================

-- ---- g1_iam: OIDC linked accounts ----
CREATE TABLE IF NOT EXISTS kernel_oidc_accounts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email      VARCHAR(255) NOT NULL REFERENCES kernel_users(email),
    provider        VARCHAR(30)  NOT NULL,         -- GOOGLE | MICROSOFT | GITHUB
    provider_sub    VARCHAR(255) NOT NULL,         -- subject claim from IdP
    provider_email  VARCHAR(255),
    display_name    VARCHAR(255),
    picture_url     TEXT,
    raw_claims      JSONB        DEFAULT '{}',
    linked_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    UNIQUE(provider, provider_sub)
);

CREATE INDEX idx_oidc_user  ON kernel_oidc_accounts(user_email);
CREATE INDEX idx_oidc_prov  ON kernel_oidc_accounts(provider, provider_sub);

-- ---- g1_iam: Magic link (passwordless auth) ----
CREATE TABLE IF NOT EXISTS kernel_magic_links (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL,
    token_hash      VARCHAR(64)  NOT NULL UNIQUE,
    expires_at      TIMESTAMPTZ  NOT NULL,
    used            BOOLEAN      NOT NULL DEFAULT FALSE,
    used_at         TIMESTAMPTZ,
    client_ip       VARCHAR(45),
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_magic_email ON kernel_magic_links(email);

-- ---- g5_search: Full-Text Search materialized view ----
-- Unified search across all core entities (SyR-PLAT-02.02)
CREATE TABLE IF NOT EXISTS kernel_search_index (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(30)  NOT NULL,         -- USER | STAKEHOLDER | APP | EVENT
    entity_id       UUID         NOT NULL,
    tenant_id       VARCHAR(100) DEFAULT 'default',
    title           VARCHAR(500) NOT NULL,
    body            TEXT,                           -- searchable text blob
    tsv             TSVECTOR,                       -- pre-computed tsvector
    indexed_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_search_tsv    ON kernel_search_index USING gin(tsv);
CREATE INDEX idx_search_type   ON kernel_search_index(entity_type);
CREATE INDEX idx_search_tenant ON kernel_search_index(tenant_id);
CREATE UNIQUE INDEX idx_search_entity ON kernel_search_index(entity_type, entity_id);

-- Trigger: auto-update tsvector on insert/update
CREATE OR REPLACE FUNCTION search_index_tsv_trigger() RETURNS trigger AS $$
BEGIN
    NEW.tsv := setweight(to_tsvector('simple', coalesce(NEW.title, '')), 'A') ||
               setweight(to_tsvector('simple', coalesce(NEW.body, '')), 'B');
    RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_search_tsv
    BEFORE INSERT OR UPDATE ON kernel_search_index
    FOR EACH ROW EXECUTE FUNCTION search_index_tsv_trigger();
