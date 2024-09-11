from aiogram import types
from utils.database import cursor, conn
from middlewares.authorization import is_user_member, is_private_chat
from utils.helpers import set_current_upload_folder, send_or_edit_message
from config import ADMIN_IDS, REQUIRED_CHANNELS, CHANNEL_ID

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
        #global current_upload_folder

        # Only the admin can create folders
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to create folders.")
            return

        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a folder name.")
            return

        # Insert the new folder into the database
        cursor.execute('INSERT INTO folders (name) VALUES (?)', (folder_name,))
        conn.commit()

        # Set the current upload folder for the user to the newly created folder
        set_current_upload_folder(user_id, folder_name)

        await send_or_edit_message()

        await message.reply(f"Folder '{folder_name}' created and set as the current upload folder.")

# Command to rename a folder (Admin only)
async def rename_folder(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to rename folders.")
            return

        args = message.get_args().split(',')
        if len(args) != 2:
            await message.reply("Please specify the current folder name and the new folder name in the format: /renamegame <current_name>,<new_name>")
            return

        current_name, new_name = args

        # Check if the folder with the current name exists
        cursor.execute('SELECT id FROM folders WHERE name = ?', (current_name,))
        folder_id = cursor.fetchone()
        if folder_id:
            # Update the folder name in the database
            cursor.execute('UPDATE folders SET name = ? WHERE id = ?', (new_name, folder_id[0]))
            conn.commit()
            await message.reply(f"Folder '{current_name}' has been renamed to '{new_name}'.")
        else:
            await message.reply("Folder not found.")


# Command to delete a folder and its contents (Admin only)
async def delete_folder(message: types.Message):
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
        if str(message.from_user.id) not in ADMIN_IDS:
            await message.reply("You are not authorized to delete folders.")
            return

        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a folder name.")
            return

        # Get the folder ID to be deleted
        cursor.execute('SELECT id FROM folders WHERE name = ?', (folder_name,))
        folder_id = cursor.fetchone()
        if folder_id:
            folder_id = folder_id[0]

            # Get the message IDs of the files in the folder
            cursor.execute('SELECT message_id FROM files WHERE folder_id = ?', (folder_id,))
            message_ids = cursor.fetchall()

            # Delete the files from the channel and the database
            for message_id in message_ids:
                await bot.delete_message(CHANNEL_ID, message_id[0])
            cursor.execute('DELETE FROM files WHERE folder_id = ?', (folder_id,))

            # Delete the folder from the database
            cursor.execute('DELETE FROM folders WHERE id = ?', (folder_id,))
            conn.commit()

            await send_or_edit_message()

            await message.reply(f"Folder '{folder_name}' and its contents deleted.")
        else:
            await message.reply("Folder not found.")
