import discord
from discord.ext import commands
import os
import json
import random
import time

def load_bank_data():
    _file_ = open("./cogs/bank.json")
    return json.load(_file_)

def load_time_data():
    _file_=open("./cogs/time.json")
    return json.load(_file_)

def save_data(bank_data, time_data):
    with open("./cogs/bank.json","w") as _file_:
        json.dump(bank_data,_file_)
    with open("./cogs/time.json","w") as _file_:
        json.dump(time_data,_file_)
    
file_ = open('choice.json')
choice_ = json.load(file_)

class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    def chunks(self, list_, n):
        for i in range(0, len(list_), n):
            yield list_[i:i+n]

    @commands.command()
    async def bal(self, ctx, user : discord.Member=None):
        try:
            if user == None:
                user = ctx.author
            bank_data = load_bank_data()
            time_data=load_time_data()
            id = str(user.id)
            if id not in bank_data:
                if id != str(ctx.author.id):
                    await ctx.send(f"{user} does not have an account yet")

                else:
                    bank_data[id] = {
                            "wallet": 0,
                            "bank": 0,
                            "debt": 0
                            }
                    time_data[id]={}
                    await ctx.send('Account Created Successfully!')
            else: 
                embed = discord.Embed(title=f"{str(user)[:-5]}'s balance", colour=int(random.choice(choice_["COLOURS"]), 16))
                embed.add_field(
                            name="Wallet",
                            value=bank_data[id]["wallet"],
                            inline=True
                        )
                embed.add_field(name="Bank",
                            value=bank_data[id]["bank"],
                            inline=True
                        )
                embed.add_field(name="Debt",
                            value=bank_data[id]["debt"],
                            inline=True
                        )
                await ctx.send(embed=embed)
            save_data(bank_data,time_data)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')          
    
    @commands.command()
    async def free(self, ctx):
        bank_data = load_bank_data()
        time_data = load_time_data() 
        id = str(ctx.author.id)
        if id not in bank_data:
            await ctx.send('Please open an account first by typing ;bal')
        else:
            if "free" not in time_data[id]:
                time_data[id]["free"] = 0
            if round(time.time()) >= time_data[id]['free'] + 60:
                time_data[id]['free'] = round(time.time())
                free = random.randint(0,100)
                free_money = random.randint(0,len(choice_["FREE"])-1)
                if free_money == 2:
                    await ctx.send(choice_["FREE"][free_money].format(str(ctx.author)[:-5],free))
                else:
                    await ctx.send(choice_["FREE"][free_money].format(str(ctx.author)[:-5],free))
                    bank_data[id]["wallet"] += free
            else:
                embed = discord.Embed(colour=int(random.choice(choice_["COLOURS"]), 16))
                embed.add_field(name='Thand Rakh',
                        value=f"You need to wait {await self.time_format(time_data[id]['free']+60-round(time.time()))} more to get the free stuff",
                        inline=False
                    )
                await ctx.send(embed=embed)
        save_data(bank_data,time_data)
    
    @commands.command(aliases=['dep', ])
    async def deposit(self, ctx, *, amount):
        try:
            bank_data = load_bank_data()
            time_data = load_time_data() 
            id = str(ctx.author.id)
            if id not in bank_data:
                await ctx.send('Please open an account first by typing ;bal')
            else:
                if "dep" not in time_data[id]:
                    time_data[id]["dep"] = 0
                if round(time.time()) >= time_data[id]['dep'] + 20:
                    if amount.lower() == "all" or amount.lower() == "max":
                        amount = f"{bank_data[id]['wallet']}"
                    if int(amount) == 0:
                        await ctx.send("C'mon, how broke can one be?")
                    elif int(amount) > bank_data[id]["wallet"]:
                        await ctx.send(f'You retarded or what? You only have {bank_data[id]["wallet"]} in your wallet')
                    else:
                        bank_data[id]["wallet"] -= int(amount)
                        bank_data[id]["bank"] += int(amount)
                        await ctx.send(f'Transfer successful! Now you have {bank_data[id]["bank"]} in your bank account!')
                        time_data[id]['dep'] = round(time.time())
                else:
                    embed = discord.Embed(colour=int(random.choice(choice_["COLOURS"]), 16))
                    embed.add_field(name='Thand Rakh',
                            value=f"You need to wait {await self.time_format(time_data[id]['dep']+20-round(time.time()))} more to deposit your sh*t",
                            inline=False
                        )
                    await ctx.send(embed=embed)
            save_data(bank_data,time_data)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')          
    @deposit.error
    async def clear_deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(random.choice([
                    "I thought I was supposed to deposit something",
                    "Bruh, sorry, I didn't know you were so broke :hand_splayed: :pensive: :broken_heart: :point_left:"
                ]))
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(random.choice([
                "At least give me a proper number for Christ's sake",
                "I'm supposed to store that?!"
            ]))

    @commands.command(aliases=['with', ])
    async def withdraw(self, ctx, *, amount):
        try:
            bank_data = load_bank_data()
            time_data = load_time_data() 
            id = str(ctx.author.id)
            if id not in bank_data:
                await ctx.send('Please open an account first by typing ;bal')
            else:
                if "with" not in time_data[id]:
                    time_data[id]["with"] = 0
                if round(time.time()) >= time_data[id]['with'] + 20:
                    if amount.lower() == "all" or amount.lower() == "max":
                        amount = f"{bank_data[id]['bank']}"
                    if int(amount) == 0:
                        await ctx.send("C'mon, how broke can one be?")
                    elif int(amount) > bank_data[id]["bank"]:
                        await ctx.send(f'Bruh wut? You only have {bank_data[id]["bank"]} in your bank')
                    else:
                        bank_data[id]["bank"] -= int(amount)
                        bank_data[id]["wallet"] += int(amount)
                        await ctx.send(f'Transfer successful! Now you have {bank_data[id]["wallet"]} in your wallet!\nWhat did you need it for though? :thinking:')
                        time_data[id]['with'] = round(time.time())
                else:
                    embed = discord.Embed(colour=int(random.choice(choice_["COLOURS"]), 16))
                    embed.add_field(name='Thand Rakh',
                            value=f"You need to wait {await self.time_format(time_data[id]['with']+20-round(time.time()))} more to withdraw your sh*tty funds",
                            inline=False
                        )
                    await ctx.send(embed=embed)
            save_data(bank_data,time_data)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')          
    @withdraw.error
    async def clear_withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(random.choice([
                    "I thought I was supposed to withdraw something",
                    "Bruh, sorry, I didn't know you were so broke :hand_splayed: :pensive: :broken_heart: :point_left:"
                ]))
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(random.choice([
                "At least give me a proper number for Christ's sake",
                "I'm supposed to withdraw that?! I highly doubt you even have that"
            ]))

    @commands.command()
    async def daily(self, ctx):
        try:
            bank_data = load_bank_data()
            time_data = load_time_data()
            id = str(ctx.author.id)
            if id not in bank_data:
                await ctx.send('Please open an account first by typing ;bal')
            else:
                if 'daily' not in time_data[id]:
                    time_data[id]['daily'] = 0
                if round(time.time()) >= time_data[id]['daily'] + 86400:
                        await ctx.send(f'Wow! You got 500 daily coins, and now they go to your wallet')
                        bank_data[id]['wallet'] += 500
                        time_data[id]['daily'] = round(time.time())
                else:
                    embed = discord.Embed(colour=int(random.choice(choice_["COLOURS"]), 16))
                    embed.add_field(name='Thand Rakh',
                            value=f"You need to wait {await self.time_format(time_data[id]['daily']+86400-round(time.time()))} more to get your daily cash",
                            inline=False
                        )
                    await ctx.send(embed=embed)
            save_data(bank_data,time_data)     
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}') 

    @commands.command()
    async def weekly(self, ctx):
        try:
            bank_data = load_bank_data()
            time_data = load_time_data()
            id = str(ctx.author.id)
            if id not in bank_data:
                await ctx.send('Please open an account first by typing ;bal')
            else:
                if 'weekly' not in time_data[id]:
                    time_data[id]['weekly'] = 0
                if round(time.time()) >= time_data[id]['weekly'] + 604800:
                        await ctx.send(f'Wow! You got 5000 weekly coins, and now they go to your wallet, make sure to transfer them to your bank, just to be on the safe side')
                        bank_data[id]['wallet'] += 5000
                        time_data[id]['weekly'] = round(time.time())
                else:
                    embed = discord.Embed(colour=int(random.choice(choice_["COLOURS"]), 16))
                    embed.add_field(name='Thand Rakh',
                            value=f"You need to wait {await self.time_format(time_data[id]['weekly']+604800-round(time.time()))} more to get your weekly cash",
                            inline=False
                        )
                    await ctx.send(embed=embed)
            save_data(bank_data,time_data)     
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')

    @commands.command()
    async def top(self, ctx):
        try:
            top_data = {}
            bank_data = load_bank_data()
            embed_ = discord.Embed(title=f'Richest wallets in {ctx.guild.name}',
                    colour=int(random.choice(choice_["COLOURS"]), 16))
            for member_ in ctx.guild.members:
                if str(member_.id) in bank_data:
                    top_data[f'{member_}'] = bank_data[f'{member_.id}']['wallet']
            sorted_top_data = sorted(top_data.items(),
            key=lambda x : (x[1], x[0]), reverse=True)
            for i in list(self.chunks(sorted_top_data, 5)):
                print(i)
            for i in range(5 if len(sorted_top_data)>5 else len(sorted_top_data)):
                embed_.add_field(name=f'#{i+1} {sorted_top_data[i][0]}',
                value=f'{sorted_top_data[i][1]}', inline=False)
            await ctx.send(embed=embed_)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')

    @commands.command()
    async def topbank(self, ctx):
        try:
            top_data = {}
            bank_data = load_bank_data()
            embed_ = discord.Embed(title=f'Richest banks in {ctx.guild.name}',
                    colour=int(random.choice(choice_["COLOURS"]), 16))
            for member_ in ctx.guild.members:
                if str(member_.id) in bank_data:
                    top_data[f'{member_}'] = bank_data[f'{member_.id}']['bank']
            sorted_top_data = sorted(top_data.items(),
            key=lambda x : (x[1], x[0]), reverse=True)
            for i in range(5 if len(sorted_top_data)>5 else len(sorted_top_data)):
                embed_.add_field(name=f'#{i+1} {sorted_top_data[i][0]}',
                value=f'{sorted_top_data[i][1]}', inline=False)
            await ctx.send(embed=embed_)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')
        
    @commands.command()
    async def toptotal(self, ctx):
        try:
            top_data = {}
            bank_data = load_bank_data()
            embed_ = discord.Embed(title=f'Richest people in {ctx.guild.name}',
                    colour=int(random.choice(choice_["COLOURS"]), 16))
            for member_ in ctx.guild.members:
                if str(member_.id) in bank_data:
                    top_data[f'{member_}'] = (bank_data[f'{member_.id}']['wallet']
                                            + bank_data[f'{member_.id}']['bank'])
            sorted_top_data = sorted(top_data.items(),
            key=lambda x : (x[1], x[0]), reverse=True)
            for i in range(5 if len(sorted_top_data)>5 else len(sorted_top_data)):
                embed_.add_field(name=f'#{i+1} {sorted_top_data[i][0]}',
                value=f'{sorted_top_data[i][1]}', inline=False)
            await ctx.send(embed=embed_)
        except Exception as e:
            await ctx.send(f'Exception occured :\n{e}')
     
    async def time_format(self, time_):
        sec = time_
        time_string = f'{sec}s'
        if sec >= 60:
            minute = sec // 60
            sec = sec % 60
            time_string = f'{minute}m {sec}s'
            if minute >= 60:
                hour = minute // 60
                minute = minute % 60
                time_string = f'{hour}h {minute}m {sec}s'
                if hour >= 24:
                    day = hour // 24
                    hour = hour % 24
                    time_string = f'{day}d {hour}h {minute}m {sec}s'
                    if day >= 7:
                        week = day // 7
                        day = day % 7
                        time_string = f'{week}w {day}d {hour}h {minute}m {sec}s'
        return time_string

def setup(client):
    client.add_cog(Bank(client))