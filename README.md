# GiftForge MVP

A Telegram Stars gifting system for coffee shops.

## Quick Start

1. **Clone and navigate to the directory:**
```bash
cd giftforge-mvp

```


2. **Create a .env file:**
```bash
cp .env.example .env
# Edit .env and add your tokens

```


3. **Start the infrastructure:**
```bash
docker-compose up -d postgres redis

```


4. **Apply migrations:**
```bash
docker-compose run --rm core-api alembic upgrade head

```


5. **Start all services:**
```bash
docker-compose up -d

```



## Checking the Setup

* API: http://localhost:8000/docs
* Postgres: localhost:5432
* Redis: localhost:6379

## Day 1: What's Ready

* [x] Project structure
* [x] Docker Compose with Postgres and Redis
* [x] SQLAlchemy models
* [x] Alembic migrations
* [x] Basic FastAPI server

## 🪟 For Windows Users

If `start.sh` closes immediately after running:

1. Use `start.bat` (double-click)
2. Or open `WINDOWS_GUIDE.md` for detailed instructions.

Quick start in CMD:

```cmd
start.bat

```
