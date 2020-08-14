import discord
from variables_ import *
from discord.ext import commands
import json
import random
import os

client=commands.Bot(command_prefix=';')
file_ = open('choice.json')
choice_ = json.load(file_)

@client.event
async def on_ready():
    print('y')
    # print(GOOGLE_API)
    # print(type(GOOGLE_API))

for py_file in os.listdir('./cogs'):
    if py_file.endswith('py'): #and py_file != 'variables_.py':
        client.load_extension(f'cogs.{py_file[: -3]}')

# client.load_extension('guild-specific-cogs')


@client.event
async def on_member_join(member):
    _channel=client.get_channel(MY_SERVER_CHANNEL)
    _embed=discord.Embed(title=f'WELCOME {member.name}',
                     url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                     description=f'{random.choice(choice_["WELCOME"]).format(member.mention)}'
                )
    _embed.add_field(name='Member',
                value=f'{member.guild.member_count}',
                inline=True
            )
    # _embed.set_image(url='https://media1.tenor.com/images/a47d5d571e6cbeb46a660338641d4e9c/tenor.gif')
    _embed.set_image(url='https://media.tenor.com/images/215762eb3dc67aa6b2625e14f573ea91/tenor.gif')

    await _channel.send(embed=_embed)
    

@client.event
async def on_member_remove(member):
    _channel=client.get_channel(MY_SERVER_CHANNEL)
    _embed=discord.Embed(title=f'SAYONARA {member.name}',
                     url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                     description=f'{random.choice(choice_["BYE"]).format(member.mention)}'
                )
    _embed.add_field(name='Member',
                value=f'{member.guild.member_count + 1}',
                inline=True
            )
    _embed.set_image(url='https://media.giphy.com/media/XHr6LfW6SmFa0/giphy.gif')
    await _channel.send(embed=_embed)

@client.command()
async def load(ctx, *, msg):
    client.load_extension(f'cogs.{msg}')

@client.command()
async def unload(ctx, *, msg):
    client.unload_extension(f'cogs.{msg}')

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)}ms ping hai behen ke ghode')

@client.command()
async def echo(ctx, *, msg):
    await ctx.send(msg)

@client.command(aliases=['clear', 'delete'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
# @purge.error
# async def clear_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send('You lack the role Desi patthe for this cmd')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,
            member:discord.Member,
            *, reason='no reason bruh'
        ):
        await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, 
            member:discord.Member, 
            *, reason='no reason bruh'
        ):
        await member.ban(reason=reason)

client.run(BOT_TOKEN)