import difflib

import discord
from discord.ext import commands

import config
from utility.paginators import ButtonPaginator as Paginator
from utility.utils import database, dev
from asyncio import run
from discord.ext.buttons import Paginator
from tagformatter import Parser
import random

parser = Parser(case_insensitive=True)  # hate to have to do it this way

@parser.tag('author', aliases=['member', 'user'])
def a(env):
    return env.author.name

@a.tag('mention', alias='ping')
def am(env):
    return env.author.mention

@a.tag('discriminator', alias='discrim')
def ad(env):
    return env.author.discriminator


class tag_modal(discord.ui.Modal, title="Create tag"):
    name = discord.ui.TextInput(label="Tag name")
    content = discord.ui.TextInput(label="Tag content", style=discord.TextStyle.paragraph, max_length=1984) # literally 1984

    async def on_submit(self, interaction: discord.Interaction):
        tag_name = self.name.value
        content = self.content.value
        if len(content) > 1975:
            await interaction.response.send_message(
                f"Tag content is too long. Max length is 1975 characters."
            )
            return
        if tag_name.lower() in ["delete", "create", "info", "list"]:
            return await interaction.response.send_message("tag_name may not be a reserved keyword.")
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", tag_name.lower())
        embed = "--embed" in content
        if embed:
            content = content.replace("--embed", "")
        try:
            e = [x for x in await x.fetchone()]
            await interaction.response.send_message(f"Tag {tag_name!r} already exists")
        except TypeError:
            await db.exec("INSERT INTO tags VALUES (?, ?, ?, ?)",
                          (content, tag_name.lower(), interaction.user.id, embed))
            # the above schema is weird but it is what it is
            await interaction.response.send_message("Created!")

@a.tag('id')
def ai(env):
    return env.author.id

@parser.tag('prefix')
def p(env):
    return env.prefix

@parser.tag('random')
def r(env, low: int, high:int):
    return random.randint(low, high)

class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.parser = parser

    async def send_final_tag(self, ctx, tag):
        env = {
            "prefix": ctx.prefix,
            "author": ctx.author
            }
        tagname = tag['name']
        tagcontent = tag['content']
        embed = tag['embed']
        tagcontent = self.parser.parse(tagcontent, env)
        if embed:
            tosend = discord.Embed(
                title=tagname,
                description=tagcontent.replace("&l;", "{").replace("&r;", "}").replace("&amp;", "&"),
                color=discord.Color.red()
            )
            await ctx.send(embed=tosend)
        else:
            tosend = tagcontent.replace("&l;", "{").replace("&r;", "}").replace("&amp;", "&")
            await ctx.send(tosend, allowed_mentions=discord.AllowedMentions.none())

        self.tag_content = None
        self.cache = []

    tag_group = discord.app_commands.Group(
        name='tag',
        description='Manage tags',
        guild_ids=[config.slash_guild]
    )

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
            await self.send_final_tag(ctx, {"name": tagname.lower(), "content": content, "embed": embed})
        except TypeError:
            await ctx.send("Unknown tag")

    @tag.command()
    async def list(self, ctx):
        """Lists tags"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags")
        x = await x.fetchall()
        l = ""
        for i in x:
            l += f"\n{[e for e in i][1]}".replace("\\", "\\\\").replace("_", "\\_").replace("*", "\\*").replace("`",
                                                                                                                "\\`").replace(
                "<", "<\\")
        l = l.lstrip("\n")
        l = [l[i: i + 2000] for i in range(0, len(l), 2000)]
        pag = Paginator(pages=l, timeout=100, title="Tags", color=discord.Color.red())
        await pag.start(ctx)

    @tag_group.command(name="create", description="Create a new tag.")
    async def tag_create(self, interaction: discord.Interaction):
        devs = [553677148611936267, 742976057761726514, 347366054806159360, 721745855207571627, 535059139999825922,
                813770420758511636]
        if interaction.user.id not in devs:
            return await interaction.response.send_message("You are not a developer", ephemeral=True)
        await interaction.response.send_modal(tag_modal())
        self.cache = None


    async def tag_autocomplete(self, interaction: discord.Interaction, current: str):
        if not self.cache:
            db = await database.init("tags")
            x = await db.exec("SELECT * FROM tags")
            self.cache = [e[1] for e in [i for i in await x.fetchall()]]
        matches = difflib.get_close_matches(current, self.cache, n=10, cutoff=0.6)
        return list(set([discord.app_commands.Choice(name=e[:100], value=e) for e in matches] + [
            discord.app_commands.Choice(name=e[:100], value=e) for e in self.cache if current in e]))[:10]

    @tag_group.command(name="view", description="View a tag.")
    @discord.app_commands.describe(tagname="The tag to view.")
    @discord.app_commands.autocomplete(tagname=tag_autocomplete)
    async def tag_view(self, interaction: discord.Interaction, tagname: str):
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", tagname.lower())
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
            await interaction.response.send_message(content if not embed else None, embed=embed if embed else None,
                                                    allowed_mentions=discord.AllowedMentions.none())
        except TypeError:
            await interaction.response.send_message("Unknown tag")

    @tag_group.command(name="list", description="List all the available tags.")
    async def tag_list(self, interaction: discord.Interaction):
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags")
        x = await x.fetchall()
        l = ""
        for i in x:
            l += f"\n{[e for e in i][1]}".replace("\\", "\\\\").replace("_", "\\_").replace("*", "\\*").replace("`",
                                                                                                                "\\`").replace(
                "<", "<\\")
        l = l.lstrip("\n")
        l = [l[i: i + 2000] for i in range(0, len(l), 2000)]
        embed = discord.Embed(
            title="Tags",
            description="".join(l),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tag_group.command(name="delete", description="Delete a tag.")
    @discord.app_commands.describe(tagname="The tag to delete.")
    @discord.app_commands.autocomplete(tagname=tag_autocomplete)
    async def tag_delete(self, interaction: discord.Interaction, tagname: str):
        devs = [553677148611936267, 742976057761726514, 347366054806159360, 721745855207571627, 535059139999825922,
                813770420758511636]
        if interaction.user.id not in devs:
            return await interaction.response.send_message("You are not a developer", ephemeral=True)
        db = await database.init("tags")
        x = await db.exec("DELETE FROM tags WHERE tagname = ?", (tagname.lower()))
        await interaction.response.send_message("Tag deleted")
        self.cache = None

    class TagEditModal(discord.ui.Modal, title="Edit tag"):
        content = discord.ui.TextInput(label="Tag content", style=discord.TextStyle.paragraph, max_length=1984)

        def __init__(self, tag_content, tagname):
            self.tag_content = tag_content
            self.tagname = tagname
            self.content._underlying.value = tag_content
            self.content._value = tag_content
            super().__init__()

        async def on_submit(self, interaction: discord.Interaction):
            db = await database.init("tags")
            x = await db.exec("UPDATE tags SET content = ? WHERE tagname = ?", (self.content.value, self.tagname))
            await interaction.response.send_message("Tag edited")

    @tag_group.command(name="edit", description="Edit a tag.")
    @discord.app_commands.describe(tagname="The tag to edit.")
    @discord.app_commands.autocomplete(tagname=tag_autocomplete)
    async def tag_edit(self, interaction: discord.Interaction, tagname: str):
        db = await database.init("tags")
        tag_content = await db.exec("SELECT * FROM tags WHERE tagname = ?", tagname.lower())
        tag_content = await tag_content.fetchone()
        try:
            tag_content = [x for x in tag_content]
        except TypeError:
            return await interaction.response.send_message("Unknown tag")
        tag_content = tag_content[0]
        modal = self.TagEditModal(tag_content, tagname)
        await interaction.response.send_modal(modal)

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
        self.cache = None

    @dev()
    @tag.command()
    async def delete(self, ctx, *, tag_name):
        """deletes a tag"""
        db = await database.init("tags")
        x = await db.exec("SELECT * FROM tags WHERE tagname = ?", tag_name)
        try:
            e = [x for x in await x.fetchone()]
        except TypeError:
            return await ctx.send("Unknown tag")
        e = await db.exec("DELETE FROM tags WHERE tagname = ?", tag_name)
        await ctx.send("Tag deleted")
        self.cache = None


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
                url=self.client.get_server().icon.url
            )
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send("Unknown tag")


async def setup(client):
    await client.add_cog(Tags(client))
