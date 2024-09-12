import os
import shutil
import sys
from aiogram import types
from middlewares.authorization import is_private_chat, is_user_member
from config import REQUIRED_CHANNELS, ADMIN_IDS, DB_FILE_PATH, CHANNEL_ID
from utils.helpers import get_bot_state, set_bot_state, get_current_upload_folder
from utils.database import connect_db

# Handler for incoming documents
async def handle_document(message: types.Message):
    from main import bot
    if not is_private_chat(message):
        return
    
    user_id = message.from_user.id

    # Check if the user is a member of the required channels
    if not await is_user_member(user_id):
        join_message = ("Welcome to PC Games Bot 🪄\n\n"
                        "I have repacked PC game files downloaded from original sources 👾\n\n"
                        "A new game uploaded every day 👻\n\n"
                        "Please join our update channels and help us grow our community 😉\n")
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
        return

    # Check if awaiting a new DB upload
    if get_bot_state('awaiting_new_db_upload') and message.document.file_name == "game_management.db":
        if str(user_id) not in ADMIN_IDS:
            set_bot_state('awaiting_new_db_upload', False)
            await message.reply("You are not authorized to upload a new database file.")
            return

        # Define the path to the old and new database files
        old_db_path = DB_FILE_PATH
        new_file_path = f"new_{message.document.file_name}"

        # Download the new database file
        await message.document.download(destination_file=new_file_path)

        try:
            # Delete the old database file
            if os.path.exists(old_db_path):
                os.remove(old_db_path)
                await message.reply("Old database file deleted successfully.")
            else:
                await message.reply("Old database file not found. Proceeding with the replacement.")

            # Move the new file to replace the old database
            shutil.move(new_file_path, DB_FILE_PATH)
            set_bot_state('awaiting_new_db_upload', False)
            await message.reply("Database file replaced successfully. Restarting the bot to apply changes.")

            # Restart the bot to apply the new database changes
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            set_bot_state('awaiting_new_db_upload', False)
            await message.reply(f"An error occurred while replacing the database file: {e}")
            return

    # Existing document handling code
    # Only admins can upload files, so check admin authorization
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply("You are not authorized to upload files.")
        return

    # Get file details from the incoming document
    file_id = message.document.file_id
    file_name = message.document.file_name

    # Determine the folder ID for the current upload folder
    current_upload_folder = get_current_upload_folder(user_id)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        folder_id = None
        if current_upload_folder:
            # Get folder ID from PostgreSQL
            cursor.execute('SELECT id FROM folders WHERE name = %s', (current_upload_folder,))
            folder = cursor.fetchone()
            if folder:
                folder_id = folder[0]

        # Send the file to the storage channel and get the message ID
        sent_message = await bot.send_document(CHANNEL_ID, file_id, caption=f"New file uploaded: {file_name}")
        message_id = sent_message.message_id

        # Insert the file into the PostgreSQL database
        cursor.execute('INSERT INTO files (file_id, file_name, folder_id, message_id) VALUES (%s, %s, %s, %s)', 
                       (file_id, file_name, folder_id, message_id))
        conn.commit()

        await message.reply(f"File '{file_name}' uploaded successfully.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()