import discord
from discord.ext import commands
import random
import json
import time

file_ = open('choice.json')
choice_ = json.load(file_)
except_perms='I don\'t have one or more of the following permissions\n\
1. Read Message History\n\
2. Add reactions\n\
3. Manage Channels\
OR it might be just the internet tripping over, try to rerun a few times\
                    '
class invite_handler(commands.Cog):

    def __init__(self, client):
        self.client=client
        self.list_=[]


    @commands.command(aliases=['inv'])
    async def invite(self, ctx, time_ : int=1440, *, reason : str='No reason given'):
        try:
            time_ *= 60
            invite_ = await ctx.channel.create_invite(max_age=time_, reason=reason)
            embed_ = discord.Embed(colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='New invite created!', value=invite_)
            await ctx.send(embed=embed_)
        except:
            await ctx.send('I don\'t have the permission : Create Instant Invite')


    @invite.error
    async def clear_invite_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Command: invite", colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='aliases : ', value='inv', inline=False
            ).add_field(name='Usage :\n', value=';inv [Time(in minutes)] [Reason]', inline=False
            ).add_field(name='Note : ', value='Time defaults to 1440 (24 hours)\nReason defaults to "No reason given"'))
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send('The time should be equal to or less than 24 hours (1440 minutes)')


    @commands.command(aliases=['actinv', ])
    @commands.has_permissions(administrator=True)
    async def activeinvites(self, ctx, user : discord.Member=None):  
        try:
            if len(await ctx.guild.invites()) == 0:
                _no_active = 'No active server invite links'
                if user != None:
                    _no_active = _no_active + f' by {user}'
                await ctx.send(_no_active)
                return
            flag = 0
            if user != None:
                for inv in await ctx.guild.invites():
                    if inv.inviter == user:
                        flag = 1
                        break    
                if flag == 0:
                    await ctx.send(f'No active server invite links by {user}')
                    return
            title_ = "All active invites"
            if user == None:
                title_ = title_ + f" : {len(await ctx.guild.invites())}"
            else:
                title_ = title_+ f" by {user}"
            ind_ = 1
            embed_ = discord.Embed(title=title_, colour=int(random.choice(choice_['COLOURS']), 16))
            for  invite_ in await ctx.guild.invites():
                inviter_ = 'BOT' if invite_.inviter.bot else invite_.inviter
                if user != None:
                    if invite_.inviter != user:
                        continue
                embed_.add_field(name=f'{ind_}. By {inviter_}', value=f'in {invite_.channel}\nat {str(invite_.created_at)[: -10]} used for {invite_.uses} times', inline=False)
                ind_ += 1
            await ctx.send(embed=embed_)
        except Exception:
            await ctx.send('I don\'t have one or more of the following permissions\n\
1. Read Message History\n\
2. Manage Channels\n\
OR it might be just the internet tripping over, try to rerun a few times\
                    ')
    @activeinvites.error
    async def clear_activeinvites_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator')


    @commands.command(aliases = ['delallinv','delallinvites', ])
    @commands.has_permissions(administrator=True)
    async def deleteallinvites(self, ctx):
        try:
            if len(await ctx.guild.invites()) == 0:
                await ctx.send('No active server invite links')
                return
            confirm_ = await ctx.send('Are you sure you want to revoke all active server invites?', delete_after=20)
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
    

    @commands.command(aliases=['delinv', 'delinvites', ])
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
            confirm_ = await ctx.send(f'Are you sure you want to revoke all active server invites by {user}?', delete_after=20)
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


    @commands.command(aliases=['delinvin', 'delinvitesin', ])
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
            confirm_ = await ctx.send(f'Are you sure you want to revoke all active server invites in {channel_}?', delete_after=20)
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


    @commands.command(aliases=['delinvbyin', 'delinvitsebyin', ])
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
            confirm_ = await ctx.send('Are you sure you want to revoke all active server invites by {user} in {channel_}?', delete_after=20)
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
            await ctx.send(embed=discord.Embed(title="Command: deleteinvitesbyin", colour=int(random.choice(choice_['COLOURS']), 16)
            ).add_field(name='aliases : ', value='delinvinby, delinvitesbyin', inline=False
            ).add_field(name='Usage :\n', value=';deleteinvitesinby <user_mention> #<text_channel_name>', inline=False
            ))
        elif isinstance(error, commands.BadArgument):
            await ctx.send('No such user/channel, dummy-dum\nUsage is ;deleteinvitesinby <user_mention> #<text_channel_name>')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry bruh, but you dont have the perms : Administrator') 


    async def add_reac(self, msg: discord.Message):
        await msg.add_reaction('\u2705')
        await msg.add_reaction('\u274C')


    async def del_0(self, msg):
        if len(await msg.guild.invites()) == 0:
            await msg.channel.send('No active server invite links')
            return
        for invite_ in await msg.guild.invites():
            await invite_.delete()
        await msg.channel.send('All server invites deleted successfully!')

        
    async def del_1(self, msg, user):
        flag = 0
        for i in await msg.guild.invites():
            if i.inviter == user:
                flag = 1
                break
        if flag == 0:
            await msg.channel.send(f'No active server invite links by {str(user)[: -5]}')
            return
        for i in await msg.guild.invites():
            if i.inviter == user:
                await i.delete()
        await msg.channel.send(f'All server invites by {user} deleted successfully!')


    async def del_2(self, msg, channel_):
        flag = 0
        for i in await msg.guild.invites():
            if i.channel == channel_:
                flag = 1
                break
        if flag == 0:
            await msg.channel.send(f'No active server invite links in {channel_}')
            return
        for i in await msg.guild.invites():
            if i.channel == channel_:
                await i.delete()
        await msg.channel.send(f'All server invites in {channel_} deleted successfully!')


    async def del_3(self, msg, channel_, user):
        flag = 0
        for i in await msg.guild.invites():
            if i.inviter == user and i.channel == channel_:
                flag = 1
                break
        if flag == 0:
            await msg.channel.send(f'No active server invite links by {str(user)[: -5]} in {channel_}')
            return
        for i in await msg.guild.invites():
            if i.channel == channel_ and i.inviter == user:
                await i.delete()
        await msg.channel.send(f'All server invites by {user} in {channel_} deleted successfully!')


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction) == '\u2705' or str(reaction) == '\u274C':
            for ind in range(0, len(self.list_)):
                if self.list_[ind]['msg'].id == reaction.message.id:
                    break
            if user.id == self.list_[ind]['auth'].id and str(reaction) == '\u2705' and self.list_[ind]['msg'].id == reaction.message.id:
                id_ = self.list_[ind]['del_id']
                await self.list_[ind]['msg'].delete()
                if id_ == 0 :
                    await self.del_0(self.list_[ind]['msg'])
                    del self.list_[ind]
                elif id_ == 1:
                    await self.del_1(self.list_[ind]['msg'], self.list_[ind]['user'])
                    del self.list_[ind]
                elif id_ == 2:
                    await self.del_2(self.list_[ind]['msg'], self.list_[ind]['channel'])
                    del self.list_[ind]
                else:
                    await self.del_3(self.list_[ind]['msg'], self.list_[ind]['channel'], self.list_[ind]['user'])
                    del self.list_[ind]

            elif user.id == self.list_[ind]['auth'].id and str(reaction) == '\u274C' and self.list_[ind]['msg'].id == reaction.message.id:
                await self.list_[ind]['msg'].delete()
                await self.list_[ind]['msg'].channel.send(f'Action cancelled by {str(self.list_[ind]["auth"])[: -5]}')
            else:
                pass

def setup(client):
    client.add_cog(invite_handler(client))