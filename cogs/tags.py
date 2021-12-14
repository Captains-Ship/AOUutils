import discord
from discord.ext import commands
import urllib.request, json
from logger import logger
class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Tags(client))
