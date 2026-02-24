import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import httpx

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CORE_BOT_TOKEN = os.getenv("CORE_BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://core-api:8000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение"""
    await update.message.reply_text(
        "🎁 GiftForge Core Bot\n\n"
        "Этот бот отвечает за отправку подарков Stars.\n"
        "Используйте Client Bot для получения подарков."
    )

async def send_gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ручная отправка подарка (для тестирования)"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Использование: /sendgift <user_id> <rarity>\n"
            "Пример: /sendgift 123456789 common"
        )
        return

    try:
        user_id = int(context.args[0])
        rarity = context.args[1]

        # Здесь будет реальная отправка через Telegram Gifts API
        # Пока имитируем
        await update.message.reply_text(
            f"✅ Подарок отправлен!\n"
            f"Пользователь: {user_id}\n"
            f"Редкость: {rarity}"
        )

    except ValueError:
        await update.message.reply_text("❌ Неверный user_id")

async def health_check(context: ContextTypes.DEFAULT_TYPE):
    """Периодическая проверка здоровья"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                logger.info("✅ API is healthy")
            else:
                logger.warning(f"⚠️ API health check failed: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ API connection error: {e}")

def main():
    if not CORE_BOT_TOKEN:
        logger.error("CORE_BOT_TOKEN not set!")
        return

    application = Application.builder().token(CORE_BOT_TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendgift", send_gift_command))

    # Периодические задачи
    # job_queue = application.job_queue
    # job_queue.run_repeating(health_check, interval=60, first=10)

    logger.info("🤖 Core Bot запущен")
    application.run_polling()

if __name__ == "__main__":
    main()
