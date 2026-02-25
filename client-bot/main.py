import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import asyncio

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Подгружаем переменные окружения из файла .env (если запускаете локально)
load_dotenv()
logger = logging.getLogger(__name__)

from services.api_client import api_client

CLIENT_BOT_TOKEN = os.getenv("CLIENT_BOT_TOKEN")
if not CLIENT_BOT_TOKEN:
    logger.debug("CLIENT_BOT_TOKEN not found in environment after load_dotenv()")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка /start с deep link параметром"""
    # Log args and raw message for debugging deep-link behavior
    try:
        msg_text = update.message.text if update.message else None
    except Exception:
        msg_text = None
    logger.info(f"/start invoked by user {update.effective_user.id if update.effective_user else 'unknown'}; args={context.args}; text={msg_text}")
    user = update.effective_user

    # Проверяем deep link параметр
    param = None
    if context.args and len(context.args) > 0:
        param = context.args[0]
    else:
        # Фоллбек: некоторые клиенты Telegram не прокидывают args при нажатии Start.
        # Пытаемся распарсить параметр прямо из текста сообщения: '/start qr_...'
        try:
            text = update.message.text if update.message else ""
            if text and text.startswith("/start "):
                possible = text.split(" ", 1)[1].strip()
                if possible:
                    param = possible
                    logger.debug(f"Parsed start param from text fallback: {param}")
        except Exception:
            param = None

    if param and param.startswith("qr_"):
        qr_token = param[3:]  # Убираем префикс

        # Отправляем сообщение о обработке
        processing_msg = await update.message.reply_text(
            "🎁 *Обработка вашего подарка...*\n"
            "Пожалуйста, подождите несколько секунд.",
            parse_mode="Markdown"
        )

        try:
            # Отправляем запрос к API
            result = await api_client.send_gift(
                user_id=user.id,
                qr_token=qr_token,
                username=user.username
            )

            if result.get("success"):
                # Успешно получили подарок
                rarity = result.get("rarity", "common")
                name = result.get("name", "Подарок")
                emoji = result.get("emoji", "🎁")
                stars = result.get("stars_spent", 0)

                await processing_msg.delete()

                # Красивое сообщение о подарке
                await update.message.reply_text(
                    f"{emoji} *Поздравляем!* {emoji}\n\n"
                    f"Вы получили: *{name}*!\n"
                    f"Редкость: {rarity.capitalize()}\n"
                    f"Стоимость: {stars} Stars\n\n"
                    f"🎉 Наслаждайтесь вашим подарком!\n\n"
                    f"_Спасибо, что выбрали CoffeeShop! ☕_",
                    parse_mode="Markdown"
                )

                logger.info(f"Gift sent to user {user.id}, rarity: {rarity}")

            else:
                await processing_msg.edit_text(
                    "❌ *Не удалось получить подарок*\n"
                    "Возможно, QR код уже использован или истёк.",
                    parse_mode="Markdown"
                )

        except Exception as e:
            logger.error(f"Error processing gift: {e}")
            await processing_msg.edit_text(
                "❌ *Ошибка обработки*\n"
                "Попробуйте отсканировать QR код ещё раз или обратитесь к бариста.",
                parse_mode="Markdown"
            )

    elif param:
        # Неизвестный параметр
        await update.message.reply_text(
            "⚠️ *Неверная ссылка*\n"
            "Пожалуйста, получите QR код у бариста.",
            parse_mode="Markdown"
        )

    else:
        # Обычный /start без параметров
        await update.message.reply_text(
            "☕ *Добро пожаловать в CoffeeShop!*\n\n"
            "🎁 Получите подарок у бариста!\n"
            "Он выдаст вам уникальный QR код.\n\n"
            "Просто отсканируйте его камерой Telegram "
            "или нажмите на ссылку — подарок придёт автоматически!\n\n"
            "_Ждём вас снова! ☕_",
            parse_mode="Markdown"
        )


# (Normal operation: only /start handler is registered)

def main():
    if not CLIENT_BOT_TOKEN:
        logger.error("CLIENT_BOT_TOKEN not set!")
        return

    application = Application.builder().token(CLIENT_BOT_TOKEN).build()

    # Удаляем возможный webhook (если кто-то ставил webhook, он мешает polling)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(application.bot.delete_webhook())
        logger.debug("Called delete_webhook() to avoid polling conflict")
    except Exception as e:
        logger.debug(f"delete_webhook() failed or not needed: {e}")

    application.add_handler(CommandHandler("start", start))

    logger.info("🤖 Client Bot запущен")
    application.run_polling()

if __name__ == "__main__":
    main()
