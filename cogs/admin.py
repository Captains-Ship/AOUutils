import discord
from discord.ext import commands

from config import slash_guild
from utility.utils import *
from discord.ext.commands import *





class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @DevCommand()
    @commands.is_owner()
    async def sync(self, ctx, *, guild_id: int = None):
        if guild_id == 0:
            await self.client.tree.sync()
            await ctx.send("globally synced :D")
            return
        if guild_id is None:
            guild_id = ctx.guild.id
        await self.client.tree.sync(guild=discord.Object(id=guild_id))

    @DevCommand()
    @commands.is_owner()
    async def close(self, ctx):
        await ctx.reply('ok')
        await self.client.close()

    @commands.hybrid_command()
    @app_commands.guilds(slash_guild)
    @dev()
    async def locale_test(self, ctx: commands.Context):
        await ctx.reply(ctx.locale)

    @commands.hybrid_command()
    @app_commands.guilds(slash_guild)
    @dev()
    async def get_str(self, ctx: commands.Context, *, string: str):
        await ctx.reply(Response(ctx.locale)[string])

    
    








async def setup(client):
    await client.add_cog(Admin(client))
