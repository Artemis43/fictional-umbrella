import asyncpg
import logging
from typing import Optional

# Connection details
DATABASE_URL = "postgresql://user=postgres.vpzreiwdcoyaobicckun password=[YOUR-PASSWORD] host=aws-0-ap-south-1.pooler.supabase.com port=6543 dbname=postgres"

# Database connection pool
pool: Optional[asyncpg.pool.Pool] = None

async def create_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=10)
        logging.info("PostgreSQL connection pool created.")

async def close_pool():
    global pool
    if pool is not None:
        await pool.close()
        logging.info("PostgreSQL connection pool closed.")

async def fetch_all(query: str, *args):
    async with pool.acquire() as connection:
        return await connection.fetch(query, *args)

async def fetch_one(query: str, *args):
    async with pool.acquire() as connection:
        return await connection.fetchrow(query, *args)

async def execute(query: str, *args):
    async with pool.acquire() as connection:
        await connection.execute(query, *args)

async def setup_database():
    queries = [
        '''
        CREATE TABLE IF NOT EXISTS folders (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES folders (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            file_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            folder_id INTEGER,
            message_id INTEGER,
            FOREIGN KEY (folder_id) REFERENCES folders (id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS bot_messages (
            id SERIAL PRIMARY KEY,
            chat_id TEXT,
            topic_id INTEGER,
            message_id INTEGER
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS bot_state (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
        '''
    ]

    async with pool.acquire() as connection:
        for query in queries:
            await connection.execute(query)
        logging.info("Database tables created or verified.")

# Ensure the database setup is complete before running the bot
async def initialize_database():
    await create_pool()
    await setup_database()

# Call this function to close the database connection pool when shutting down
async def close_database():
    await close_pool()