import discord
from discord.ext import commands

import slash_utils as s


class Slash(s.ApplicationCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.bot  # we do mass amounts of trolling

    @s.user_command(guild_id=841890589640359946)
    async def userinfo(self, ctx: s.Context, member):
        mention = [r.mention.replace(f"<@&{ctx.guild.id}>", "@everyone") for r in reversed(member.roles)]
        memberRole = ", ".join(mention)                                          # noqa # we do a bit of trolling by disabling pycharm lint
        joinDate = member.joined_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")       # noqa # we do a bit of trolling by disabling pycharm lint
        creationDate = member.created_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")  # noqa # we do a bit of trolling by disabling pycharm lint
        memberIcon = member.display_avatar                                       # noqa # we do a bit of trolling by disabling pycharm lint
        embed = discord.Embed(                                                   # noqa # we do a bit of trolling by disabling pycharm lint
            title=f'{member.name}#{member.discriminator}',
            description=f'ID: {member.id}',
            colour=member.colour
        )
        embed.add_field(name="Join Date", value=joinDate)
        embed.add_field(name="Creation Date", value=creationDate, inline=True)
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name="Roles", value=memberRole)
        embed.set_thumbnail(url=memberIcon)
        await ctx.send(embed=embed, ephemeral=True)

    @s.user_command(guild_id=841890589640359946)
    async def scam(self, ctx: s.Context, member):
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.send("You do not have permission to ban members.")
        reason = "Nitro/Steam Scam; Your account may be hacked, please change your password. You may rejoin at https://discord.gg/S8waxK7QXd after securing your account." # noqa
        embed = discord.Embed(
            title=f'You were kicked from {ctx.guild.name}',
            description=f'Reason:\n{reason}',
            colour=discord.Colour.red()
        )
        if ctx.author.top_role > member.top_role:
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass
            await ctx.guild.ban(member, reason=reason)
            await ctx.guild.unban(discord.Object(id=member.id))
            await ctx.send(f'**{ctx.author}** Slapped **{member}** out of the server\n(dont forget the censoring too)')
        else:
            await ctx.reply('**role hierarchy moment**')



def setup(client):
    client.add_cog(Slash(client))