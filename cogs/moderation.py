import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit=None):
        if limit != None:
            if limit <= 300:
                if limit > 0:
                    await ctx.channel.purge(limit=limit)
                await ctx.reply('ah yes purge nothing')
            else:
                await ctx.reply('Max to purge is `300`')
        await ctx.reply('ah yes purge nothing')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *,  reason=None):
        if member != None:
            if ctx.author.top_role > member.top_role:
                embed = discord.Embed(
                    title='You were banned from All Of Us',
                    description=f'Reason:\n{reason}',
                    colour=discord.Colour.red()
                )
                embed.add_field(name='Appeal At:', value='http://bit.ly/launchpadbanappeal')
                try:
                    await member.send(embed=embed)
                except:
                    pass
                await ctx.guild.ban(member, reason=reason)
            else:
                await ctx.reply('role hierachy moment')
        else:
            await ctx.send('http://bit.ly/launchpadbanappeal')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if member != None:
            await member.send(f'You have been kicked from AOU for:\n{reason}')
            await ctx.guild.kick(member, reason=reason)
def setup(client):
    client.add_cog(Moderation(client))
