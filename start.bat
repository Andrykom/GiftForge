@echo off
chcp 65001 >nul
echo ☕ =========================================
echo     GiftForge MVP - Запуск инфраструктуры
echo    =========================================
echo.

REM Проверяем наличие .env
if not exist ".env" (
    echo ⚠️  Файл .env не найден. Копируем из .env.example...
    copy .env.example .env
    echo 📝 ВАЖНО: Отредактируйте .env и добавьте свои токены ботов!
    echo.
    pause
    exit /b 1
)

echo 🚀 Запускаем Postgres и Redis...
docker-compose up -d postgres redis

if errorlevel 1 (
    echo ❌ Ошибка запуска Docker Compose
    pause
    exit /b 1
)

echo ⏳ Ждем инициализации БД (5 сек)...
timeout /t 5 /nobreak >nul

echo 🔧 Применяем миграции...
docker-compose run --rm core-api alembic upgrade head

if errorlevel 0 (
    echo ✅ Инфраструктура готова!
    echo.
    echo 📋 Доступные сервисы:
    echo    Postgres: localhost:5432
    echo    Redis:    localhost:6379
    echo.
    echo 🚀 Для запуска API:     docker-compose up core-api
    echo 🤖 Для запуска ботов:  docker-compose up admin-bot client-bot
    echo 📊 Проверка статуса:   docker-compose ps
    echo.
    echo 💡 Для остановки:      docker-compose down
) else (
    echo ❌ Ошибка применения миграций
)

echo.
pause
