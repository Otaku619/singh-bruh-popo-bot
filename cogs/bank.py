import discord
from discord.ext import commands
import os
import json
import random
import time

def load_data():
    f=open("./cogs/bank.json")
    return json.load(f)

def save_data(data):
    with open("./cogs/bank.json","w") as f:
        json.dump(data,f)
    f.close()
    

fil=open('messages.json')
messages=json.load(fil)

class _BANK(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def bal(self,msg:discord.Message):
        data=load_data()
        id=str(msg.author.id)
        if id not in data:
            data.update({id:{"wallet":0,"bank":0,"debt":0,"time":0}})
            await msg.channel.send('Account Created Successfully!')
        embed=discord.Embed(title=f"{str(msg.author)[:-5]}'s balance")
        embed.add_field(name="Wallet", value=data[id]["wallet"],inline=True)
        embed.add_field(name="Bank", value=data[id]["bank"],inline=True)
        embed.add_field(name="Debt", value=data[id]["debt"],inline=True)
        await msg.channel.send(embed=embed)
        save_data(data)
    
    @commands.command(aliases=['free','Free'])
    async def FREE(self,msg:discord.Message):
        data=load_data()
        id=str(msg.author.id)
        if id not in data:
            await msg.channel.send('Please open an account first by typing ;bal')
        else:
            if round(time.time())>=data[id]['time']+60:
                data[id]['time']=round(time.time())
                free=random.randint(0,100)
                free_exp=random.randint(0,len(messages["FREE"])-1)
                if free_exp==2:
                    await msg.channel.send(messages["FREE"][free_exp].format(str(msg.author)[:-5],free))
                else:
                    await msg.channel.send(messages["FREE"][free_exp].format(str(msg.author)[:-5],free))
                    data[id]["wallet"]+=free
            else:
                embed=discord.Embed()
                embed.add_field(name='Thand Rakh', value=f"You need to wait {data[id]['time']+60-round(time.time())}s more to get the free stuff", inline=False)
                await msg.channel.send(embed=embed)
        save_data(data)

def setup(client):
    client.add_cog(_BANK(client))