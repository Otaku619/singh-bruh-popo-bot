import discord
from discord.ext import commands
from saucenao_api import SauceNao
import json
import random
import requests
import urllib.parse
# from BeautifulSoup import BeautifulSoup
file_ = open('choice.json')
choice_ = json.load(file_)
a = 5


class sauce(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sauce = SauceNao()

    @commands.command(aliases=['snao', ])
    async def saucenao(self, ctx, *, url: str):
        try:
            results = self.sauce.from_url(url)
            if (len(results) < 2):
                await ctx.send("No sauce found")
                return
            best = results[0]
            embed_ = discord.Embed(
                colour=int(
                    random.choice(choice_["COLOURS"]),
                    16),
                title=f"{best.title}", url=best.urls[0]
                if len(best.urls) != 0 else None).add_field(
                name="Similarity", value=f"{best.similarity}%").set_image(
                url=best.thumbnail).add_field(name="Author",
                                              value=f"{best.author}",
                                              inline=False)
            if (best.similarity < 60):
                embed_.add_field(
                    name="No relevant image found",
                    value="This is the closest match")
            await ctx.send(embed=embed_)
        except Exception as e:
            print(e)
            await ctx.send('Invalid URL bruh')

    @saucenao.error
    async def clear_saucenao_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('You need to put an URL not your dead\
                           brain you retard')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Command: saucenao",
                                               colour=int(random.choice(
                                                   choice_['COLOURS']), 16)
                                               ).add_field(name='aliases : ',
                                                           value='snao',
                                                           inline=False
                                                           ).add_field(
                                                               name='Usage :\n',
                                                               value=';saucenao <image_url>'))

    @commands.command(aliases=[])
    async def iqdb(self, ctx, *, url: str):
        try:
            searchURL = f'https://danbooru.iqdb.org/?url={url}'

            params_ = {'format': 'json', }
            response = requests.get(searchURL, params=params_)
            response = str(response.content)
            # response.findAll
            print(response)
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(sauce(client))
