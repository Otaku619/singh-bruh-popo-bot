import discord
from discord.ext import commands
import random
import json

file_ = open('choice.json')
choice_ = json.load(file_)

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ['av'])
    async def avatar(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        await ctx.send(embed=discord.Embed(
            title=f"{str(user)[: -5]}'s avatar")
            .set_image(url=user.avatar_url)
            )

    @avatar.error
    async def clear_avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('User not found!')

    @commands.command(aliases=['clear', 'delete' ])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount+1)
        except:
            await ctx.send('Encountered some kind of stupid problem, sorry for that :(')
    @purge.error
    async def clear_purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You lack the permission to manage messages')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('You sure you using the correct syntax?')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: Purge", colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='aliases : ', value='clear, delete', inline=False
            ).add_field(name='Usage :\n', value=';purge <Number of messages to purge>'))
        

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx,
                member:discord.Member,
                *, reason : str='No reason bruh'
            ):
            try:
                await member.kick(reason=reason)
            except discord.Forbidden:
                await ctx.send('Sorry, I can\'t kick that person')
    @kick.error
    async def clear_kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You lack the permission to kick members')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('You sure you using the correct syntax?')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: Kick", colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='aliases : ', value='None', inline=False
            ).add_field(name='Usage :\n', value=';kick <User to kick> [Reason]', inline=False
            ).add_field(name='Note : ', value='Reason defaults to "No reason bruh"'))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, 
                member:discord.Member, 
                *, reason : str='No reason bruh'
            ):
            try:
                await member.ban(reason=reason)
            except discord.Forbidden:
                await ctx.send('Sorry, I can\'t ban that person')
    @ban.error
    async def clear_ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You lack the permission to ban mesmbers')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('You sure you using the correct syntax?')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: Ban", colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='aliases : ', value='None', inline=False
            ).add_field(name='Usage :\n', value=';ban <User to ban> [Reason]', inline=False
            ).add_field(name='Note : ', value='Reason defaults to "No reason bruh"'))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency*1000)}ms ping hai behen ke ghode')

    @commands.command()
    async def echo(self, ctx, *, msg):
        # if not (str(msg).startswith(';') or ctx.bot):
            await ctx.send(msg)
        # else:
            # await ctx.send('Why would you run my own commands by echoing me, wanna break me, eh?')
        
    @commands.command()
    async def members(self, ctx):
        print(ctx.guild.members)
        if(len(str(ctx.guild.members))) >= 2000:
            await ctx.send('The list is over 2000 characters\nCheck your terminal for the output')
        else:
            await  ctx.send(str(ctx.guild.members))


def setup(client):
    client.add_cog(utils(client))