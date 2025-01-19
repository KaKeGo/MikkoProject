import discord

from discord.ext import commands


class UserDatabase:
    def __init__(self, pool):
        self.pool = pool

    async def create_tables(self):
        """Create user tables in the database"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT,         # ID user from discord (never change)
                    display_name TEXT,      # Username (server nick)
                    global_name TEXT,       # Discord username
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                )
            ''')
            
    async def add_user(self, member: discord.Member):
        """Add or update user in database"""
        pass