import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions
from utils.database import connect_db
from config import STICKER_ID, REQUIRED_CHANNELS
from middlewares.authorization import is_private_chat, is_user_member
from utils.helpers import add_user_to_db

# Function to send the UI
async def send_ui(chat_id, message_id=None, current_folder=None, selected_letter=None):
    from main import bot
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch the number of files and folders
    cursor.execute('SELECT COUNT(*) FROM folders')
    folder_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM files')
    file_count = cursor.fetchone()[0]

    # Visual representation of the current location
    current_path = "Root"
    if current_folder:
        current_path = f"Root / {current_folder}"

    # Create inline keyboard for navigation
    keyboard = InlineKeyboardMarkup()

    # Alphabet buttons
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_buttons = [InlineKeyboardButton(letter, callback_data=f'letter_{letter}') for letter in alphabet]

    # Add a button for symbols
    alphabet_buttons.insert(0, InlineKeyboardButton("❗", url='https://t.me/Fitgirl_adminbot'))

    # Add alphabet buttons in rows of 5-6 buttons per row
    row_width = 7
    for i in range(0, len(alphabet_buttons), row_width):
        keyboard.row(*alphabet_buttons[i:i+row_width])

    # Add navigation buttons only if a folder is selected
    if current_folder:
        keyboard.add(InlineKeyboardButton("🥱 Back", callback_data='back'))

    keyboard.add(InlineKeyboardButton("🙃 Refresh", callback_data='root'))

    # Compose the UI message text
    text = (
        f"**Welcome to The Fitgirl Bot 🪄**\n\n"
        f"**New game added every 3 hrs 👾**\n\n"
        f"**Complete List of Games:** [Here](https://t.me/fitgirl_repacks_pc/2560)\n\n"
        f"**How to Use:** /help\n\n"
        f"**📁 Total Games:** {folder_count}\n\n"
        f"**Games: (Select letter 👇)**\n\n"
    )

    # Fetch and list folders and files based on the current folder or selected letter
    if selected_letter:
        if selected_letter == "#":
            cursor.execute('SELECT name FROM folders WHERE parent_id IS NULL AND (name ~ %s OR name ~ %s) ORDER BY name', ('[^A-Za-z0-9]*', '[!@#$%^&*()_+{}|:<>?]*'))
        else:
            cursor.execute('SELECT name FROM folders WHERE parent_id IS NULL AND name LIKE %s ORDER BY name', (f'{selected_letter}%',))
        folders = cursor.fetchall()

        cursor.execute('SELECT file_name FROM files WHERE folder_id IS NULL ORDER BY file_name')
        files = cursor.fetchall()

        # Add folders and files to the text
        for folder in folders:
            text += f"|-📁 {folder[0]}\n\n"
    
    text += "Files are in .bin form\nDue to Telegram's restrictions, they are split into 2 GB or 4 GB files. Merge them before install.\n\nRefer: [Click here](https://t.me/fitgirl_repacks_pc/969/970)\n\n⬇ Report to Admin if no files"

    try:
        if message_id:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
    except exceptions.MessageNotModified:
        pass  # Handle the exception gracefully by ignoring it

    cursor.close()
    conn.close()

# Command to start the bot and show the UI
async def start(message: types.Message):
    if not is_private_chat(message):
        return

    from main import bot
    user_id = message.from_user.id

    # Add user to the PostgreSQL database
    add_user_to_db(user_id)

    if not await is_user_member(user_id):
        sticker_msg = await bot.send_sticker(message.chat.id, STICKER_ID)
        await asyncio.sleep(3)
        await bot.delete_message(message.chat.id, sticker_msg.message_id)

        join_message = ("Welcome to PC Games Bot 🪄\n\n"
                        "I have repacked PC game files downloaded from original sources 👾\n\n"
                        "A new game uploaded every day 👻\n\n"
                        "Please join our update channels and help us grow our community 😉\n")

        keyboard = InlineKeyboardMarkup(row_width=1)
        for channel in REQUIRED_CHANNELS:
            button = InlineKeyboardButton(text=channel, url=f"https://t.me/{channel.lstrip('@')}")
            keyboard.add(button)

        await message.reply(join_message, reply_markup=keyboard)
    else:
        sticker_msg = await bot.send_sticker(message.chat.id, STICKER_ID)
        await asyncio.sleep(2)
        await bot.delete_message(message.chat.id, sticker_msg.message_id)

        # Send the UI
        await send_ui(message.chat.id)