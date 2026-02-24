import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

CLIENT_BOT_TOKEN = os.getenv("CLIENT_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and context.args[0].startswith("qr_"):
        qr_token = context.args[0][3:]
        await update.message.reply_text(
            f"🎁 Получение подарка...
"
            f"(QR токен: {qr_token[:20]}...)

"
            f"Будет реализовано на Дне 5"
        )
    else:
        await update.message.reply_text(
            "☕ Добро пожаловать в CoffeeShop!

"
            "Попросите бариста QR-код для получения подарка.

"
            "(MVP Day 1 - базовая структура)"
        )

def main():
    application = Application.builder().token(CLIENT_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("🤖 Client Bot запущен")
    application.run_polling()

if __name__ == "__main__":
    main()
