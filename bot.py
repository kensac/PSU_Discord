import os
import discord
import random
from discord.ext import commands
import htmlParsing

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='info', aliases=['i'])
async def info(message):

    text=message.message.content.lower().strip("$info").strip()
    soup=htmlParsing.find_course_by_number(text)
    result=htmlParsing.get_all_info(soup)

    # implement something that can handle over 2000 charecters

    await message.channel.send(f'{result[0]}\n{result[1]}\n{result[2]}')

bot.run(TOKEN)