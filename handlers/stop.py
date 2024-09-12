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
    if not is_private_chat(message):
        return
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to stop the bot.")
        return

    await message.reply("Bot is stopping...")
    # Ensure the bot exits gracefully and does not trigger a restart
    sys.exit("Bot stopped by admin command.")