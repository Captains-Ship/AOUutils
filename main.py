#!/usr/bin/env python3
import asyncio
import json
import os
from jishaku.cog import Jishaku
import discord
from discord.ext import commands
from apilol import start
from logger import logger
from utility.utils import getconfig
from io import BytesIO
import config
import aiohttp
from traceback import format_exception


# os.chdir(__file__) # this was a skill issue

# TODO: Un-hardcode all the "all of us" scattered throughout the code.
#  -this includes commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info('Logging in...')
        self.tag_db = None
        self.recentlyflagged = {}
        self.session: aiohttp.ClientSession = None


    async def setup_hook(self):
        """
        this is run when the bot is starting but not ready
        its async so you can await stuff
        """
        # await self.load_extension('jishaku') # remind me when jsk works on latest discord.py
        for filename in os.listdir(r'./cogs'):
            if filename.endswith('.py'):
                if filename.startswith("_"):
                    continue
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'Loaded extension {filename}')
                except Exception as e:
                    logger.error(f"Error loading cog `cogs.{filename[:-3]}`")
                    # format the traceback and print it to the console
                    logger.error("".join(format_exception(type(e), e, e.__traceback__)))



    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=config.slash_guild))

    def get_general_staff(self):
        return self.get_server().get_role(config.staff_role)

    def get_general_dev(self):
        return self.get_server().get_role(config.dev_role)

    def get_server(self):
        return self.get_guild(config.server)

    def get_moderator(self):
        return self.get_server().get_role(config.moderator)

    def get_admin(self):
        return self.get_server().get_role(config.admin)

    def get_dev_server(self):
        return self.get_guild(config.dev_server)

    async def start(self, *args, **kwargs):
        async with aiohttp.ClientSession() as self.session:
            await super().start(*args, **kwargs)

    async def get_cdn(self, filename):
        x = "https://" + config.cdn + "/" + filename
        async with self.session.get(x) as resp:
            return BytesIO(await resp.read())

    def get_bot_devs(self):
        return config.devs

    async def load_extension(self, *args, **kwargs) -> None:
        await super().load_extension(*args, **kwargs)


async def get_pre(client, message):
    return commands.when_mentioned_or(config.prefix)(client, message)
    # if not message.guild:
    #     return ''
    # else:
    #     with open('prefixes.json', 'r') as f:
    #         prefixes = json.load(f)
    #         try:
    #             h = prefixes[str(message.author.id)]
    #             return commands.when_mentioned_or(prefixes[str(message.author.id)])(client, message)
    #         except KeyError:
    #             return commands.when_mentioned_or(config.prefix)(client, message)


bot = Bot(
    command_prefix=get_pre,
    case_insensitive=True,
    status=discord.Status.dnd,
    activity=discord.Game(f'Launching...'),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True
    ),
    owner_ids=config.owners,
    strip_after_prefix=True
)
bot.debug = False


# start(client) # this used to start the API nobody uses
# disabled for now because it's not needed
# also performance poggers


@bot.command()
async def prefix(ctx, *, prefix=config.prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        if prefix == 'aou':
            prefixes[str(ctx.author.id)] = 'aou '
        else:
            prefixes[str(ctx.author.id)] = str(prefix)
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        await ctx.send(f'Changed your prefix to `{prefix}`!')


@bot.event
async def on_message(msg):
    if msg.author.id not in config.blacklist:
        await bot.process_commands(msg)
    else:
        ctx = await bot.get_context(msg)
        if ctx.valid:
            embed = discord.Embed(
                title="Uh Oh...",
                description=f"Looks like you've been blacklisted, so you can't run {ctx.invoked_with}",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


@bot.command(aliases=['load'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def loadextension(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.reply('loaded!')


@bot.command(aliases=['unload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def unloadextension(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.reply('unloaded!')


@bot.command(aliases=['reload'], hidden=True)
@commands.is_owner()
@commands.has_permissions(administrator=True)
async def reloadextension(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.reply('Reloaded!')


async def main():
    token = config.token \
        if not config.beta \
        else config.beta_token
    await bot.start(token, reconnect=True)
    # im not sure but i remember something
    # about needing to use async context manager with bot to run it
    # but i cant find anything about it so i'm just gonna leave it here for now


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
