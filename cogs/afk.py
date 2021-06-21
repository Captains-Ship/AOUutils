import discord
import datetime
from discord.ext import *
import json

class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def afk(self, ctx, *, reason='AFK'):
        dt = datetime.datetime
        time = dt.now()
        with open('afk.json', 'r') as f:
            afk = json.load(f)
            afk[str(ctx.author.id)] = {}
            user = afk[str(ctx.author.id)]
            user['reason'] = reason
            user['time'] = str(dt.now())
        with open('afk.json', 'w') as f:
            json.dump(afk, f, indent=4)
            await ctx.send(f'{ctx.author.mention} i set your afk: {reason}')
    

    @commands.Cog.listener()
    async def on_message(self, message):
        dtdt = datetime.datetime
        dt = datetime
        if message.author.bot:
            return
        #ctx = await self.client.get_context(message)
        with open('afk.json', 'r') as f:
            afk = json.load(f)
            try:
                print(afk[str(message.author.id)]['reason'])
                del afk[str(message.author.id)]
                await message.channel.send(f'{message.author.mention} I have removed your afk.', delete_after=5)
            except:
                pass
                for mention in message.mentions:
                    if str(mention.id) in afk:
                        hehe = afk[str(mention.id)]['time'].split('.')[0]
                        timekek = dtdt.strptime(hehe, '%Y-%m-%d %H:%M:%S')
                        timekek2 = datetime.datetime.now() - timekek
                        time = timekek2.total_seconds()
                        timeformat = str(datetime.timedelta(seconds=time))
                        timelol = timeformat.split(':')
                        s3 = timelol[2]
                        s2 = s3.split('.')
                        s = s2[0]
                        m = timelol[1]
                        h = timelol[0]
                        reason = afk[str(mention.id)]['reason']
                        await message.channel.send(f'{mention.name} is afk: {reason}\n{h} Hours, {m} Minutes and {s} Seconds ago.')
        with open('afk.json', 'w') as f:
            json.dump(afk, f, indent=4)
            
            



def setup(client):
    client.add_cog(Afk(client))