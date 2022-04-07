import discord
from discord.ext import commands
import datetime
from utility.utils import *
from discord.ext.commands import *
import os
from logger import logger





class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.reply('ok')
        os.system('run.bat')
        await self.client.close()

    @commands.command()
    @commands.is_owner()
    async def close(self, ctx):
        await ctx.reply('ok')
        await self.client.close()



    
    








async def setup(client):
    await client.add_cog(Admin(client))
