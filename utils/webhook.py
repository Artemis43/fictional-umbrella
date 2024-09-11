import logging
from config import WEBHOOK_URL
import logging
from aiogram import Dispatcher

# Function to be called on bot startup
async def on_startup(dispatcher: Dispatcher):
    from main import bot
    logging.info("Setting up webhook...")
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook setup complete.")

# Function to be called on bot shutdown
async def on_shutdown(dispatcher: Dispatcher):
    from main import bot
    logging.warning("Shutting down...")
    await bot.delete_webhook()

    # Close PostgreSQL connection
    from utils.database import conn
    conn.close()

    logging.warning("Bye!")