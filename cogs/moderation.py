import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int=0):
        if limit < 301:
            if limit > 0:
                await ctx.channel.purge(limit=limit + 1)
                embed = discord.Embed(
                    title="Purge Command",
                    description=f'Purged {limit} message(s)',
                    colour=discord.Colour.red()
                )
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by: {ctx.message.author.name}')
                await ctx.send(embed=embed)
            else:
                await ctx.reply('ah yes purge nothing')
        else:
            await ctx.reply('Max to purge is `300`')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
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
                try:
                    await ctx.guild.ban(member, reason=reason)
                    await ctx.send(f'**{ctx.author}** Banned **{member}**')
                except discord.Forbidden:
                    await ctx.send('above my top role, cant ban')
            else:
                await ctx.reply('**role hierachy moment**')
        else:
            await ctx.send('http://bit.ly/launchpadbanappeal')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if member != None:
            if ctx.author.top_role > member.top_role:
                try:
                    await member.send(embed=embed)
                except:
                    pass
                try:
                    await ctx.guild.kick(member, reason=reason)
                except commands.discordForbidden:
                    await ctx.reply('their role is above mine')
            else:
                await ctx.reply('**role hierachy moment**')
def setup(client):
    client.add_cog(Moderation(client))
