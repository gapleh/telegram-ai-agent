import os
import requests
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conversation_history = {}

BASE_URL = os.getenv("OPENAI_BASE_URL").rstrip("/")
API_KEY = os.getenv("OPENAI_API_KEY")


def ask_ai(messages):

    r = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen/qwen3.6-27b",
            "messages": messages,
            "temperature": 0.7
        },
        timeout=120
    )

    if r.status_code != 200:
        raise Exception(f"{r.status_code}: {r.text}")

    return r.json()["choices"][0]["message"]["content"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ready 🚀")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": text
    })

    try:

        response = ask_ai(conversation_history[user_id])

        conversation_history[user_id].append({
            "role": "assistant",
            "content": response
        })

        await update.message.reply_text(response)

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            f"Error:\n{str(e)[:1000]}"
        )


def main():

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise Exception("TELEGRAM_BOT_TOKEN missing")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
