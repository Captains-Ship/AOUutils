import discord
from discord.ext import commands
from discord import app_commands
from config import slash_guild

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="amogus", description="amogus'ing moment")
    @app_commands.guilds(slash_guild)
    async def amogus(self, interaction: discord.Interaction):
        await interaction.send("amogus")
        print(interaction.user)



async def setup(bot):  # async now
    await bot.add_cog(Example(bot))  # async now
