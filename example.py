import asyncio

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import hybrid_command
from config import slash_guild

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="amogus", description="amogus'ing moment")
    @app_commands.guilds(slash_guild)
    async def amogus(self, interaction: discord.Interaction):
        await interaction.response.send_message("amogus")
        print(interaction.user)

    @hybrid_command(name="sudo", description="superuser do")  # both message and slash command
    @app_commands.guilds(slash_guild)  # do not forget this!
    async def sudo(self, ctx: commands.Context, *, command: str):
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send(f"```sh\n{ctx.author}@Captain8771-mint:~$ {command}\noh no you don't```")


async def setup(bot):  # async now
    await bot.add_cog(Example(bot))  # async now
