import discord
from discord.ext import commands
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
from traceback import *
from logger import logger
from discord.ext.buttons import Paginator


def haseval():
    async def predicate(ctx):
        team = [347366054806159360]
        return ctx.author.id in team

    return commands.check(predicate)

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='eval', aliases=["exec"])
    @haseval()
    async def evaluation(self, ctx, *, code):
        team = [347366054806159360]
        if ctx.author.id in team:

            code = clean_code(code)

            local_variables = {
                "discord": discord,
                "commands": commands,
                "bot": self.client,
                "send": ctx.send,
                "reply": ctx.reply,
                "client": self.client,
                "ctx": ctx,
                "ctz": ctx,
                "CTX": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "e": discord.Embed,
                "m": discord.Member,
                "message": ctx.message,
	"code": code
            }

            stdout = io.StringIO()

            try:
                with contextlib.redirect_stdout(stdout):
                    exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                    )

                    obj = await local_variables["func"]()
                    result = f"{stdout.getvalue()}\n-- {obj}\n"
            except Exception as e:
                result = "".join(format_exception(e, e, e.__traceback__))

            pager = Pag(timeout=100, entries=[result[i: i + 2000] for i in range(0, len(result), 2000)], length=1,
                        prefix="AOUutils has completed the evaluation:```py\n", suffix="```")

            await pager.start(ctx)
        else:
            await ctx.send(f'{ctx.author.mention}\n`*inhales*`\nNo.')


def setup(client):
    client.add_cog(Eval(client))
