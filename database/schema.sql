-- GiftForge MVP - Схема базы данных (День 1)

-- Таблица: businesses (Кофейни)
CREATE TABLE businesses (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    total_deposited NUMERIC(12,2) DEFAULT 0,
    spent NUMERIC(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Таблица: baristas (Баристы)
CREATE TABLE baristas (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(64),
    full_name VARCHAR(128),
    business_id VARCHAR(32) REFERENCES businesses(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица: qr_tokens (QR коды)
CREATE TABLE qr_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_hash VARCHAR(64) UNIQUE NOT NULL,
    business_id VARCHAR(32) REFERENCES businesses(id),
    barista_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    used_by BIGINT,
    is_used BOOLEAN DEFAULT FALSE
);

-- Таблица: gift_history (История подарков)
CREATE TABLE gift_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id VARCHAR(32) REFERENCES businesses(id),
    qr_token_id UUID REFERENCES qr_tokens(id),
    user_id BIGINT NOT NULL,
    telegram_username VARCHAR(64),
    rarity VARCHAR(20) NOT NULL, -- common, rare, epic, mythic
    stars_spent INTEGER NOT NULL,
    gift_telegram_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'
);

-- Индексы для производительности
CREATE INDEX idx_qr_tokens_expires ON qr_tokens(expires_at) WHERE is_used = FALSE;
CREATE INDEX idx_gift_history_user ON gift_history(user_id);
CREATE INDEX idx_gift_history_business ON gift_history(business_id);
