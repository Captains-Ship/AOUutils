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
from apilol import *
import datetime
import sys
from logger import logger
from utility.utils import getconfig

start()


class AOUbot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_aou(self):
        return self.get_guild(794950428756410429)

    def get_dev_server(self):
        return self.get_guild(850668209148395520)

    def get_bot_devs(self):
        devrole = self.get_dev_server().get_role(866618255917580309)
        devs = []
        for member in self.get_dev_server().members:
            if devrole in member.roles:
                devs.append(member.id)
        return devs


async def get_pre(client, message):
    if not message.guild:
        return ''
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            try:
                h = prefixes[str(message.author.id)]
                return commands.when_mentioned_or(prefixes[str(message.author.id)])(client, message)
            except KeyError:
                return commands.when_mentioned_or('aou ', 'aou')(client, message)


client = AOUbot(
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

# client.remove_command('help')
bot = client
AOUclient = client

@client.command()
async def prefix(ctx, *, prefix='aou'):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        if prefix == 'aou':
            prefixes[str(ctx.author.id)] = 'aou '
        else:
            prefixes[str(ctx.author.id)] = str(prefix)
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        await ctx.send(f'Changed your prefix to `{prefix}`!')


@client.event
async def on_message(msg):
    config = getconfig()
    if not msg.author.id in config['blacklist']:
        await client.process_commands(msg)


@client.command(aliases=['load'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def loadextension(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply('loaded!')


@client.command(aliases=['unload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def unloadextension(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply('unloaded!')


@client.command(aliases=['reload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def reloadextension(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.reply('Reloaded!')


bot.load_extension('jishaku')
# client.load_extension('jishaku')
for filename in os.listdir(r'.\cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            logger.error(f"Error loading cog `cogs.{filename[:-3]}`, error:\n{e}")

config = getconfig()

client.run(config['tokens']['discord'])