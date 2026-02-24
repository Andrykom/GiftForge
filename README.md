# GiftForge MVP

Система подарков Telegram Stars для кофеен.

## Быстрый старт

1. **Клонируйте и перейдите в папку:**
   ```bash
   cd giftforge-mvp
   ```

2. **Создайте .env файл:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env, добавьте свои токены
   ```

3. **Запустите инфраструктуру:**
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Примените миграции:**
   ```bash
   docker-compose run --rm core-api alembic upgrade head
   ```

5. **Запустите все сервисы:**
   ```bash
   docker-compose up -d
   ```

## Проверка работы

- API: http://localhost:8000/docs
- Postgres: localhost:5432
- Redis: localhost:6379

## День 1: Что готово

- [x] Структура проекта
- [x] Docker Compose с Postgres и Redis
- [x] SQLAlchemy модели
- [x] Alembic миграции
- [x] Базовый FastAPI сервер

## 🪟 Для Windows пользователей

Если `start.sh` закрывается сразу после запуска:
1. Используйте `start.bat` (двойной клик)
2. Или откройте `WINDOWS_GUIDE.md` для подробной инструкции

Быстрый старт в CMD:
```cmd
start.bat
```
