from pyrogram.errors import MessageNotModified
from config import GROUP_USERNAME, TOPIC_ID
import asyncpg
from utils.database import connect_to_db

# Function to add a user to the database asynchronously
async def add_user_to_db(user_id):
    pool = await connect_to_db()
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO users (user_id) VALUES ($1)
            ON CONFLICT (user_id) DO NOTHING
        ''', user_id)
    await pool.close()

# Function to set the current upload folder for a user (in-memory storage)
def set_current_upload_folder(user_id, folder_name):
    from main import current_upload_folders
    current_upload_folders[user_id] = folder_name

# Function to get the current upload folder for a user (in-memory storage)
def get_current_upload_folder(user_id):
    from main import current_upload_folders
    return current_upload_folders.get(user_id)

# Function to set the bot's state in the database asynchronously
async def set_bot_state(key: str, value: bool):
    pool = await connect_to_db()
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO bot_state (key, value) VALUES ($1, $2)
            ON CONFLICT (key) DO UPDATE SET value = excluded.value
        ''', key, int(value))
    await pool.close()

# Function to get the bot's state from the database asynchronously
async def get_bot_state(key: str) -> bool:
    pool = await connect_to_db()
    async with pool.acquire() as connection:
        result = await connection.fetchval('SELECT value FROM bot_state WHERE key = $1', key)
    await pool.close()

    if result is not None:
        return bool(result)
    return False

# Function to send or edit a message asynchronously
async def send_or_edit_message():
    from main import app
    pool = await connect_to_db()

    # Fetch the list of folders from the database
    async with pool.acquire() as connection:
        folders = await connection.fetch('SELECT name FROM folders ORDER BY name ASC')

    # Format the message
    folder_list = "\n\n".join([folder['name'] for folder in folders])
    message_text = f"**Games uploaded in Bot:**\n\n`{folder_list}`\n\nAny issues: [Report](https://t.me/Art3mis_adminbot)"

    # Check if we have already sent a message in this topic
    async with pool.acquire() as connection:
        result = await connection.fetchval(
            'SELECT message_id FROM bot_messages WHERE chat_id = $1 AND topic_id = $2',
            GROUP_USERNAME, TOPIC_ID
        )

    async with app:
        if result:
            # We have a message ID, try to edit it
            message_id = result
            try:
                await app.edit_message_text(chat_id=GROUP_USERNAME, message_id=message_id, text=message_text)
            except MessageNotModified:
                pass  # Ignore if the message is not modified
            except Exception as e:
                print(f"Failed to edit message: {e}")
        else:
            # We need to send a new message
            sent_message = await app.send_message(chat_id=GROUP_USERNAME, text=message_text, reply_to_message_id=TOPIC_ID)
            
            # Store the new message ID in the database
            async with pool.acquire() as connection:
                await connection.execute('''
                    INSERT INTO bot_messages (chat_id, topic_id, message_id) VALUES ($1, $2, $3)
                ''', GROUP_USERNAME, TOPIC_ID, sent_message.message_id)
    await pool.close()