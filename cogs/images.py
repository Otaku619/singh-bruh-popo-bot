import discord
from discord.ext import commands
# from google_images_search import GoogleImagesSearch
import random
import json
# import sys
from variables_ import *
from aiohttp import ClientSession
from PIL import Image, ImageOps
from io import BytesIO
import requests
import os

file_ = open('choice.json')
choice_ = json.load(file_)

async def get(session, url):
    async with session.get(url) as response:
        return await response.text()

async def image_fetch_api(session, _url):
            url = await get(session, _url)
            url = json.loads(url)
            return url
# gis = GoogleImagesSearch(GOOGLE_API,GOOGLE_CX)
# gis = GoogleImagesSearch('AIzaSyBeX06-SqwSm42sDRE9m8EblOi39P0wC3c','1d9bda494833b26a6')

class Animals(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['Cat', 'CAT', 'pussy', 'PUSSY', 'Pussy', 'Neko', 'neko', 'NEKO', 'nya', 'NYA', 'Nya', 'Meow', 'meow', 'MEOW'])
    async def cat(self, ctx):
        async with ClientSession() as session:
            url = await image_fetch_api(session, f'https://api.thecatapi.com/v1/images/search?api_key={CAT_API}')
            await ctx.send(embed=discord.Embed(
                title="🐈 Catto >.<", url=url[0]['url']
            ).set_image(url=url[0]['url']))

    @commands.command(aliases=['Dog', 'DOG', 'boww', 'Boww', 'BOWW', 'doggo', 'Doggo', 'DOGGO'])
    async def dog(self, ctx):
        async with ClientSession() as session:
            url = await image_fetch_api(session, 'https://api.thedogapi.com/v1/images/search?api_key={DOG_API}')
            await ctx.send(embed=discord.Embed(
                title="🐈 Doggo >.<", url=url[0]['url']
            # ).add_field(name='Name: ', value=url[0]['breeds'][0]['name']
            # ).add_field(name='Breed Group: ', value=url[0]['breeds'][0]['breed_group']
            # ).add_field(name='Lifespan: ', value=url[0]['breeds'][0]['life_span']
            ).set_image(url=url[0]['url']))
    
    @commands.command(aliases=['Birb', 'BIRB', 'bird', 'BIRD', 'Bird'])
    async def birb(self, ctx):
        async with ClientSession() as session:
            url = await image_fetch_api(session, 'https://some-random-api.ml/img/birb')
            await ctx.send(embed=discord.Embed(
                title="🐦 Birb >.<", url=url['link']
            ).set_image(url=url['link']))
    
    @commands.command(aliases=['Panda', 'PANDA', 'pandu', 'Pandu', 'PANDU'])
    async def panda(self, ctx):
        async with ClientSession() as session:
            url = await image_fetch_api(session, 'https://some-random-api.ml/img/panda')
            await ctx.send(embed=discord.Embed(
                title="🐼 Pandu >.<", url=url['link']
            ).set_image(url=url['link']))

    @commands.command(aliases=['KOALA','Koala'])
    async def koala(self, ctx):
        async with ClientSession() as session:
            url = await image_fetch_api(session, 'https://some-random-api.ml/img/koala')
            await ctx.send(embed=discord.Embed(
                title="🐨 Koala >.<", url=url['link']
            ).set_image(url=url['link']))

class Animu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Hug','HUG'])
    async def hug(self, ctx, user : discord.Member = None):
        user1, user2 = ctx.author, user
        if user == None:
            user1 = self.client.get_user(BOT_ID)
            user2 = ctx.author
        if user == ctx.author:
            await ctx.send(f"{random.choice(choice_['HUG']).format(str(ctx.author)[: -5])}")
        else:
            async with ClientSession() as session:
                url = await image_fetch_api(session, 'https://some-random-api.ml/animu/hug')
                await ctx.send(embed=discord.Embed(
                    title=f"{str(user1)[: -5]} hugged {str(user2)[: -5]} OwO", url=url['link']
                ).set_image(url=url['link']))
                if user2 == self.client.get_user(728695187731251220):
                    await ctx.send("Thanks for hugging me OwO")
    @hug.error
    async def clear_hug_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('No such user, let me hug you instead, uwu')

    @commands.command(aliases=['Wink','WINK'])
    async def wink(self, ctx, user : discord.Member = None):
        user1, user2 = ctx.author, user
        if user == None:
            user1 = self.client.get_user(BOT_ID)
            user2 = ctx.author
        if user == ctx.author:
            await ctx.send(f"{random.choice(choice_['WINK']).format(str(ctx.author)[: -5])}")
        else:
            async with ClientSession() as session:
                url = await image_fetch_api(session, 'https://some-random-api.ml/animu/wink')
                await ctx.send(embed=discord.Embed(
                    title=f"{str(user1)[: -5]} winked at {str(user2)[: -5]} OwO", url=url['link']
                ).set_image(url=url['link']))
                if user2 == self.client.get_user(728695187731251220):
                    await ctx.send("Stop winking at me, it's embarrassing!!")
    @wink.error
    async def clear_wink_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('No one to wink at ;-;')
    
    @commands.command(aliases=['Pat','PAT'])
    async def pat(self, ctx, user : discord.Member=None):
        user1, user2 = ctx.author, user
        if user == None:
            user1 = self.client.get_user(BOT_ID)
            user2 = ctx.author
        if user == ctx.author:
            await ctx.send(f"{random.choice(choice_['PAT']).format(str(ctx.author)[: -5])}")
        else:
            async with ClientSession() as session:
                url = await image_fetch_api(session, 'https://some-random-api.ml/animu/pat')
                await ctx.send(embed=discord.Embed(
                    title=f"{str(user1)[: -5]} pats {str(user2)[: -5]} OwO", url=url['link']
                ).set_image(url=url['link']))
                if user2 == self.client.get_user(728695187731251220):
                    await ctx.send("OwO thanks for the pat!")
    @pat.error
    async def clear_pat_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('User not found so i\'ll pat you instead, uwu')

class filters(commands.Cog):

    def __inti__(self, client):
        self.client = client
    
    @commands.command(aliases = ['INVERT', 'Invert'])
    async def invert(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        avatar_ = requests.get(user.avatar_url)
        img = Image.open(BytesIO(avatar_.content))
        inverted_avatar = ImageOps.invert(img)
        inverted_avatar.save(f'./filter/invert/{user.id}.png')
        await ctx.send(file=discord.File(f'./filter/invert/{user.id}.png'))
        os.remove(f'./filter/invert/{user.id}.png')
    @invert.error
    async def clear_invert_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('No such user, dummy-dum')
        

def setup(client):
    client.add_cog(Animals(client))
    client.add_cog(Animu(client))
    client.add_cog(filters(client))