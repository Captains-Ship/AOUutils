import discord
from discord.ext import commands
from utility.utils import database
from asyncio import run


class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = self.client.tag_db

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tagname=None):
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", (tagname.lower()))
        await ctx.send([x for x in await x.fetchone()][1])

    @tag.command()
    async def info(self, ctx, *, tagname=None):
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", (tagname.lower()))
        x = await x.fetchone()
        if x[2] == -1:
            owner = "System Tag"
        else:
            owner = self.client.get_user(int(x[2])) or self.client.fetch_user(int(x[2]))
            owner = owner.name
        embed = discord.Embed(
            title=tagname,
            description=f"Owner: {owner}",
            color=discord.Color.dark_theme()
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Tags(client))
