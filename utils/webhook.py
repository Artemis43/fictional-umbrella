import logging
from utils.database import connect_db, initialize_database
from config import WEBHOOK_URL

# Startup function to set the webhook
async def on_startup(dispatcher):
    from main import bot
    await bot.set_webhook(WEBHOOK_URL)

    initialize_database()

# Shutdown function to delete the webhook and close the database connection
async def on_shutdown(dispatcher):
    from main import bot
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    
    conn = connect_db()
    # Close the PostgreSQL connection if needed (e.g., a global connection)
    conn.close()  # Assuming a global connection is being used
    logging.warning('Bye!')