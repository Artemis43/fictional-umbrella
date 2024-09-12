import os

# For pyrogram client
API_ID = os.environ.get('API_ID')

# For pyrogram client
API_HASH = os.environ.get('API_HASH')

# Bot Api Token from the BotFather
API_TOKEN = os.environ.get('TOKEN')

# Admin IDs for the bot. Requests always sent to 1st ID
ADMIN_IDS = os.environ.get('ADMINS').split(',')

# Telegram Storage Channel
CHANNEL_ID = os.environ.get('CHANNEL')

# Sticker
STICKER_ID = os.environ.get('STICKER')

# To update games list (Without @)
GROUP_USERNAME = 'fitgirl_repacks_pc'

# To update games list
TOPIC_ID = 2560

# For Pyrogram client
BOT_TOKEN = os.environ.get('TOKEN')

# Webhook settings
WEBHOOK_HOST = os.environ.get('HOST_URL')
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# List of required channels to join
REQUIRED_CHANNELS = os.environ.get('SUBSCRIPTION').split(',')

# Supabase Connection String
POSTGRES_CONNECTION_STRING = os.environ.get('DB_STRING')