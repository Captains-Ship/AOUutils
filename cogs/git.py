from os import system, listdir
from json import load
from discord.ext import commands
import logger
class Git(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def git(self, ctx):
        """
        a variety of git commands
        """
        pass

    @git.command()
    @commands.is_owner()
    async def pull(self, ctx):
        with open('config.json', 'r') as f:
            config = load(f)
        system(f"git pull https://{config['github']}:{config['tokens']['github']}@github.com/captains-ship/aouutils")
        await ctx.send("Pulled, reloading cogs!")
        for filename in listdir(r'./cogs'):
            if filename.endswith('.py'):
                try:
                    self.client.reload_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    logger.error(f"Error loading cog `cogs.{filename[:-3]}`, error:\n{e}") # couldnt be bothered checking if it was new, cry about it
    @git.command()
    @commands.is_owner()
    async def push(self, ctx, *, message="Push through AOUutils"):
        with open('config.json', 'r') as f:
            config = load(f)
        system("git add .")
        system(f"git commit -a -m {message}")
        system(f"git push https://{config['github']}:{config['tokens']['github']}@github.com/captains-ship/aouutils")
        await ctx.send("Pushed!")

def setup(client):
    client.add_cog(Git(client))
