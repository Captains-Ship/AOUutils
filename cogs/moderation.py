import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, *, text=" "):
        if text != ' ':
            await ctx.send(text)
        else:
            await ctx.reply('I cannot send nothing')


def setup(client):
    client.add_cog(Moderation(client))
