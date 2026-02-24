#!/bin/bash
# GiftForge MVP - Quick Start Script (Linux/Mac/Git Bash)

echo "☕ ========================================="
echo "    GiftForge MVP - Запуск инфраструктуры"
echo "   ========================================="

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверяем наличие .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Файл .env не найден. Копируем из .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}📝 ВАЖНО: Отредактируйте .env и добавьте свои токены ботов!${NC}"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

echo "🚀 Запускаем Postgres и Redis..."
docker-compose up -d postgres redis

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ошибка запуска Docker Compose${NC}"
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

echo "⏳ Ждем инициализации БД (5 сек)..."
sleep 5

echo "🔧 Применяем миграции..."
docker-compose run --rm core-api alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Инфраструктура готова!${NC}"
    echo ""
    echo "📋 Доступные сервисы:"
    echo "   Postgres: localhost:5432"
    echo "   Redis:    localhost:6379"
    echo ""
    echo -e "${GREEN}🚀 Для запуска API:${NC}     docker-compose up core-api"
    echo -e "${GREEN}🤖 Для запуска ботов:${NC}  docker-compose up admin-bot client-bot"
    echo -e "${GREEN}📊 Проверка статуса:${NC}   docker-compose ps"
    echo ""
    echo -e "${YELLOW}💡 Совет: Для фонового запуска используйте флаг -d${NC}"
else
    echo -e "${RED}❌ Ошибка применения миграций${NC}"
fi

echo ""
read -p "Нажмите Enter для закрытия окна..."
