import datetime
import json

import discord
from discord.ext import commands

from utility.utils import Command, Response


class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client

    def get_full_data(self) -> dict:
        with open("afk.json", "r") as f:
            data = json.load(f)
        return data

    def set_afk(self, id: int, time: datetime.datetime = None, message: str = "AFK", active: bool = True) -> dict:
        data = self.get_full_data()
        if active == None:
            return data.get(str(id))
        
        if not time:
            time = datetime.datetime.now()
        
        if not data.get(str(id), None):
            data[str(id)] = {
                "time": int(time.timestamp()),
                "reason": message,
                "active": active
            }
        else:
            data[str(id)]["time"] = int(time.timestamp())
            data[str(id)]["reason"] = message
            data[str(id)]["active"] = active


        with open("afk.json", "w") as f:
            json.dump(data, f, indent=4)
        return data[str(id)]
    
    def set_auto(self, id: int, active: bool = True) -> dict:
        data = self.get_full_data()
        if active == None:
            return data.get(str(id))
        
        if not data.get(str(id), None):
            data[str(id)] = {
                "time": 0,
                "reason": "AFK",
                "active": False
            }

        data[str(id)]["autoafk"] = active

        with open("afk.json", "w") as f:
            json.dump(data, f, indent=4)
        return data[str(id)]



    @Command(description='Sets your afk status.',
                      usage='<reason>\n`reason`: The reason why you are going AFK. This is an optional argument.')
    async def afk(self, ctx, *, reason='AFK'):
        resp = Response(ctx.locale)
        self.set_afk(ctx.author.id, None, reason)
        await ctx.send(resp.afk_set.format(ctx.author.mention, reason))

    # @Command(description='toggles if your afk should be disabled when you talk')
    # async def toggleautoafk(self, ctx, toggled: bool = None):
    #     resp = Response(ctx.locale)
    #     if toggled == None:
    #         data = self.set_auto(ctx.author.id, None)
    #         toggled = not data.get("autoafk", False)

    #     self.set_auto(ctx.author.id, toggled)
    #     await ctx.send(resp.toggle.format(toggled))

    @Command()
    async def removeafk(self, ctx: commands.Context, member: discord.Member = None):
        resp = Response(ctx.locale)
        if member is not None:
            if not self.client.get_moderator() in ctx.author.roles:
                return await ctx.reply(resp.no_afk_perms)
        else:
            member = ctx.author
        try:
            data = self.set_afk(member.id, None, "AFK", None)
            if not data["active"]:
                raise Exception("User is not AFK.")
            
            self.set_afk(member.id, None, "AFK", False)
            await ctx.channel.send(
                resp.afk_removed.format(ctx.author.mention, "your" if member == ctx.author else "their")
            )
        except:
            await ctx.send(resp.not_afk.format("you" if member == ctx.author else "they"))


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        ctx = await self.client.get_context(message)
        if ctx.valid and ctx.command.name == "afk":
            return
        resp = Response(ctx.locale)
        data = self.get_full_data()
        
        if \
            data.get(str(ctx.author.id), None) \
            and data[str(ctx.author.id)]["active"] \
            and not data[str(ctx.author.id)].get("autoafk", False):

            self.set_afk(ctx.author.id, None, "AFK", False)
            await message.channel.send(resp.afk_removed.format(ctx.author.mention, "your"))
        
        for mention in message.mentions:
            if mention.id == ctx.author.id: 
                continue
            afk_data = data.get(str(mention.id), {})
            active = afk_data.get("active", False)
            if not active:
                continue
            await message.channel.send(f"{mention.name}, <t:{afk_data['time']}:R> is afk: {afk_data['reason']}")




        # with open('afk.json', 'r') as f:
        #     afk = json.load(f)
        #     try:
        #         e = True
        #         with open("toggleafk.json", "r") as f:
        #             tglafk = json.load(f)
        #             if tglafk[str(message.author.id)] == False:
        #                 e = False
        #     except KeyError:
        #         pass
        #     if e:
        #         try:
        #             print(afk[str(message.author.id)]['reason'])
        #             del afk[str(message.author.id)]
        #             await message.channel.send(resp.afk_removed.format(ctx.author.mention, "your"), delete_after=5)
        #         except:
        #             pass
        #     for mention in message.mentions:
        #         if str(mention.id) in afk:
        #             reason = afk[str(mention.id)]['reason']
        #             time = afk[str(mention.id)]['time']
        #             await message.channel.send(f'{mention.name}, <t:{time}:R>, is afk: {reason}')
        # with open('afk.json', 'w') as f:
        #     json.dump(afk, f, indent=4)


async def setup(client):
    await client.add_cog(Afk(client))
