import os
import discord
from discord.ext import commands

class Failures(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('Missing roles')
        # elif isinstance(error, commands.MissingPermissions):
        #     await ctx.send('Sorry bruh, but you dont have the perms')   
        # elif isinstance(error, commands.MissingRequiredArgument):
        #     await ctx.send('At least enter a value bruh')
        # elif isinstance(error, commands.BadArgument):
        #     await ctx.send('Bad argument type')
        # elif isinstance(error, commands.CommandInvokeError):
        #     await ctx.send('The other person has a high status so this can\'t be done to them')
        # elif isinstance(error, commands.CheckFailure):
        #     await ctx.send('bruh')

        if isinstance(error, commands.CommandNotFound):
            await ctx.send('no such cmd')

        raise error
    
    @commands.command()
    async def test(self, msg: discord.Message):
        await msg.channel.send('Testing cog')

def setup(client):
    client.add_cog(Failures(client))
