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
                    user_id BIGINT PRIMARY KEY,                     -- ID user from discord (never change)
                    display_name TEXT,                              -- Username (server nick)
                    global_name TEXT,                               -- Discord username
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
    async def add_user(self, member: discord.Member):
        """Add or update user to database if not existing"""
        exists = await self.user_exists(member.id)

        if not exists:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO users (user_id, display_name, global_name)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                            display_name = $2,
                            global_name = $3
                ''',
                    member.id,
                    member.display_name,
                    member.global_name
                )
                return "New user added to Mikko_DB"
        else:
            async with self.pool.acquire() as conn:
                current_data = await self.get_user(member.id)
                if current_data['display_name'] != member.display_name or \
                    current_data['global_name'] != member.global_name:
                    await conn.execute('''
                        UPDATE users
                        SET display_name = $2, global_name = $3
                        WHERE user_id = $1
                    ''', member.id, member.display_name, member.global_name)
                    return "User updated successfully"
                return "User exist in Mikko_DB"
    
    async def get_user(self, user_id: int):
        """Take user information form db"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                SELECT * FROM users WHERE user_id = $1
            ''', user_id)

    async def user_exists(self, user_id: int) -> bool:
        """Check if user exists"""
        user = await self.get_user(user_id)
        return user is not None
    
    async def get_last_users(self, limit: int = 10):
        """Get the 10 last users in to Mikko_DB"""
        async with self.pool.acquire() as conn:
            return await conn.fetch('''
                SELECT user_id, display_name, global_name, joined_at
                FROM users
                ORDER BY joined_at DESC
                LIMIT $1
            ''', limit)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Update member nick on server"""
        if before.display_name != after.display_name:
            await self.add_user(after)