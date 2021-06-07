import json
import os

import discord
from discord.ext import commands

client = commands.Bot(
    command_prefix=commands.when_mentioned_or('aou ', 'AOU', 'Aou'),
    case_insensitive=True,
    status=discord.Status.dnd,
    activity=discord.Game(f'AOU'),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True
    )
)
client.blacklist = ['675474604533219360', '347366054806159360']
with open('config.json', 'r') as config:
    token = json.load(config)

client.remove_command('help')
bot = client


@client.command(aliases=['load'])
@commands.has_permissions(administrator=True)
async def loadExtension(ctx, extension):
    client.load_extension(f'cogs.{extension} loaded')


@client.command(aliases=['unload'])
@commands.has_permissions(administrator=True)
async def unloadExtension(ctx, extension):
    client.unload_extension(f'cogs.{extension} unloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token['token'])
