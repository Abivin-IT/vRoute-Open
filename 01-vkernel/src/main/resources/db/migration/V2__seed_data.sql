-- =============================================================
-- V2__seed_data.sql — Core reference data
-- GovernanceID: 2.0.0-SEED
-- Currencies + Countries essential for VN-first platform
-- =============================================================

-- ---- Currencies ----
INSERT INTO kernel_currencies (code, name, symbol, decimals, is_active) VALUES
    ('VND', 'Vietnamese Dong',   '₫',  0, TRUE),
    ('USD', 'US Dollar',         '$',  2, TRUE),
    ('EUR', 'Euro',              '€',  2, TRUE),
    ('JPY', 'Japanese Yen',      '¥',  0, TRUE),
    ('CNY', 'Chinese Yuan',      '¥',  2, TRUE),
    ('KRW', 'South Korean Won',  '₩',  0, TRUE),
    ('THB', 'Thai Baht',         '฿',  2, TRUE),
    ('SGD', 'Singapore Dollar',  'S$', 2, TRUE)
ON CONFLICT (code) DO NOTHING;

-- ---- Countries (ASEAN + key trade partners) ----
INSERT INTO kernel_countries (code, name, phone_code, currency, is_active) VALUES
    ('VN', 'Vietnam',       '+84',  'VND', TRUE),
    ('US', 'United States', '+1',   'USD', TRUE),
    ('SG', 'Singapore',     '+65',  'SGD', TRUE),
    ('JP', 'Japan',         '+81',  'JPY', TRUE),
    ('KR', 'South Korea',   '+82',  'KRW', TRUE),
    ('CN', 'China',         '+86',  'CNY', TRUE),
    ('TH', 'Thailand',      '+66',  'THB', TRUE),
    ('DE', 'Germany',       '+49',  'EUR', TRUE)
ON CONFLICT (code) DO NOTHING;

-- ---- Default tenant ----
INSERT INTO kernel_tenants (id, code, name, tax_id, country_code, status) VALUES
    ('00000000-0000-0000-0000-000000000001', 'DEFAULT', 'Default Tenant', NULL, 'VN', 'ACTIVE')
ON CONFLICT (code) DO NOTHING;
