import discord
from discord.ext import commands
import datetime
from utility.utils import *
from discord.ext.commands import *
import os






class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def check(self, ctx):
     return not str(ctx.author.id) in self.client.blacklist



    @commands.command()
    @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def reboot(self, ctx):
        await ctx.reply('ok')
        os.system('run.bat')
        await self.client.close()

    @commands.command()
    @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def close(self, ctx):
        await ctx.reply('ok')
        await self.client.close()



    
    








def setup(client):
    client.add_cog(Admin(client))