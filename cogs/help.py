import discord
from discord.ext import commands
import datetime
class HelpUwU(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(
                title='Help Menu',
                description=page,
                colour = discord.Colour.red(),
                timestamp=datetime.datetime.utcnow()
                )
            emby.set_footer(icon_url=self.context.author.avatar_url, text=self.context.author)
            await destination.send(embed=emby)



class Help(commands.Cog):

    def __init__(self, client):
        attributes = {
        'name': "help",
        'cooldown': commands.Cooldown(1, 10.0, commands.BucketType.user)
        }
        self.client = client
        self.client.original_help = self.client.help_command
        self.client.help_command = HelpUwU(command_attrs=attributes)
    def cog_unload(self):
        self.client.help_command = commands.DefaultHelpCommand()
def setup(client):
    client.add_cog(Help(client))
