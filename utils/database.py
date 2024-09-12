import psycopg2
from config import POSTGRES_CONNECTION_STRING

# Connect to PostgreSQL database
def connect_db():
    return psycopg2.connect(POSTGRES_CONNECTION_STRING)

def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Create folders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS folders (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES folders (id) ON DELETE SET NULL
    )
    ''')

    # Create files table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id SERIAL PRIMARY KEY,
        file_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        folder_id INTEGER,
        message_id INTEGER,
        FOREIGN KEY (folder_id) REFERENCES folders (id) ON DELETE CASCADE
    )
    ''')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY
    )
    ''')

    # Create bot_messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bot_messages (
        id SERIAL PRIMARY KEY,
        chat_id TEXT,
        topic_id INTEGER,
        message_id INTEGER
    )
    ''')

    # Create bot_state table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bot_state (
        key TEXT PRIMARY KEY,  -- The name of the state (e.g., 'awaiting_new_db_upload')
        value INTEGER  -- The value of the state (e.g., 0 or 1)
    )
    ''')

    # Commit changes
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()