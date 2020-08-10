import discord
from variables import *
from discord.ext import commands
import json
import random
client=commands.Bot(command_prefix=';')
f=open('messages.json')
messages=json.load(f)

@client.event
async def on_ready():
    print('y')

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel)=="dhairya-kartik-tarun-gajwani":
            await channel.send(random.choice(messages['WELCOME']).format(member.mention))

@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel)=="dhairya-kartik-tarun-gajwani":
            await channel.send(random.choice(messages['BYE']).format(member.mention))

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)}ms ping hai behen ke ghode')

@client.command()
async def echo(ctx,*,msg):
    await ctx.send(msg)

@client.command(aliases=['clear','delete'])
@commands.has_role('Desi patthe')
async def purge(ctx,amount=5):
    await ctx.channel.purge(limit=amount+1)
@purge.error
async def clear_error(ctx,error):
    if isinstance(error,commands.MissingRole):
        await ctx.send('You lack the role Desi patthe for this cmd')

@client.command()
async def kick(ctx,member:discord.Member,*,reason='no reason bruh'):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx,member:discord.Member,*,reason='no reason bruh'):
    await member.ban(reason=reason)

client.run(BOT_TOKEN)