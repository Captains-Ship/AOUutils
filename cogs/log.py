import discord
from discord.ext import commands


class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    def _gcm(self, command):
        return f"{command.qualified_name} {command.signature}"

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if not ctx.guild:
            return
        cmdlog = self.client.get_channel(896394252962123806)
        embed = discord.Embed(
            title=f"Command {ctx.command} Invoked!",
            description=ctx.message.content,
            colour=discord.Colour.green()
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await cmdlog.send(embed=embed)


def setup(client):
    client.add_cog(Log(client))