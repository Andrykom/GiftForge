FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir python-telegram-bot==20.7 httpx==0.25.2

COPY . .

CMD ["python", "main.py"]
