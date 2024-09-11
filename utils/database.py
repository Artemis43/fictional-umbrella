import asyncpg
import os
#from dotenv import load_dotenv

# Load environment variables from a .env file
#load_dotenv()
#user=postgres.vpzreiwdcoyaobicckun password=[YOUR-PASSWORD] host=aws-0-ap-south-1.pooler.supabase.com port=6543 dbname=postgres
DATABASE_URL = {
    "user": "postgres.vpzreiwdcoyaobicckun",
    "password": "4Rczj78ezNTFm?YK",
    "database": "postgres",
    "host": "aws-0-ap-south-1.pooler.supabase.com",
    "port": 6543
}

async def connect_to_db():
    """Create a connection pool to the database."""
    try:
        pool = await asyncpg.create_pool(
            user=DATABASE_URL["user"],
            password=DATABASE_URL["password"],
            database=DATABASE_URL["database"],
            host=DATABASE_URL["host"],
            port=DATABASE_URL["port"]
        )
        return pool
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

async def fetch_folders(pool):
    """Fetch all folders."""
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM folders;")
        return rows

async def insert_folder(pool, name, parent_id=None):
    """Insert a new folder."""
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO folders (name, parent_id) VALUES ($1, $2);",
            name, parent_id
        )

async def fetch_files(pool, folder_id):
    """Fetch files by folder_id."""
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM files WHERE folder_id=$1;", folder_id)
        return rows

async def insert_file(pool, file_id, file_name, folder_id, message_id):
    """Insert a new file."""
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO files (file_id, file_name, folder_id, message_id) VALUES ($1, $2, $3, $4);",
            file_id, file_name, folder_id, message_id
        )

async def fetch_users(pool):
    """Fetch all users."""
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM users;")
        return rows

async def insert_user(pool, user_id):
    """Insert a new user."""
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (user_id) VALUES ($1);",
            user_id
        )

# Add more functions as needed for bot_messages and bot_state tables