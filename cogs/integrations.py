import discord
import os
from discord.ext import commands
from aiohttp import ClientSession
import json
import urllib
import pafy

class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)

class url_to_vid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.requests=[]

    async def fetch_api(self, session, url):
        async with session.get(url) as response:
            return json.loads(await response.text())
 
    @commands.command(aliases=['instagram', ])
    async def ig(self, ctx,* , url):
        try:
            url = url.split('?')
            url = url[0]
            url = url + '?__a=1'
            async with ClientSession() as session:
                url_json = await self.fetch_api(session, url)
                msg_  = await ctx.send('Getting the video for you')              
                urllib.request.urlretrieve(url_json['graphql']['shortcode_media']['video_url'], f'./imgs/instagram/IssuedBy{ctx.author}id={ctx.message.id}.mp4')
                try:
                    await ctx.send(file=discord.File(f'./imgs/instagram/IssuedBy{ctx.author}id={ctx.message.id}.mp4'))
                except:
                    await ctx.send('The video size is larger than your IQ and we talkin\' in megabytes')
                await msg_.delete()
                os.remove(f'./imgs/instagram/IssuedBy{ctx.author}id={ctx.message.id}.mp4')
        except Exception as e:
            if str(e).startswith('Expecting value'):
                await ctx.send('Not a valid instagram URL')
            elif str(e) == "'video_url'" or str(e) == "graphql":
                await ctx.send('Invalid instagram link')
            else:
                await ctx.send('Sorry a problem occured')

    @commands.command(aliases=['youtube, '])
    async def yt(self, ctx, *, url):
        try:
            yt_vid = pafy.new(url)
            msg_  = await ctx.send('Getting the video for you')
            yt_stream = yt_vid.getbest(preftype='mp4')
            if yt_stream.get_filesize() > (8 * 1024 * 1024):
                await ctx.send('The video size is larger than your IQ and we talkin\' in megabytes')
                return
            yt_stream.download(filepath=f'./imgs/youtube/IssuedBy{ctx.author}id={ctx.message.id}.mp4')
            await ctx.send(file=discord.File(f'./imgs/youtube/IssuedBy{ctx.author}id={ctx.message.id}.mp4'))
            await msg_.delete()
            os.remove(f'./imgs/youtube/IssuedBy{ctx.author}id={ctx.message.id}.mp4')
        except Exception as e:
            print(e)
            if str(e).startswith("Need 11 character video id or the URL of the video"):
                await ctx.send('Not a valid youtube URL')
            else:
                await ctx.send('Sorry a problem occured')



def setup(client):
    client.add_cog(url_to_vid(client))