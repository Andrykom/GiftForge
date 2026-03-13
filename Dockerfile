# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для всех сервисов
COPY requirements.txt .
COPY core-api/requirements.txt ./core-api/
COPY core-bot/requirements.txt ./core-bot/
COPY admin-bot/requirements.txt ./admin-bot/
COPY client-bot/requirements.txt ./client-bot/

# Объединение всех зависимостей
RUN cat core-api/requirements.txt core-bot/requirements.txt \
    admin-bot/requirements.txt client-bot/requirements.txt > combined.txt && \
    pip install --no-cache-dir -r combined.txt

# Копирование общего кода
COPY core-api/ ./core-api/
COPY core-bot/ ./core-bot/
COPY admin-bot/ ./admin-bot/
COPY client-bot/ ./client-bot/
COPY database/ ./database/

# Аргумент для выбора сервиса
ARG SERVICE
ENV SERVICE=${SERVICE}

# Создаем скрипт запуска
RUN echo '#!/bin/bash\n\
if [ "$SERVICE" = "core-api" ]; then\n\
    cd core-api && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}\n\
elif [ "$SERVICE" = "core-bot" ]; then\n\
    cd core-bot && python main.py\n\
elif [ "$SERVICE" = "admin-bot" ]; then\n\
    cd admin-bot && python main.py\n\
elif [ "$SERVICE" = "client-bot" ]; then\n\
    cd client-bot && python main.py\n\
else\n\
    echo "Unknown service: $SERVICE"\n\
    exit 1\n\
fi' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]