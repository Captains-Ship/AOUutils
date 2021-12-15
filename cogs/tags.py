import discord
from discord.ext import commands
from utility.utils import database, dev
from asyncio import run


class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tagname):
        """Tags"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", (tagname.lower()))
        try:
            t = await x.fetchone()
            e = [x for x in t]
            content = e[0]
            embed = bool(e[3])
            if embed:
                embed = discord.Embed(
                    title=tagname.lower(),
                    description=content,
                    color=discord.Color.red()
                )
            await ctx.send(content if not embed else None, embed = embed if embed else None, allowed_mentions=discord.AllowedMentions.none())
        except TypeError:
            await ctx.send("Unknown tag")

    @tag.command()
    async def list(self, ctx):
        """Lists tags"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags")
        x = x.fetchall()
        l = ""
        for i in x:
            l += f"\n{i[1]}"
        l = l.lstrip("\n")
        embed = discord.Embed(
            title="Tag list",
            description=x,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

    @dev()
    @tag.command()
    async def create(self, ctx, tag_name, *, content):
        """Creates a tag"""
        if tag_name.lower() in ["delete", "create", "info", "list"]:
            return await ctx.send("tag_name may not be a reserved keyword.")
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", tag_name.lower())
        embed = "--embed" in content
        if embed:
            content = content.replace("--embed", "")
        try:
            e = [x for x in await x.fetchone()]
            await ctx.send(f"Tag {tag_name!r} already exists")
        except TypeError:
            await db.exec("INSERT INTO tags VALUES (?, ?, ?, ?)", (content, tag_name.lower(), ctx.author.id, embed))
            # the above schema is weird but it is what it is
            await ctx.send("Created!")

    @dev()
    @tag.command()
    async def delete(self, ctx, tag_name):
        """deletes a tag"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", tag_name)
        try:
            e = [x for x in await x.fetchone()]
        except TypeError:
            return await ctx.send("Unknown tag")
        e = await db.exec("DELETE FROM tags WHERE tagname = ?", tag_name)
        await ctx.send("Tag deleted")

    @tag.command()
    async def info(self, ctx, *, tagname):
        """gets info about a tag"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", (tagname.lower()))
        x = await x.fetchone()
        try:
            if x[2] == -1:
                owner = "System Tag"
            else:
                owner = self.client.get_user(int(x[2])) or await self.client.fetch_user(int(x[2]))
                if owner:
                    owner = str(owner)
                else:
                    owner = "?"
            embed = discord.Embed(
                title=tagname,
                description=f"Owner: {owner}",
                color=discord.Color.red()
            )
            embed.add_field(name="Embedded tag?", value=str(int(x[3]) == 1))
            embed.set_thumbnail(
                url=self.client.get_aou().icon.url
            )
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send("Unknown tag")


def setup(client):
    client.add_cog(Tags(client))
