import json
import os
from jishaku.cog import Jishaku
import discord
from discord.ext import commands
import json
import traceback
import sys
from discord_slash import *


            

client = commands.Bot(
    command_prefix=commands.when_mentioned_or('aou '),
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
client.curblack = [742976057761726514]
with open('config.json', 'r') as config:
    token = json.load(config)

#client.remove_command('help')
bot = client
client.remove_command('help')


@client.command(aliases=['load'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def loadExtension(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply('loaded!')


@client.command(aliases=['unload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def unloadExtension(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply('unloaded!')



@client.command(aliases=['reload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def reloadExtension(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.reply('Reloaded!')
bot.load_extension('jishaku')
#client.load_extension('jishaku')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token['token'])
