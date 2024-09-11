from aiogram import types
from middlewares.authorization import is_user_member, is_private_chat
from utils.helpers import set_current_upload_folder, send_or_edit_message
from config import ADMIN_IDS, REQUIRED_CHANNELS, CHANNEL_ID
from utils.database import connect_to_db
from utils.helpers import set_current_upload_folder, send_or_edit_message
from asyncpg import Connection

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

        # Insert the new folder into the database
        pool = await connect_to_db()
        async with pool.acquire() as connection:
            await connection.execute('INSERT INTO folders (name) VALUES ($1)', folder_name)

        # Set the current upload folder for the user to the newly created folder
        set_current_upload_folder(user_id, folder_name)

        # Update the message in the channel
        await send_or_edit_message()

        await message.reply(f"Game '{folder_name}' created and set as the current upload folder.")

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
            await message.reply("You are not authorized to rename games.")
            return

        args = message.get_args().split(',')
        if len(args) != 2:
            await message.reply("Please specify the current game name and the new game name in the format: /renamegame <current_name>,<new_name>")
            return

        current_name, new_name = args

        # Check if the folder with the current name exists and rename it
        pool = await connect_to_db()
        async with pool.acquire() as connection:
            folder_id = await connection.fetchval('SELECT id FROM folders WHERE name = $1', current_name)

            if folder_id:
                await connection.execute('UPDATE folders SET name = $1 WHERE id = $2', new_name, folder_id)
                await message.reply(f"Game '{current_name}' has been renamed to '{new_name}'.")
            else:
                await message.reply("Game not found.")

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
            await message.reply("You are not authorized to delete games.")
            return

        folder_name = message.get_args()
        if not folder_name:
            await message.reply("Please specify a game name.")
            return

        # Get the folder ID to be deleted
        pool = await connect_to_db()
        async with pool.acquire() as connection:
            folder_id = await connection.fetchval('SELECT id FROM folders WHERE name = $1', folder_name)

            if folder_id:
                # Get the message IDs of the files in the folder
                message_ids = await connection.fetch('SELECT message_id FROM files WHERE folder_id = $1', folder_id)

                # Delete the files from the channel and the database
                for message_id in message_ids:
                    try:
                        await bot.delete_message(CHANNEL_ID, message_id['message_id'])
                    except Exception as e:
                        print(f"Failed to delete message {message_id['message_id']}: {e}")

                await connection.execute('DELETE FROM files WHERE folder_id = $1', folder_id)
                await connection.execute('DELETE FROM folders WHERE id = $1', folder_id)

                await send_or_edit_message()

                await message.reply(f"Game '{folder_name}' and its contents deleted.")
            else:
                await message.reply("Game not found.")