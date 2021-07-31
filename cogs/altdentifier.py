import discord
from discord.ext import commands
from utility.rules import rules
import datetime
from logger import logger


class Altdentifier(commands.Cog):

    def __init__(self, client):
        self.client = client

    global inverif, leaveduringinverif
    inverif = []
    leaveduringverif = []

    async def verified(self, member):
        inverif.remove(member)

    async def verifymom(self, member):
        inverif.append(member)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bypass(self, ctx, member: discord.Member):
        if member.id in inverif:
            await self.verified(member.id)
            await ctx.reply(f'**Bypassed {member}**')
        else:
            await ctx.send(f'{member} isnt being verified.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def verify(self, ctx, member: discord.Member):
        if member.id not in inverif:
            await self.verifymom(member.id)
            await ctx.send(f'**Started verification on {member}**')
            await ctx.send(inverif)
        else:
            await ctx.send('They are already in verification')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 850668209148395520:
            if member.created_at == datetime.datetime.now() - datetime.timedelta(minutes=10):
                print(member)
                inverif.append(member.id)
            elif member.id in leaveduringverif:
                inverif.append(member.id)
                leaveduringverif.remove(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.id in inverif:
            inverif.remove(member.id)
            leaveduringverif.append(member.id)


def setup(client):
    client.add_cog(Altdentifier(client))
