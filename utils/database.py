import sqlite3
from config import DB_FILE_PATH, ADMIN_IDS

# Connect to the SQLite database
conn = sqlite3.connect(DB_FILE_PATH)
cursor = conn.cursor()

# Create tables for folders and files
cursor.execute('''
CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES folders (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    folder_id INTEGER,
    message_id INTEGER,
    FOREIGN KEY (folder_id) REFERENCES folders (id)
)
''')
conn.commit()

# Create table for users for broadcast
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
''')
conn.commit()

# Ensure table for storing message ID
cursor.execute('''
CREATE TABLE IF NOT EXISTS bot_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    topic_id INTEGER,
    message_id INTEGER
)
''')
conn.commit()

# Table to store global bot states
cursor.execute('''
CREATE TABLE IF NOT EXISTS bot_state (
    key TEXT PRIMARY KEY,  -- The name of the state (e.g., 'awaiting_new_db_upload')
    value INTEGER  -- The value of the state (e.g., 0 or 1)
)
''')
conn.commit()

def add_user_to_db(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()