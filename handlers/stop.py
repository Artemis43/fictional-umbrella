import logging
import sys
from aiogram import types
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS
from utils.database import cursor, conn
from handlers.sync import FLAG_FILE_PATH
import os

async def stop(message: types.Message):
    from main import bot

    # Prevent the restart logic when stopping the bot manually
    if os.path.exists(FLAG_FILE_PATH):
        os.remove(FLAG_FILE_PATH)

    if not is_private_chat(message):
        return
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to stop the bot.")
        return

    await message.reply("Bot is stopping...")

    conn.commit()

    # Path to the database file
    db_file_path = 'game_management.db'

    try:
        await bot.send_document(message.chat.id, types.InputFile(db_file_path))
    except Exception as e:
        logging.error(f"Error sending backup file: {e}")
        await message.reply("Error sending backup file. Please try again later.")

    # Safely shut down the bot instead of using sys.exit()
    print("Stopping bot gracefully...")
    await bot.session.close()  # Close bot session
    await bot.shutdown()  # Shutdown the bot

    # Manually raise a SystemExit to stop the bot
    raise SystemExit("Bot stopped by admin command.")
