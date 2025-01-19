import discord
import os

from discord.ext import commands
from decouple import config
from database.database import Database


TOKEN = config('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class Mikko(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.db = Database()

    async def setup_hook(self):
        """Setup when bot is started"""
        await self.db.connect()

bot = Mikko()

@bot.event
async def on_ready():
    print(f'Login like a {bot.user}')

    channel = discord.utils.get(bot.get_all_channels(), name='bot-tests')
    if channel:
        await channel.send('Mikko logged in and ready to fight')


    await bot.load_extension('welcome.welcome')

bot.run(TOKEN)
