import discord
from discord.ext import commands

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ['AV', 'Av', 'Avatar', 'av', 'AVATAR'])
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

def setup(client):
    client.add_cog(utils(client))