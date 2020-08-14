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

    @commands.command(aliases=['Bal', 'BAL',])
    async def bal(self, ctx, user : discord.Member=None):
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
    
    @commands.command(aliases=['Free', 'FREE', ])
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
                        value=f"You need to wait {time_data[id]['free']+60-round(time.time())}s more to get the free stuff",
                        inline=False
                    )
                await ctx.send(embed=embed)
        save_data(bank_data,time_data)
    
    @commands.command(aliases=['Dep', 'DEP', 'dep', 'Deposit', 'DEPOSIT'],)
    async def deposit(self, ctx, *, amount):
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
                        value=f"You need to wait {time_data[id]['dep']+20-round(time.time())}s more to deposit your sh*t",
                        inline=False
                    )
                await ctx.send(embed=embed)
        save_data(bank_data,time_data)
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

    @commands.command(aliases=['With', 'WITH', 'WITHDRAW', 'with', 'Withdraw', ])
    async def withdraw(self, ctx, *, amount):
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
                        value=f"You need to wait {time_data[id]['with']+20-round(time.time())}s more to withdraw your sh*tty funds",
                        inline=False
                    )
                await ctx.send(embed=embed)
        save_data(bank_data,time_data)

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

def setup(client):
    client.add_cog(Bank(client))