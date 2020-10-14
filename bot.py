import discord
from variables_ import *
from discord.ext import commands
import json
import random
import os
import time

client = commands.Bot(command_prefix=';', case_insensitive=True)
file_ = open('choice.json')
choice_ = json.load(file_)


@client.event
async def on_ready():
    print('y')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="Trinidad Chutney",
        url='https://www.youtube.com/watch?v=22T_K_PrhC0',
        details='I\'m just vibing, move on',
        large_image_url='https://toppng.com/uploads/preview/trinidad-and-tobago-flag-115629907007duxiy4wvo.png',
        small_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Flag_of_Pakistan.svg/320px-Flag_of_Pakistan.svg.png',
        large_image_text='Jai Trinidad',
        small_image_text='Jai Pakistan'
    ))
    # print(GOOGLE_API)
    # print(type(GOOGLE_API))

for py_file in os.listdir('./cogs'):
    if py_file.endswith('py'):  # and py_file != 'variables_.py':
        client.load_extension(f'cogs.{py_file[: -3]}')

# client.load_extension('guild-specific-cogs')

# @client.command()
# async def load(ctx, *, msg):
#     client.load_extension(f'cogs.{msg}')

# @client.command()
# async def unload(ctx, *, msg):
#     client.unload_extension(f'cogs.{msg}')


client.run(BOT_TOKEN)
