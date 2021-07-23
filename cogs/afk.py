import discord
import datetime
from discord.ext import *
import json
from logger import logger

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
            h = str(datetime.datetime.now().timestamp()).split('.')
            user['time'] = h[0]
        with open('afk.json', 'w') as f:
            json.dump(afk, f, indent=4)
            await ctx.send(f'{ctx.author.mention} i set your afk: {reason}')

    @commands.Cog.listener()
    async def on_message(self, message):
        dtdt = datetime.datetime
        dt = datetime
        if message.author.bot:
            return
        # ctx = await self.client.get_context(message)
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
                        reason = afk[str(mention.id)]['reason']
                        time = afk[str(mention.id)]['time']
                        await message.channel.send(f'{mention.name}, <t:{time}:R>, is afk: {reason}')
        with open('afk.json', 'w') as f:
            json.dump(afk, f, indent=4)


def setup(client):
    client.add_cog(Afk(client))
