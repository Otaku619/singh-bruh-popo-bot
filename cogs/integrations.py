import discord
import os
from discord.ext import commands
from aiohttp import ClientSession
import json
import urllib
import pafy
import random
file_ = open('choice.json')
choice_ = json.load(file_)


class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class url_to_vid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.requests = []

    async def fetch_api(self, session, url):
        async with session.get(url) as response:
            return json.loads(await response.text())

    @commands.command(aliases=['instagram', ])
    async def ig(self, ctx, url):
        try:
            url = url.split('?')
            url = url[0]
            url = url + '?__a=1'
            async with ClientSession() as session:
                url_json = await self.fetch_api(session, url)
                await ctx.send(url_json['graphql']['shortcode_media']['video_url'])
        except Exception as e:
            if str(e).startswith('Expecting value'):
                await ctx.send('Not a valid instagram URL')
            elif str(e) == "'video_url'" or str(e) == "graphql":
                await ctx.send('Invalid instagram link')
            else:
                await ctx.send('Sorry a problem occured')

    @ig.error
    async def clear_ig_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: ig", colour=int(random.choice(choice_['COLOURS']), 16)
                                               ).add_field(name='aliases : ', value='instagram', inline=False
                                                           ).add_field(name='Usage :\n', value=';instagram <instagram_url>', inline=False))

    @commands.command(aliases=['youtube, '])
    async def yt(self, ctx, url):
        try:
            yt_vid = pafy.new(url)
            msg_ = await ctx.send('Getting the video for you')
            yt_streams = yt_vid.streams[::-1]
            for yt_stream in yt_streams:
                if yt_stream.get_filesize() <= (8 * 1024 * 1024):
                    break
            else:
                await ctx.send('The video size is larger than your IQ and we talkin\' in megabytes')
                return
            yt_stream.download(
                filepath=f'./imgs/youtube/{ctx.message.id}.mp4')
            await ctx.send(file=discord.File(f'./imgs/youtube/{ctx.message.id}.mp4'))
            await msg_.delete()
            os.system(f'rm ./imgs/youtube/{ctx.message.id}.mp4')
        except Exception as e:
            print(e)
            if str(e).startswith(
                    "Need 11 character video id or the URL of the video"):
                await ctx.send('Not a valid youtube URL')
            else:
                await ctx.send('Sorry a problem occured')

    @yt.error
    async def clear_yt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: yt", colour=int(random.choice(choice_['COLOURS']), 16)
                                               ).add_field(name='aliases : ', value='youtube', inline=False
                                                           ).add_field(name='Usage :\n', value=';yt <youtube_url>', inline=False))

    @commands.command(aliases=['reddit, '])
    async def rd(self, ctx, url):
        try:
            url = f"https://api.reddit.com/api/info/?id=t3_{url.split('/')[-3]}"
            async with ClientSession() as session:
                url_json = await self.fetch_api(session, url)
                for f in url_json['data']['children']:
                    await ctx.send(f['data']['media']['reddit_video']['fallback_url'] if f['data']['is_video'] else f['data']['url'])
        except Exception as e:
            if str(e).startswith('Expecting value'):
                await ctx.send('Not a valid reddit URL')
            else:
                await ctx.send('Sorry a problem occured')

    @rd.error
    async def clear_rd_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: rd", colour=int(random.choice(choice_['COLOURS']), 16)
                                               ).add_field(name='aliases : ', value='reddit', inline=False
                                                           ).add_field(name='Usage :\n', value=';rd <reddit_post_url>', inline=False))


def setup(client):
    client.add_cog(url_to_vid(client))
