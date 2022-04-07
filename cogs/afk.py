import datetime
import json

import discord
from discord.ext import commands

import main


class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(description='Sets your afk status.',
                      usage='<reason>\n`reason`: The reason why you are going AFK. This is an optional argument.')
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

    @commands.command(description='toggles if your afk should be disabled when you talk')
    async def toggleautoafk(self, ctx):
        with open("toggleafk.json", "r") as f:
            tglafk = json.load(f)
            try:
                tglafk[str(ctx.author.id)] = not tglafk[str(ctx.author.id)]
            except KeyError:
                tglafk[str(ctx.author.id)] = False
        with open("toggleafk.json", "w") as f:
            json.dump(tglafk, f, indent=4)
        await ctx.send(f"Successfully toggled to `{tglafk[str(ctx.author.id)]}`!")

    @commands.command()
    async def removeafk(self, ctx: commands.Context, member: discord.Member = None):
        if member is not None:
            if not self.client.get_moderator() in ctx.author.roles:
                return await ctx.reply("You do not have the permission to remove other's afk.")
        else:
            member = ctx.author
        try:
            with open("afk.json", "r") as f:
                afk = json.load(f)
                print(afk[str(member.id)]['reason'])
                del afk[str(member.id)]
            with open("afk.json", "w") as f:
                json.dump(afk, f, indent=4)
                await ctx.channel.send(
                    f'{member.mention} I have removed your afk.' if member == ctx.author else f'I have removed {member}\'s afk.')
        except KeyError:
            await ctx.send("You aren't afk!" if member == ctx.author else f"{member} isn't afk!")

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
                e = True
                with open("toggleafk.json", "r") as f:
                    tglafk = json.load(f)
                    if tglafk[str(message.author.id)] == False:
                        e = False
            except KeyError:
                pass
            if e:
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


async def setup(client):
    await client.add_cog(Afk(client))
