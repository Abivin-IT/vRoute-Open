-- =============================================================
-- V3__event_tables.sql — Event Bus & Audit Trail
-- GovernanceID: 3.0.0-SCHEMA  (SyR-PLAT-03)
-- Append-only event log + subscription registry
-- =============================================================

-- ---- Immutable event log (SyR-PLAT-03.03 Audit Trail) ----
CREATE TABLE IF NOT EXISTS kernel_event_log (
    id               UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type       VARCHAR(100) NOT NULL,              -- e.g. SALES_ORDER_CONFIRMED
    event_version    VARCHAR(10)  NOT NULL DEFAULT '1.0',
    source_app       VARCHAR(100) NOT NULL,
    payload          JSONB        NOT NULL DEFAULT '{}',
    correlation_id   VARCHAR(100),
    status           VARCHAR(20)  NOT NULL DEFAULT 'QUEUED', -- QUEUED | DELIVERED | FAILED
    subscribers      JSONB        DEFAULT '[]',           -- snapshot of notified apps
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now()
    -- NO updated_at: append-only, immutable by design (NFR-PLAT-03)
);

CREATE INDEX idx_event_log_type      ON kernel_event_log(event_type);
CREATE INDEX idx_event_log_source    ON kernel_event_log(source_app);
CREATE INDEX idx_event_log_corr      ON kernel_event_log(correlation_id);
CREATE INDEX idx_event_log_created   ON kernel_event_log(created_at DESC);
CREATE INDEX idx_event_log_payload   ON kernel_event_log USING gin(payload);

-- ---- Subscription registry (SyR-PLAT-03.02) ----
CREATE TABLE IF NOT EXISTS kernel_event_subscriptions (
    id               UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    subscriber_app   VARCHAR(100) NOT NULL,
    event_type       VARCHAR(100) NOT NULL,
    status           VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE | PAUSED
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    UNIQUE(subscriber_app, event_type)
);

CREATE INDEX idx_subs_event_type ON kernel_event_subscriptions(event_type);
CREATE INDEX idx_subs_app        ON kernel_event_subscriptions(subscriber_app);
