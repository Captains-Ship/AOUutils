import asyncio

import discord
from discord.ext import commands
import datetime

from discord.ext.buttons import Paginator
from discord.ext.commands import CommandError

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

    async def on_help_command_error(self, ctx, error):
        await ctx.send(error)

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            # U+2002 Middle
            joined = ', '.join(c.name for c in commands)
            self.paginator.add_line(f'__**{heading}**__')
            self.paginator.add_line(joined)
            self.filter_commands(commands)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            help_embed = discord.Embed(
                title='Help Menu',
                description=page,
                colour=discord.Colour.red(),
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.set_footer(icon_url=self.context.author.display_avatar.url, text=self.context.author)

            await destination.send(embed=help_embed)

    def get_ending_note(self):
        return """Bot Provided by the AOUutils Team.  
                  EnderB0YHD, Toasty, GingerGigiCat, Robin, Captain."""

    async def filter_commands(self, commands, *, sort=False, key=None):
        if sort and key is None:
            key = lambda c: c.name

        iterator = commands if self.show_hidden else filter(lambda c: not c.hidden, commands)

        if self.verify_checks is False:
            return sorted(iterator, key=key) if sort else list(iterator)

        if self.verify_checks is None and not self.context.guild:
            return sorted(iterator, key=key) if sort else list(iterator)

        async def predicate(cmd):
            try:
                return await cmd.can_run(self.context)
            except CommandError:
                return False

        ret = []
        for cmd in iterator:
            valid = await predicate(cmd)
            if valid:
                ret.append(cmd)

        if sort:
            ret.sort(key=key)
        return ret


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
