from middlewares.authorization import is_private_chat, is_user_member
from config import REQUIRED_CHANNELS, ADMIN_IDS
from utils.database import connect_db
from utils.helpers import send_or_edit_message, set_current_upload_folder
from aiogram import types

# Command to create a new folder
async def create_folder(message: types.Message):
    if not is_private_chat(message):
        return
    
    user_id = message.from_user.id
    
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        # Only the admin can create folders
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to create games.")
            return

        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a game name.")
            return

        # Insert the new folder into the PostgreSQL database
        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO folders (name) VALUES (%s) RETURNING id', (folder_name,))
            folder_id = cursor.fetchone()[0]
            conn.commit()

            # Set the current upload folder for the user to the newly created folder
            set_current_upload_folder(user_id, folder_name)

            await send_or_edit_message()

            await message.reply(f"Game '{folder_name}' created and set as the current upload folder.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()