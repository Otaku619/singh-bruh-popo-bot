import discord
from discord.ext import commands
from saucenao_api import SauceNao
import json
import random
import requests
import urllib.parse
from bs4 import BeautifulSoup
file_ = open('choice.json')
choice_ = json.load(file_)
a = 5


class sauce(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sauce = SauceNao()

    def fix_extension(self, url):
        url = url.split('.')
        return ('.').join(url[0:-1])+'.png?'+url[-1].split('?')[-1]

    @commands.command(aliases=['snao', ])
    async def saucenao(self, ctx, *, url: str = ''):
        try:
            url_ = ctx.message.attachments[0].url if len(
                ctx.message.attachments) > 0 else url
            if url_.strip() == '':
                await ctx.send(embed=discord.Embed(title="Command: saucenao",
                                                   colour=int(random.choice(
                                                       choice_['COLOURS']), 16)
                                                   ).add_field(name='aliases : ',
                                                               value='snao',
                                                               inline=False
                                                               ).add_field(
                    name='Usage :\n',
                    value=';saucenao <image_url>'))
                return
            url_ = self.fix_extension(url_)
            results = self.sauce.from_url(url_)
            if len(results) < 2:
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

    @commands.command(aliases=[])
    async def iqdb(self, ctx, *, url: str = ''):
        try:
            url_ = ctx.message.attachments[0].url if len(
                ctx.message.attachments) > 0 else url
            if url_.strip() == '':
                await ctx.send(embed=discord.Embed(title="Command: iqdb",
                                                   colour=int(random.choice(
                                                       choice_['COLOURS']), 16)
                                                   ).add_field(name='aliases : ',
                                                               value='None',
                                                               inline=False
                                                               ).add_field(
                    name='Usage :\n',
                    value=';iqdb <image_url>'))
                return
            url_ = self.fix_extension(url_)
            searchURL = f'https://iqdb.org/?url={url_}'
            soup = BeautifulSoup(requests.get(searchURL).text, 'lxml')
            sauce = soup.find('div', class_='pages')
            nomatch = sauce.find('div', class_='nomatch') is None
            sauce = sauce.find_all('div')[1 if nomatch else 2].find(
                'table').find_all('tr')
            embed_ = discord.Embed(
                colour=int(random.choice(choice_['COLOURS']),
                           16),
                title='Best Match' if nomatch else 'No good match found :(',
                url=('https:' if sauce[1].td.a.get('href')[0] != 'h' else '') +
                sauce[1].td.a.get("href")).set_image(
                url=('https://www.iqdb.org'
                     if sauce[1].td.a.img.get('src')[0] != 'h' else '') +
                sauce[1].td.a.img.get("src")).add_field(
                name='Similarity: ', value=sauce[4].td.text.split(' ')[0],
                inline=False).add_field(
                name='Want more results?',
                value=f'[Click here for all search results]({searchURL})',
                inline=0)
            await ctx.send(embed=embed_)
        except Exception as e:
            print(e)
            await ctx.send("Invalid URL or couldn't find")

    @ iqdb.error
    async def clear_iqdb_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('You need to put an URL not your dead\
                           brain you retard')


def setup(client):
    client.add_cog(sauce(client))
