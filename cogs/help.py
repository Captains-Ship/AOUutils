import discord
from discord.ext import commands
import datetime

from discord.ext.buttons import Paginator
from logger import logger


class HelpUwU(commands.MinimalHelpCommand):

    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    def get_opening_note(self):
        command_name = self.invoked_with
        return (
            f"Use `{self.context.clean_prefix}{command_name} [command]` for more info on a command.\n"
            f"You can also use `{self.context.clean_prefix}{command_name} [category]` for more info on a category. (CASE SENSITIVE)"
        )

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            # U+2002 Middle Dot
            joined = ', '.join(c.name for c in commands)
            self.paginator.add_line(f'__**{heading}**__')
            self.paginator.add_line(joined)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            help_embed = discord.Embed(
                title='Help Menu',
                description=page,
                colour=discord.Colour.red(),
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.set_footer(icon_url=self.context.author.avatar.url, text=self.context.author)

            await destination.send(embed=help_embed)

    def get_ending_note(self):
        return """Bot Provided by the AOUutils Team.  
                  EnderB0YHD, Toasty, GingerGigiCat, Captain."""


class Help(commands.Cog):

    def __init__(self, client):
        attributes = {
            'name': "help"
        }
        self.client = client
        self.client.original_help = self.client.help_command
        self.client.help_command = HelpUwU(command_attrs=attributes)

    def cog_unload(self):
        self.client.help_command = commands.DefaultHelpCommand()


def setup(client):
    client.add_cog(Help(client))
