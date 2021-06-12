import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    """
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
        title='Help',
        description='Command List',
        colour=discord.Colour.red()
        )
        for command in self.client.commands:
            if command.cog_name != 'Tags':
               embed.add_field(name=command, value=command.help, inline=True)
        await ctx.send(embed=embed)
    """
    @commands.command(help='h')
    async def help(self, ctx, cmd=None):
        if cmd == None:
            embed=discord.Embed(
                title='help',
                colour=discord.Colour.red()
            )
            cmdlist = ""
            for command in self.client.commands:
                if command.cog_name != 'Tags':
                    cmdlist = cmdlist + ', ' + str(command)
            cmdlist = cmdlist.replace(', ', '\n')
            embed.add_field(name='Command List', value=cmdlist, inline=False)
            embed.add_field(name='And a bunch more tags', value='cant be bothered adding them here sorry', inline=False)
            await ctx.send(embed=embed)
        else:
            for command in self.client.commands:
                if cmd.lower() == str(command).lower():
                    embed = discord.Embed(
                        title=command,
                        description=command.help,
                        colour=discord.Colour.red()
                    )
                    await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Help(client))