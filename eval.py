import discord
import random
from discord.ext import commands
from discord.ext.commands import cog
from discord.ext import tasks
from itertools import cycle
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
from traceback import format_exception
import io
import contextlib
from io import BytesIO
from pprint import pprint
import os
import textwrap
import asyncio
import json
import datetime
import urllib.request
import traceback
async def evale():
    try:
        inputted = input('>>> ')
        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": client,
            "send": ctx.send,
            "client": client,
            "ctx": ctx,
            "ctz": ctx,
            "CTX": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "e": discord.Embed,
            "m": discord.Member,
            "message": ctx.message
        }
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(inputted, '    ')}",
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
            print(result)
    except Exception as error:
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
evale()
