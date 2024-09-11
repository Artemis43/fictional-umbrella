import logging
from aiogram import types
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS
import os
from aiogram import types
from utils.helpers import set_bot_state

# Command to send a backup of the database file (Admin only)
async def send_backup(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to get the backup.")
        return

    # Path to the local database file
    db_file_path = 'game_management.db'
    
    # Check if the file exists and send it
    if os.path.exists(db_file_path):
        try:
            await bot.send_document(message.chat.id, types.InputFile(db_file_path))
        except Exception as e:
            logging.error(f"Error sending backup file: {e}")
            await message.reply("Error sending backup file. Please try again later.")
    else:
        await message.reply("Backup file not found. Please ensure the database file exists.")

# Command to replace the existing database file with a new one (initiates upload)
async def new_db(message: types.Message):
    if not is_private_chat(message):
        return

    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to upload a new database file.")
        return

    # Set the bot state to await new DB upload
    set_bot_state('awaiting_new_db_upload', True)
    await message.reply("Please upload the new 'game_management.db' file to replace the existing database.")