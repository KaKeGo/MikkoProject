import discord
import os

from discord.ext import commands
from decouple import config
from database.database import Database
from database.users import UserDatabase


TOKEN = config('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class Mikko(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.db = Database()
        self.user_db = None
        self.log_channel_id = 1330475978258124840

    async def setup_hook(self):
        """Setup when bot is started"""
        await self.db.connect()
        self.user_db = UserDatabase(self.db.pool)
        await self.user_db.create_tables()

    async def send_log(self, message: str):
        """Send message to log channel"""
        channel = self.get_channel(self.log_channel_id)
        if channel:
            await channel.send(message)

bot = Mikko()

@bot.event
async def on_ready():
    print(f'Login like a {bot.user}')

    for guild in bot.guilds:
        for member in guild.members:
            result = await bot.user_db.add_user(member)
            if result == "New user added to Mikko_DB":
                await bot.send_log(f"{result}: {member.display_name} (ID: {member.id})")

    channel = discord.utils.get(bot.get_all_channels(), name='bot-check')
    if channel:
        await channel.send('Mikko logged in and ready to fight on live!!')

    await bot.load_extension('welcome.welcome')

@bot.event
async def on_member_join(member):
    """New member joined to server"""
    await bot.user_db.add_user(member)
    await bot.send_log(f"New member added to Mikko_DB: {member.display_name} (ID: {member.id})")

@bot.event
async def on_member_update(before, after):
    """User Change nickname"""
    if before.display_name != after.display_name:
        result = await bot.user_db.add_user(after)
        if result == "User updated successfully":
            await bot.send_log(
                f"**__Someone change his nick:__**\n"
                f"**~~{before.display_name}~~** → **<@{after.id}>**\n"
            )

@bot.command(name='last_joined')
async def last_users(ctx, limit: int = 10):
    """Last 10 users joined to the server"""
    try:
        limit = min(limit, 20)
        users = await bot.user_db.get_last_users(limit)

        if not users:
            await ctx.send("User in Mikko_DB not founded")
            return
        
        message = "Last 10 users joined to the server:\n"
        for i, user in enumerate(users, 1):
            message += f"{i}. {user['display_name']}\n"

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Something went wrong: {str(e)}")

bot.run(TOKEN)
