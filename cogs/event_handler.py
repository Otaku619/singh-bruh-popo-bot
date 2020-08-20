import discord
from discord.ext import commands
from variables_ import *
import random
import json

file_ = open('choice.json')
choice_ = json.load(file_)

class event_handler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        _channel=self.client.get_channel(MY_SERVER_CHANNEL)
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


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        _channel=self.client.get_channel(MY_SERVER_CHANNEL)
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

    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):



def setup(client):
    client.add_cog(event_handler(client))