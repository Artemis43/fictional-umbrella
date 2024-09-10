import logging
from pyrogram import Client
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import API_ID, API_HASH, API_TOKEN, BOT_TOKEN
from keep_alive import keep_alive

# To keep the bot running
keep_alive()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize pyrogram client - to update games list in the group
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# New db upload initiated only during /restore
# awaiting_new_db_upload = False

# Global dictionary to track the current upload folder for each admin
# So that all admins can upload files simultaneously
current_upload_folders = {}

from handlers import start, folder, file, document, download, broadcast, backup, about_help, stop, sync

# Register handlers
dp.register_message_handler(start.start, commands=['start'])
dp.register_message_handler(folder.create_folder, commands=['newgame'])
dp.register_message_handler(folder.rename_folder, commands=['renamegame'])
dp.register_message_handler(folder.delete_folder, commands=['deletegame'])
dp.register_message_handler(file.rename_file, commands=['renamefile'])
dp.register_message_handler(file.delete_file, commands=['deletefile'])
dp.register_message_handler(document.handle_document, content_types=['document'])
dp.register_message_handler(download.get_all_files, commands=['get'])
dp.register_message_handler(broadcast.broadcast_message, commands=['broadcast'])
dp.register_message_handler(backup.send_backup, commands=['backup'])
dp.register_message_handler(backup.new_db, commands=['restore'])
dp.register_message_handler(about_help.help, commands=['help'])
dp.register_message_handler(about_help.about, commands=['about'])
dp.register_message_handler(stop.stop, commands=['stop'])
dp.register_message_handler(sync.sync_database_command, commands=['forcedsyncdb'])
dp.register_callback_query_handler(start.process_callback_1, lambda c: c.data)
dp.register_callback_query_handler(start.process_callback_2, lambda c: c.data)

from utils.webhook import on_startup, on_shutdown

# Start the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)