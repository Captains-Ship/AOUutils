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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, reason=None):
        if member != None:
            embed = discord.Embed(
                title='You were banned from All Of Us',
                description=f'Reason:\n{Reason}',
                colour=discord.Colour.red()
            )
            embed.add_field(name='Appeal At:', value='http://bit.ly/launchpadbanappeal')
            try:
                await member.send(embed=embed)
            except:
                pass
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send('http://bit.ly/launchpadbanappeal')

def setup(client):
    client.add_cog(Moderation(client))
