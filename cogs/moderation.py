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



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role > member.top_role:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="🔇 Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="🔇 Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            eh = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.red())
            eh.add_field(name="reason:", value=reason, inline=False)
            await ctx.send(embed=eh)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(f" you have been muted from: {guild.name} reason: {reason}")
        else:
            await ctx.send('**role hierachy moment**')

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="🔇 Muted")

        await member.remove_roles(mutedRole)
        he = discord.Embed(title="unmute", description=f" unmuted {member.mention}",colour=discord.Colour.blurple())
        await ctx.send(embed=he)
def setup(client):
    client.add_cog(Moderation(client))
