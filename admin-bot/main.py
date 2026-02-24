import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "☕ GiftForge Admin Bot

"
        "Доступные команды:
"
        "/generate - Создать QR код для подарка
"
        "/stats - Статистика
"
        "/help - Помощь

"
        "(MVP Day 1 - базовая структура)"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Генерация QR - будет реализовано на Дне 2")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Статистика - будет реализовано на Дне 4")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Помощь для бариста:

"
        "1. Используйте /generate для создания QR
"
        "2. Покажите QR клиенту
"
        "3. Клиент сканирует и получает подарок"
    )

def main():
    application = Application.builder().token(ADMIN_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("help", help_command))

    print("🤖 Admin Bot запущен")
    application.run_polling()

if __name__ == "__main__":
    main()
