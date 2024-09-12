import sys
from aiogram import types
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS
from utils.database import connect_db

async def stop(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return

    # Check if the user is an admin
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to stop the bot.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Check if the user ID exists in the database
    user_id = message.from_user.id
    cursor.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    if result:
        await message.reply("Bot is stopping...")
        # Ensure the bot exits gracefully and does not trigger a restart
        sys.exit("Bot stopped by admin command.")
    else:
        await message.reply("You need to start the bot first.")