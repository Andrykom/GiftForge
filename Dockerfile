# Multi-stage build for GiftForge services

# Core API Service
FROM python:3.11-slim AS core-api

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY core-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core-api/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Core Bot Service
FROM python:3.11-slim AS core-bot

WORKDIR /app

RUN pip install --no-cache-dir python-telegram-bot==20.7 httpx==0.25.2

COPY core-bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

COPY core-bot/ .

CMD ["python", "main.py"]

# Admin Bot Service
FROM python:3.11-slim AS admin-bot

WORKDIR /app

RUN pip install --no-cache-dir python-telegram-bot==20.7 httpx==0.25.2 qrcode==7.4.2 pillow==10.1.0

COPY admin-bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

COPY admin-bot/ .

CMD ["python", "main.py"]

# Client Bot Service
FROM python:3.11-slim AS client-bot

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY client-bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY client-bot/ .

CMD ["python", "main.py"]
