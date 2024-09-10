import logging
from aiogram import types
from utils.database import conn
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS

# Command to send a backup of the database file (Admin only)
async def send_backup(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to get the backup.")
        return
    
    # Commit any pending transactions to ensure the database is up to date
    conn.commit()

    # Path to the database file
    db_file_path = 'game_management.db'
    
    try:
        await bot.send_document(message.chat.id, types.InputFile(db_file_path))
    except Exception as e:
        logging.error(f"Error sending backup file: {e}")
        await message.reply("Error sending backup file. Please try again later.")


# Command to replace the existing database file with a new one
async def new_db(message: types.Message):
    from middlewares.authorization import is_private_chat
    from utils.helpers import set_bot_state
    if not is_private_chat(message):
        return

    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to upload a new database file.")
        return

    set_bot_state('awaiting_new_db_upload', True)
    await message.reply("Please upload the new 'game_management.db' file to replace the existing database.")
