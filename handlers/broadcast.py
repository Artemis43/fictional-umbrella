import logging
from aiogram import types
from config import ADMIN_IDS
from middlewares.authorization import is_private_chat
from utils.database import cursor

async def broadcast_message(message: types.Message):
    if not is_private_chat(message):
        return
    from main import bot
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to send broadcasts.")
        return

    broadcast_message = message.get_args()
    if not broadcast_message:
        await message.reply("Please provide a message to broadcast.")
        return

    try:
        # Fetch all users from the database
        cursor.execute('SELECT user_id FROM users')
        user_ids = cursor.fetchall()

        # Send the broadcast message to all users
        for user_id in user_ids:
            try:
                await bot.send_message(user_id[0], broadcast_message)
            except Exception as e:
                logging.error(f"Error sending broadcast to user {user_id[0]}: {e}")

        await message.reply(f"Broadcast sent to {len(user_ids)} users.")
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        await message.reply("Error fetching users. Please try again later.")
