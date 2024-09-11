import asyncio
from aiogram import types, exceptions
from middlewares.authorization import is_private_chat, is_user_member
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.helpers import add_user_to_db
from config import REQUIRED_CHANNELS, STICKER_ID
from asyncpg import Pool
from utils.database import connect_to_db

async def send_ui(chat_id, message_id=None, current_folder=None, selected_letter=None):
    from main import bot
    pool: Pool = await connect_to_db()

    # Fetch the number of files and folders asynchronously
    async with pool.acquire() as connection:
        folder_count = await connection.fetchval('SELECT COUNT(*) FROM folders')
        file_count = await connection.fetchval('SELECT COUNT(*) FROM files')

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

    # Add alphabet buttons in rows of 7 buttons per row
    row_width = 7
    for i in range(0, len(alphabet_buttons), row_width):
        keyboard.row(*alphabet_buttons[i:i+row_width])

    # Add navigation buttons only if in a subfolder
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
        async with pool.acquire() as connection:
            if selected_letter == "#":
                folders = await connection.fetch(
                    'SELECT name FROM folders WHERE parent_id IS NULL AND (name ~ $1 OR name ~ $2) ORDER BY name',
                    '[^A-Za-z0-9]*', '[!@#$%^&*()_+{}|:<>?]*'
                )
            else:
                folders = await connection.fetch(
                    'SELECT name FROM folders WHERE parent_id IS NULL AND name LIKE $1 ORDER BY name',
                    f'{selected_letter}%'
                )
            files = await connection.fetch(
                'SELECT file_name FROM files WHERE folder_id IS NULL ORDER BY file_name'
            )

        # Add folders and files to the text
        for folder in folders:
            text += f"|-📁 {folder['name']}\n\n"
        # for file in files:
        #     text += f"|-💀 {file['file_name']}\n"

    # Append instructions to the text
    text += (
        "Files are in .bin form\n"
        "Due to Telegram's restrictions, they are split into 2 GB or 4 GB files. Merge them before install.\n\n"
        "Refer: [Click here](https://t.me/fitgirl_repacks_pc/969/970)\n\n"
        "⬇ Report to Admin if no files"
    )

    try:
        if message_id:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=text,
                reply_markup=keyboard, parse_mode='Markdown'
            )
        else:
            await bot.send_message(
                chat_id, text, reply_markup=keyboard, parse_mode='Markdown'
            )
    except exceptions.MessageNotModified:
        pass  # Handle the exception gracefully by ignoring it

    # Close the connection pool
    await pool.close()

#Callback Query handler to filter UI based on inline selections
async def process_callback_1(callback_query: types.CallbackQuery):
    from main import bot
    global current_upload_folder
    user_id = callback_query.from_user.id

    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, join_message)
        return

    code = callback_query.data

    if code == 'back':
        current_upload_folder = None
        await send_ui(callback_query.from_user.id, callback_query.message.message_id)
    elif code == 'root':
        await send_ui(callback_query.from_user.id, callback_query.message.message_id)
    elif code.startswith('letter_'):
        selected_letter = code.split('_')[1]
        await send_ui(callback_query.from_user.id, callback_query.message.message_id, selected_letter=selected_letter)
    else:
        current_upload_folder = code
        await send_ui(callback_query.from_user.id, callback_query.message.message_id, current_folder=current_upload_folder)

    await bot.answer_callback_query(callback_query.id)

# Callback query handler for inline buttons
async def process_callback_2(callback_query: types.CallbackQuery):
    if callback_query.data == 'back':
        # Logic to go back to the previous folder
        await send_ui(callback_query.message.chat.id)  # This should be updated with the actual previous folder logic
    elif callback_query.data == 'root':
        await send_ui(callback_query.message.chat.id)
    # Handle other callback data if necessary

# Command to start the bot and show the UI
async def start(message: types.Message):
    if not is_private_chat(message):
        return

    user_id = message.from_user.id
    add_user_to_db(user_id)

    # Check if the user is a member of the required channels
    if not await is_user_member(user_id):
        # Send and delete a welcome sticker
        sticker_msg = await message.answer_sticker(STICKER_ID)
        await asyncio.sleep(3)
        await message.delete()

        # Provide instructions to join channels
        join_message = (
            "Welcome to PC Games Bot 🪄\n\n"
            "I have repacked PC game files downloaded from original sources 👾\n\n"
            "A new game uploaded every day 👻\n\n"
            "Please join our update channels and help us grow our community 😉\n"
        )
        keyboard = InlineKeyboardMarkup(row_width=1)
        for channel in REQUIRED_CHANNELS:
            button = InlineKeyboardButton(text=channel, url=f"https://t.me/{channel.lstrip('@')}")
            keyboard.add(button)
        await message.reply(join_message, reply_markup=keyboard)
    else:
        # Send and delete a sticker and show the UI
        sticker_msg = await message.answer_sticker(STICKER_ID)
        await asyncio.sleep(2)
        await message.delete()
        await send_ui(message.chat.id)