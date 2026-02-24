#!/bin/bash
# GiftForge MVP - Quick Start Script

echo "☕ Запуск GiftForge MVP..."

# Проверяем наличие .env
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Копируем из .env.example..."
    cp .env.example .env
    echo "📝 Отредактируйте .env и добавьте свои токены!"
    exit 1
fi

# Запускаем только инфраструктуру (День 1)
echo "🚀 Запускаем Postgres и Redis..."
docker-compose up -d postgres redis

echo "⏳ Ждем инициализации БД (5 сек)..."
sleep 5

echo "🔧 Применяем миграции..."
docker-compose run --rm core-api alembic upgrade head

echo "✅ Инфраструктура готова!"
echo ""
echo "📋 Доступные сервисы:"
echo "   Postgres: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "🚀 Для запуска API: docker-compose up core-api"
echo "🤖 Для запуска ботов: docker-compose up admin-bot client-bot"
