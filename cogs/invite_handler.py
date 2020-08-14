import discord
from discord.ext import commands
import random
import json

file_ = open('choice.json')
choice_ = json.load(file_)
except_perms='I don\'t have the following permission(s)\n\
                        1. Read Message History\n\
                        2. Add reactions\n\
                        3. Manage Channels\
                    '
class invite_handler(commands.Cog):

    def __init__(self, client):
        self.client=client
        self.list_=[]

    @commands.command(aliases=['INVITE', 'Invite', 'inv', 'INV', 'Inv'])
    async def invite(self, ctx, time_ : int=24):
        try:
            time_ *= 60
            invite_ = await ctx.channel.create_invite(max_age=time_)
            embed_ = discord.Embed(colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='New invite created!', value=invite_)
            await ctx.send(embed=embed_)
        except:
            await ctx.send('I don\'t have the permission : Create Instant Invite')
    @invite.error
    async def clear_invite_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('The time for the invite must be in integers (minutes)')
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send('The time should be equal to or less than 24 hours (1440 minutes)')

    @commands.command(aliases=['DELALLINVITES', 'Delallinvites', 'Delallinv', 'delallinv', 'DELALLINV', 'delallinvits', 'DELETEALLINVITES', 'Deleteallinvites'])
    @commands.has_permissions(administrator=True)
    async def deleteallinvites(self, ctx):
        try:
            if len(await ctx.guild.invites()) == 0:
                await ctx.send('No active server invite links')
                return
            confirm_ = await ctx.send('Are you sure you want to revoke all active server invites?', delete_after=15)
            self.list_.append({
                        "msg" : confirm_,
                        "auth" : ctx.author,
                        "del_id" : 0,
                        "user" : None,
                        "channel" : None
                    })
            await self.add_reac(confirm_)
        except:
            await ctx.send(except_perms)
    @deleteallinvites.error
    async def clear_deleteallinvites_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator') 

    @commands.command(aliases=['DELINVITES', 'Delinvites', 'Delinv', 'delinv', 'DELINV', 'delinvites', 'DELETEINVITES', 'Deleteinvites'])
    @commands.has_permissions(administrator=True)
    async def deleteinvites(self, ctx, user : discord.Member=None):
        try:
            if user == None:
                user = ctx.author
            flag = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    flag = 1
                    break
            if flag == 0:
                await ctx.send(f'No active server invite links by {str(user)[: -5]}')
                return
            confirm_ = await ctx.send(f'Are you sure you want to revoke all active server invites by {user}?', delete_after=15)
            self.list_.append({
                        "msg" : confirm_,
                        "auth" : ctx.author,
                        "del_id" : 1,
                        "user" : user,
                        "channel" : None
                    })
            await self.add_reac(confirm_)
        except:
            await ctx.send(except_perms)
    @deleteinvites.error
    async def clear_deleteinvitesz_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('No such user, dummy-dum')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator') 

    @commands.command(aliases=['DELINVITESIN', 'Delinvitesin', 'Delinvin', 'delinvin', 'DELINVIN', 'delinvitesin', 'DELETEINVITESIN', 'Deleteinvitesin'])
    @commands.has_permissions(administrator=True)
    async def deleteinvitesin(self, ctx, channel_ : discord.TextChannel=None):
        try:
            if channel_ == None:
                channel_ = ctx.channel
            flag = 0
            for i in await ctx.guild.invites():
                if i.channel == channel_:
                    flag = 1
                    break
            if flag == 0:
                await ctx.send(f'No active server invite links in {channel_}')
                return
            confirm_ = await ctx.send(f'Are you sure you want to revoke all active server invites in {channel_}?', delete_after=15)
            self.list_.append({
                        "msg" : confirm_,
                        "auth" : ctx.author,
                        "del_id" : 2,
                        "channel" : channel_,
                        "user" : None
                    })
            await self.add_reac(confirm_)
        except:
            await ctx.send(except_perms)
    @deleteinvitesin.error
    async def clear_deleteinvitesin_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('No such channel, dummy-dum')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator') 

    @commands.command(aliases=['DELINVITESBYIN', 'Delinvitesbyin', 'Delinvbyin', 'delinvbyin', 'DELINVBYIN','delinvitsebyin', 'DELETEINVITESBYIN', 'Deleteinvitesbyin'])
    async def deleteinvitesbyin(self, ctx, user : discord.Member, *, channel_ : discord.TextChannel):
        try:
            flag = 0
            for i in await ctx.guild.invites():
                if i.inviter == user and i.channel == channel_:
                    flag = 1
                    break
            if flag == 0:
                await ctx.send(f'No active server invite links by {str(user)[: -5]} in {channel_}')
                return
            confirm_ = await ctx.send('Are you sure you want to revoke all active server invites by {user} in {channel_}?', delete_after=15)
            self.list_.append({
                        "msg" : confirm_,
                        "auth" : ctx.author,
                        "del_id" : 3,
                        "channel" : channel_,
                        "user" : user
                    })
            await self.add_reac(confirm_)
        except:
            await ctx.send(except_perms)
    @deleteinvitesbyin.error
    async def clear_deleteinvitesbyin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Wrong command format:\n;deleteinvitesbyin @<user> #<text_channel>')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('No such user/channel, dummy-dum\n;deleteinvitesbyin @<user> #<text_channel>')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator') 

    async def add_reac(self, msg: discord.Message):
        await msg.add_reaction('\u2705')
        await msg.add_reaction('\u274C')

    async def del_0(self, msg):
        for invite_ in await msg.guild.invites():
            await invite_.delete()
        await msg.channel.send('All server invites deleted successfully!')
        
    async def del_1(self, msg, user):
        for i in await msg.guild.invites():
            if i.inviter == user:
                await i.delete()
        await msg.channel.send(f'All server invites by {user} deleted successfully!')

    async def del_2(self, msg, channel_):
        for i in await msg.guild.invites():
            if i.channel == channel_:
                await i.delete()
        await msg.channel.send(f'All server invites in {channel_} deleted successfully!')

    async def del_3(self, msg, channel_, user):
        for i in await msg.guild.invites():
            if i.channel == channel_ and i.inviter == user:
                await i.delete()
        await msg.channel.send(f'All server invites by {user} in {channel_} deleted successfully!')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        for ind in range(0, len(self.list_)):
            if self.list_[ind]['msg'].id == reaction.message.id:
                break
        if user.id == self.list_[ind]['auth'].id and str(reaction) == '\u2705':
            id_ = self.list_[ind]['del_id']
            await self.list_[ind]['msg'].delete()
            if id_ == 0 :
                await self.del_0(self.list_[ind]['msg'])
            elif id_ == 1:
                await self.del_1(self.list_[ind]['msg'], self.list_[ind]['user'])
            elif id_ == 2:
                await self.del_2(self.list_[ind]['msg'], self.list_[ind]['channel'])
            else:
                await self.del_3(self.list_[ind]['msg'], self.list_[ind]['channel'], self.list_[ind]['user'])
        
        elif user.id == self.list_[ind]['auth'].id and str(reaction) == '\u274C':
            await self.list_[ind]['msg'].delete()
            await self.list_[ind]['msg'].channel.send(f'Action cancelled by {str(self.list_[ind]["auth"])[: -5]}')
        else:
            pass


def setup(client):
    client.add_cog(invite_handler(client))