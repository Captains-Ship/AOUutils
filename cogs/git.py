from os import listdir
from json import load
from discord.ext import commands
import logger
from utility.utils import run
import re
from config import owners
import discord
from discord import app_commands
from config import slash_guild


class AdminPanel(discord.ui.View):
    def __init__(self, *args, **kwargs):
        self.bot = kwargs.pop("bot")
        super().__init__(*args, **kwargs)

    @discord.ui.button(label="reload cogs", style=discord.ButtonStyle.blurple)
    async def reload_cogs(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in owners:
            return await interaction.response.send_message("You are not an owner smh", ephemeral=True)
        final = ""
        for cog in listdir("cogs"):
            if cog.endswith(".py"):
                try:
                    await self.bot.reload_extension(f"cogs.{cog[:-3]}")
                    final += f"\U00002705 cogs.{cog[:-3]}\n\n\n"
                except Exception as e:
                    final += f"\U0000274C cogs.{cog[:-3]}\n\n\n"
                    logger.error(f"{cog[:-3]} failed to reload: {e}")
        await interaction.response.send_message(final)

    @discord.ui.button(label="restart bot", style=discord.ButtonStyle.danger)
    async def restart_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in owners:
            return await interaction.response.send_message("You are not an owner smh", ephemeral=True)
        await interaction.response.send_message("restarting...")
        await self.bot.close()  # use a process manager like pm2 or docker to restart the bot


class Git(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(name="git")
    @app_commands.guilds(slash_guild)
    @commands.is_owner()
    async def git(self, ctx: commands.Context):
        """
        a variety of git commands
        """
        pass

    @git.command(name="pull")
    @commands.is_owner()
    async def pull(self, ctx: commands.Context):
        # with open('config.json', 'r') as f:
        #     config = load(f)
        proc, stdout, stderr = await run(f"git pull")
        stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
        await ctx.send("Pulled, reloading cogs!")
        # make a regex and match it to the stdout for every file in cogs/
        # if it matches, reload the cog
        # if it doesn't match, don't reload the cog
        reg = re.compile(r"cogs/(.*)\.py")
        changed_cogs = reg.findall(stdout)
        errors = []
        for cog in changed_cogs:
            try:
                await self.client.reload_extension(f"cogs.{cog}")
            except Exception as e:
                logger.error(f"{cog} failed to reload: {e}")
                await ctx.send("failed to reload cogs." + cog)
                errors.append(e)
        if errors:
            raise errors[0]
        await ctx.send(f"```sh\n{stdout}```", view=AdminPanel(bot=self.client))  # amogus

    @git.command(name="push")
    @commands.is_owner()
    async def push(self, ctx: commands.Context, *, message: str = "Push through AOUutils"):
        # with open('config.json', 'r') as f:
        #     config = load(f)
        await run("git add .")
        await run(f"git commit -a -m \"{message}\"")
        # i fixed my problem with git not saving token so now i can just git push
        await run(f"git push")
        await ctx.send("Pushed!")


async def setup(client):
    await client.add_cog(Git(client))
