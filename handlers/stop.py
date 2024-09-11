import logging
import sys
from aiogram import types
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS
from aiogram.types import InputFile
from utils.database import pool  # Ensure the connection pool is imported

async def stop(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return
    
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to stop the bot.")
        return

    await message.reply("Bot is stopping...")

    # Commit any pending transactions if using asyncpg with transactions
    # Not necessary with asyncpg if transactions are committed automatically
    
    # Path to the database file
    db_file_path = 'game_management.db'
    
    try:
        # Send the backup file to the admin
        await bot.send_document(message.chat.id, InputFile(db_file_path))
    except Exception as e:
        logging.error(f"Error sending backup file: {e}")
        await message.reply("Error sending backup file. Please try again later.")
        return

    # Close the connection pool
    if pool:
        await pool.close()

    # Ensure the bot exits gracefully and does not trigger a restart
    logging.info("Bot stopped by admin command.")
    sys.exit("Bot stopped by admin command.")