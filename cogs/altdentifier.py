import discord
from discord.ext import commands
from utility.rules import rules

class Altdentifier(commands.Cog):

    def __init__(self, client):
        self.client = client



    global inverif, leaveduringinverif
    inverif = []
    leaveduringverif = []

    async def verified(self, member):
        inverif.remove(member)

    async def verify(self, member):
        inverif.append(member)
    
    async def checkverif(self, member):
        for id in inverif:
            if id == member:
                yes = 1
            else:
                pass
        try:
            if yes == 1:
                return True
            else:
                return False
        except:
            return False

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bypass(self, ctx, member: discord.Member):
        if await self.checkverif(member.id):
            await self.verify(self, member.id)
            await ctx.reply(f'**Bypasses {member}**')
        else:
            await ctx.send(f'{member} isnt being verified.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def verify(self, ctx, member: discord.Member):
        if await self.checkverif(member.id):
            await self.verify(self, member.id)
            await ctx.send(f'**Started verification on {member}**')
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