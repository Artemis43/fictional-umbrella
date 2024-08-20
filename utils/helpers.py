from utils.database import cursor, conn
from pyrogram.errors import MessageNotModified
from config import GROUP_USERNAME, TOPIC_ID

# Function to set the current upload folder for a user
def set_current_upload_folder(user_id, folder_name):
    from main import current_upload_folders
    current_upload_folders[user_id] = folder_name

# Function to get the current upload folder for a user
def get_current_upload_folder(user_id):
    from main import current_upload_folders
    return current_upload_folders.get(user_id)

# Function to set the DB upload await state
def set_bot_state(key: str, value: bool):
    cursor.execute('''
        INSERT INTO bot_state (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (key, int(value)))
    conn.commit()

# Function to get the DB upload await state
def get_bot_state(key: str) -> bool:
    cursor.execute('SELECT value FROM bot_state WHERE key = ?', (key,))
    result = cursor.fetchone()
    if result:
        return bool(result[0])
    return False

async def send_or_edit_message():
    from main import app
    # Fetch the list of folders from the database
    cursor.execute('SELECT name FROM folders ORDER BY name ASC')
    folders = cursor.fetchall()

    # Format the message
    folder_list = "\n\n".join([folder[0] for folder in folders])
    message_text = f"**Games uploaded in Bot:**\n\n`{folder_list}`\n\nAny issues: [Report](https://t.me/Fitgirl_adminbot)"

    # Check if we have already sent a message in this topic
    cursor.execute('SELECT message_id FROM bot_messages WHERE chat_id = ? AND topic_id = ?', (GROUP_USERNAME, TOPIC_ID))
    result = cursor.fetchone()

    async with app:
        if result:
            # We have a message ID, try to edit it
            message_id = result[0]
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
            cursor.execute('INSERT INTO bot_messages (chat_id, topic_id, message_id) VALUES (?, ?, ?)', (GROUP_USERNAME, TOPIC_ID, sent_message.id))
            conn.commit()
