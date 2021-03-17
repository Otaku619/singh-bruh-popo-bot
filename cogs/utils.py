import discord
from discord.ext import commands
import random
import json
from youtube_search import YoutubeSearch
import os
import urllib


file_ = open('choice.json')
choice_ = json.load(file_)


class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, user=None):
        if user is None:
            user = ctx.author
        elif user[:1] == "<":
            user = await self.client.fetch_user(int(user[3:-1:]))
        else:
            try:
                user = await self.client.fetch_user(int(user))
            except:
                await ctx.send('User not found')
                return
        await ctx.send(embed=discord.Embed(
            title=f"{str(user)[: -5]}'s avatar")
            .set_image(url=user.avatar_url)
        )

    @avatar.error
    async def clear_avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('At least mention someone nigga')

    @commands.command(aliases=['clear', 'delete'])
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
                   member: discord.Member,
                   *, reason: str = 'No reason bruh'
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
                  member: discord.Member,
                  *, reason: str = 'No reason bruh'
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
            await ctx.send(str(ctx.guild.members))

    @commands.command(aliases=["search", "yts"])
    async def ytsearch(self, ctx, *, term: str):
        sresults = YoutubeSearch(term, max_results=12).to_dict()
        await ctx.send(f"https://www.youtube.com/watch?v={random.choice(list(sresults))['id']}")

    @commands.command(aliases=["accusearch", "ayts"])
    async def accurateytsearch(self, ctx, *, term: str):
        sresults = YoutubeSearch(term, max_results=1).to_dict()
        await ctx.send(f"https://www.youtube.com/watch?v={list(sresults)[0]['id']}")

    @commands.command(aliases=["bigtext"])
    async def figlet(self, ctx, *, stuff: str):
        fig = os.popen(f'figlet \"{stuff}\"').read()
        await ctx.send(f"```\n{fig}\n```")

    @commands.command(aliases=["comp", "reduce"])
    async def compress(self, ctx, *, url: str):
        try:
            url_ = url.split()
            size = url_[-1]
            url = ctx.message.attachments[0].url if len(
                ctx.message.attachments) > 0 else url_[0]
            if(int(size) > 8*1024):
                await ctx.send("Please enter a number less than or equal to 8MBs, I don't have nitro ;-;")
                return
            msg1 = await ctx.send("Downloading the video")
            os.system(f"wget -O./imgs/Compressor/{ctx.message.id}.mp4 {url}")
            await msg1.delete()
            msg2 = await ctx.send("Compressing the video")
            os.system(
                f"./compress.sh \"./imgs/Compressor/{ctx.message.id}.mp4\" {size} \"./imgs/Compressor/Compressed{ctx.message.id}.mp4\"")
            siz = os.popen(
                f"stat -c %s \"./imgs/Compressor/Compressed{ctx.message.id}.mp4\"")
            if(int(siz.read()) > 8*1024*1024):
                await msg2.delete()
                await ctx.send("Compressed file is above 8Mb can't send cuz no nitro")
                await ctx.send(":pensive:")
            else:
                await ctx.send(file=discord.File(f"./imgs/Compressor/Compressed{ctx.message.id}.mp4"))
                await msg2.delete()
            os.system(
                f"rm ./imgs/Compressor/{ctx.message.id}.mp4 && rm ./imgs/Compressor/Compressed{ctx.message.id}")
        except Exception as e:
            print(e)
            await ctx.send("some problem occured, please run ;compress for valid syntax and don't enter a size too low")

    @compress.error
    async def clear_compress(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('You sure you using the correct syntax?')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: compress", colour=int(random.choice(choice_['COLOURS']), 16)
                                               ).add_field(name='aliases : ', value='comp, reduce', inline=False
                                                           ).add_field(name='Usage :\n', value=';compress <video_url> <size_of_the_compressed_video(in Kilobyes)>', inline=False
                                                                       ))


def setup(client):
    client.add_cog(utils(client))
