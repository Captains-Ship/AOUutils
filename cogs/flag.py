import discord
from discord.ext import commands
from discord.ext.commands import *

class Flag(commands.Cog):

    def __init__(self, client):
        self.client = client\

    





def setup(client):
    client.add_cog(Flag(client))