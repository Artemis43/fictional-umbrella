import logging
import sys
from aiogram import types
from middlewares.authorization import is_private_chat
from utils.database import cursor
from config import ADMIN_IDS

# Command to stop the bot (Admin only)
async def stop(message: types.Message):
    if not is_private_chat(message):
        return
    from main import bot
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to stop the bot.")
        return

    await message.reply("Bot is stopping...")

    # Comment out the original stop code
    # await bot.close()
    # executor.stop(dp)
    # executor.start_polling(dp, skip_updates=True)
    try:
        # Fetch all users from the database
        cursor.execute('SELECT user_id FROM users')
        user_ids = cursor.fetchall()

        # Send the broadcast message to all users
        for user_id in user_ids:
            try:
                await bot.send_message(user_id[0], "Regular maintenance 👾 for 10 mins.")
            except Exception as e:
                logging.error(f"Error sending broadcast to user {user_id[0]}: {e}")

        await message.reply(f"Broadcast sent to {len(user_ids)} users.")
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        await message.reply("Error fetching users. Please try again later.")
    
    # Use sys.exit to terminate the bot
    sys.exit("Bot stopped by admin command.")
