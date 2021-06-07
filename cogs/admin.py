import discord
from discord.ext import commands
import datetime
from utility.utils import *
from discord.ext.commands import *
import os


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reboot(self, ctx):
        await ctx.reply('ok')
        os.run('run.bat')
        self.client.close()



    
    








def setup(client):
    client.add_cog(Admin(client))