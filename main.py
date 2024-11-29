import discord
import os

from discord.ext import commands
from decouple import config


TOKEN = config('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Login like a {bot.user}')

    channel = discord.utils.get(bot.get_all_channels(), name='test')
    if channel:
        await channel.send('Mikko logged in and ready to fight')


    await bot.load_extension('welcome.welcome')
    await bot.load_extension('rules.rules')

bot.run(TOKEN)
