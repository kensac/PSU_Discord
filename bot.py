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
    if message.message.content.lower().startswith('$info'):
        text=message.message.content.lower().replace("$info",'').strip()
    else:
        text=message.message.content.lower().replace("$i",'').strip()

    soup=htmlParsing.find_course_by_number(text)
    result=htmlParsing.get_all_info(soup)

    if result[0]:

        # implement something that can handle over 2000 charecters

        output=f"{result[0]}\n\n{result[1]}\n\n{result[2]}\n\n"+'\n\n'.join(i for i in result[3:])

        await message.channel.send(f"```{output}```")
    
    else:
        await message.channel.send(f"```{text.upper()} could not be found.```")

@bot.command(name='credits', aliases=['c'])
async def credits(message):
    if message.message.content.lower().startswith('$credits'):
        text=message.message.content.lower().replace("$credits",'').strip()
    else:
        text=message.message.content.lower().replace("$c",'').strip()
        
    soup=htmlParsing.find_course_by_number(text)
    result=htmlParsing.get_all_info(soup)

    

    if result[0]:

        # implement something that can handle over 2000 charecters

        await message.channel.send(f"```{result[0]}\n\n{result[1]}```")
    
    else:
        await message.channel.send(f"```{text.upper()} could not be found.```")

@bot.command(name='extras', aliases=['e'])
async def credits(message):
    if message.message.content.lower().startswith('$extras'):
        text=message.message.content.lower().replace("$extras",'').strip()
    else:
        text=message.message.content.lower().replace("$e",'').strip()
        
    soup=htmlParsing.find_course_by_number(text)
    result=htmlParsing.get_all_info(soup)

    

    if result[0]:
        output=f"{result[0]}\n\n"+'\n\n'.join(i for i in result[3:])

        # implement something that can handle over 2000 charecters

        await message.channel.send(f"```{output}```")
    
    else:
        await message.channel.send(f"```{text.upper()} could not be found.```")

@bot.command(name='attr', aliases=["a"])
async def attr(message):
    if message.message.content.lower().startswith('$attr'):
        text=message.message.content.lower().replace("$attr",'').strip()
    else:
        text=message.message.content.lower().replace("$a",'').strip()
    
    result=htmlParsing.find_by_attribute(text)
    
    if result[0]:
        output='\n'.join("\t".join(i) for i in result)

        await message.channel.send(f"```{output}```")


bot.run(TOKEN)