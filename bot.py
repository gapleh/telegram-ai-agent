
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from litellm import completion

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store conversation history
conversation_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am an AI assistant powered by LiteLLM. "
        "Send me a message and I will respond."
    )
    conversation_history[user.id] = []

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("I am an AI assistant. Just send me a message!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using LiteLLM."""
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Add user message to history
    conversation_history[user_id].append({"role": "user", "content": user_message})

    messages = conversation_history[user_id]

    try:
        # Use LiteLLM to get a response from the AI model
        response = completion(
            model=os.getenv("LITELLM_MODEL", "qwen/qwen3.6-27b"),
            messages=messages,
            api_key=os.getenv("OPENAI_API_KEY"),
            api_base=os.getenv("OPENAI_BASE_URL"),
        )
        ai_response = response.choices[0].message.content
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error calling LiteLLM: {e}")
        await update.message.reply_text("Sorry, I encountered an error trying to get a response.")

def main() -> None:
    """Start the bot."""
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_bot_token).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # On non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
