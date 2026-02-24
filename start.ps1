# GiftForge MVP - Quick Start Script (PowerShell)
Write-Host "☕ =========================================" -ForegroundColor Cyan
Write-Host "    GiftForge MVP - Запуск инфраструктуры" -ForegroundColor Cyan
Write-Host "   =========================================" -ForegroundColor Cyan
Write-Host ""

# Проверяем .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Файл .env не найден. Копируем из .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "📝 ВАЖНО: Отредактируйте .env и добавьте свои токены ботов!" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "🚀 Запускаем Postgres и Redis..." -ForegroundColor Green
docker-compose up -d postgres redis

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка запуска Docker Compose" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "⏳ Ждем инициализации БД (5 сек)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "🔧 Применяем миграции..." -ForegroundColor Green
docker-compose run --rm core-api alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Инфраструктура готова!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Доступные сервисы:" -ForegroundColor Cyan
    Write-Host "   Postgres: localhost:5432"
    Write-Host "   Redis:    localhost:6379"
    Write-Host ""
    Write-Host "🚀 Для запуска API:     docker-compose up core-api" -ForegroundColor Green
    Write-Host "🤖 Для запуска ботов:  docker-compose up admin-bot client-bot" -ForegroundColor Green
    Write-Host "📊 Проверка статуса:   docker-compose ps" -ForegroundColor Yellow
    Write-Host "💡 Для остановки:      docker-compose down" -ForegroundColor Yellow
} else {
    Write-Host "❌ Ошибка применения миграций" -ForegroundColor Red
}

Write-Host ""
Read-Host "Нажмите Enter для закрытия окна"
