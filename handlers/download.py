from aiogram import types
from config import REQUIRED_CHANNELS
from middlewares.authorization import is_private_chat, is_user_member
from utils.database import cursor

# Command to retrieve and send all files in a specified folder
async def get_all_files(message: types.Message):
    if not is_private_chat(message):
        return
    from main import bot
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a game name.")
            return

        # Get the folder ID
        cursor.execute('SELECT id FROM folders WHERE name = ?', (folder_name,))
        folder_id = cursor.fetchone()
        if folder_id:
            folder_id = folder_id[0]

            # Get the file IDs and names in the folder
            cursor.execute('SELECT file_id, file_name FROM files WHERE folder_id = ?', (folder_id,))
            files = cursor.fetchall()

            if files:
                for file in files:
                    await bot.send_document(message.chat.id, file[0], caption=file[1])
            else:
                await message.reply("No files found in the specified game.")
        else:
            await message.reply("Game not found.")
