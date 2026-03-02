-- =============================================================
-- V6__auth_hardening.sql — Auth hardening: refresh tokens + rate limits
-- GovernanceID: SyR-PLAT-06 (Auth Hardening)
-- Step 7: Refresh token rotation, rate limit tracking.
-- =============================================================

-- ---- Refresh Tokens (opaque, DB-backed rotation) ----
CREATE TABLE IF NOT EXISTS kernel_refresh_tokens (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email      VARCHAR(255) NOT NULL REFERENCES kernel_users(email) ON DELETE CASCADE,
    token_hash      VARCHAR(64)  NOT NULL UNIQUE,   -- SHA-256 of the opaque token
    issued_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    expires_at      TIMESTAMPTZ  NOT NULL,
    revoked         BOOLEAN      NOT NULL DEFAULT FALSE,
    revoked_at      TIMESTAMPTZ,
    replaced_by     UUID         REFERENCES kernel_refresh_tokens(id),
    client_ip       VARCHAR(45),
    user_agent      VARCHAR(500)
);

CREATE INDEX idx_refresh_email ON kernel_refresh_tokens(user_email);
CREATE INDEX idx_refresh_token ON kernel_refresh_tokens(token_hash);
CREATE INDEX idx_refresh_active ON kernel_refresh_tokens(user_email, revoked, expires_at);

-- ---- Rate Limit Events (lightweight audit, optional row expiry via PG cron) ----
CREATE TABLE IF NOT EXISTS kernel_rate_limit_log (
    id         BIGSERIAL    PRIMARY KEY,
    ip_address VARCHAR(45)  NOT NULL,
    endpoint   VARCHAR(100) NOT NULL,
    event_time TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_rate_limit_ip_time ON kernel_rate_limit_log(ip_address, event_time);
