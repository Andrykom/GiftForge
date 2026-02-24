-- Инициализация тестовых данных для GiftForge MVP
INSERT INTO businesses (id, name, total_deposited, spent) 
VALUES ('COFFEE_001', 'Test Coffee Shop', 50000.0, 0.0)
ON CONFLICT (id) DO NOTHING;

INSERT INTO baristas (telegram_id, username, full_name, business_id, is_active)
VALUES (123456789, 'test_barista', 'Test Barista', 'COFFEE_001', true)
ON CONFLICT (telegram_id) DO NOTHING;
