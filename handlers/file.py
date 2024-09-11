from aiogram import types
from utils.database import cursor, conn
from middlewares.authorization import is_user_member, is_private_chat
from config import ADMIN_IDS, REQUIRED_CHANNELS, CHANNEL_ID

# Command to rename a file (Admin only)
async def rename_file(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every 3 hours 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to rename files.")
            return

        args = message.get_args().split(',')
        if len(args) != 2:
            await message.reply("Please specify the current file name and the new file name in the format: /renamefile <current_name>,<new_name>")
            return

        current_name, new_name = args

        # Check if the file with the current name exists
        cursor.execute('SELECT id FROM files WHERE file_name = ?', (current_name,))
        file_id = cursor.fetchone()
        if file_id:
            # Update the file name in the database
            cursor.execute('UPDATE files SET file_name = ? WHERE id = ?', (new_name, file_id[0]))
            conn.commit()
            await message.reply(f"File '{current_name}' has been renamed to '{new_name}'.")
        else:
            await message.reply("File not found.")


# Command to delete a file by name (Admin only)
async def delete_file(message: types.Message):
    if not is_private_chat(message):
        return
    from main import bot
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every 3 hours 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to delete files.")
            return

        file_name = message.get_args()
        if not file_name:
            await message.reply("Please specify a file name.")
            return

        # Get the message ID of the file to be deleted
        cursor.execute('SELECT message_id FROM files WHERE file_name = ?', (file_name,))
        message_id = cursor.fetchone()
        if message_id:
            message_id = message_id[0]

            # Delete the file from the database
            cursor.execute('DELETE FROM files WHERE file_name = ?', (file_name,))
            conn.commit()

            # Delete the message from the channel
            await bot.delete_message(CHANNEL_ID, message_id)

            await message.reply(f"File '{file_name}' deleted.")
        else:
            await message.reply("File not found.")
