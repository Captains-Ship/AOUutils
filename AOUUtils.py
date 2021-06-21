import json
import os
from jishaku.cog import Jishaku
import discord
from discord.ext import commands
import json
import traceback
import sys
from discord_slash import *
from traceback import *

async def get_pre(client, message):
    if message.guild == None:
        return ''
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            try:
                h = prefixes[str(message.author.id)]
                return commands.when_mentioned_or(prefixes[str(message.author.id)])(bot, message)
            except:
                return commands.when_mentioned_or('aou ', 'aou')(bot, message)
            

client = commands.Bot(
    command_prefix=get_pre,
    case_insensitive=True,
    status=discord.Status.dnd,
    activity=discord.Game(f'AOU'),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True
    ),
    strip_after_prefix=True
)
client.debug = False
client.blacklist = ['718915806754504766', '662290904203264010', '675474604533219360']
client.curblack = []
with open('config.json', 'r') as config:
    token = json.load(config)

#client.remove_command('help')
bot = client
client.remove_command('help')

@client.command()
async def prefix(ctx, *, prefix='aou '):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.author.id)] = str(prefix)
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        await ctx.send(f'Changed your prefix to `{prefix}`!')



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
