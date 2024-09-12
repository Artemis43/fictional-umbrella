import logging
from aiogram import types
from middlewares.authorization import is_private_chat
from config import ADMIN_IDS
from utils.database import connect_db

# Async function to broadcast a message to all users
async def broadcast_message(message: types.Message):
    if not is_private_chat(message):
        return
    from main import bot

    # Only admins can broadcast messages
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to send broadcasts.")
        return

    # Get the message to broadcast
    broadcast_message = message.get_args()
    if not broadcast_message:
        await message.reply("Please provide a message to broadcast.")
        return

    conn = connect_db()
    cursor = conn.cursor()

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
    finally:
        cursor.close()
        conn.close()