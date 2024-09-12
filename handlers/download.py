from aiogram import types
from middlewares.authorization import is_private_chat, is_user_member
from config import REQUIRED_CHANNELS
from utils.database import connect_db

# Command to retrieve and send all files in a specified folder
async def get_all_files(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return
    
    user_id = message.from_user.id

    if not await is_user_member(user_id):
        join_message = ("Welcome to PC Games Bot 🪄\n\n"
                        "I have repacked PC game files downloaded from original sources 👾\n\n"
                        "A new game uploaded every day 👻\n\n"
                        "Please join our update channels and help us grow our community 😉\n")
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a game name.")
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Get the folder ID from the database
            cursor.execute('SELECT id FROM folders WHERE name = %s', (folder_name,))
            folder_id = cursor.fetchone()

            if folder_id:
                folder_id = folder_id[0]

                # Get the file IDs and names in the folder
                cursor.execute('SELECT file_id, file_name FROM files WHERE folder_id = %s', (folder_id,))
                files = cursor.fetchall()

                if files:
                    for file in files:
                        await bot.send_document(message.chat.id, file[0], caption=file[1])
                else:
                    await message.reply("No files found in the specified game.")
            else:
                await message.reply("Game not found.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()