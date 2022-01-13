import discord

import slash_utils as s


class Slash(s.ApplicationCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.bot  # we do mass amounts of trolling

    @s.user_command(guild_id=841890589640359946)
    async def userinfo(self, ctx, member):
        mention = [r.mention.replace(f"<@&{ctx.guild.id}>", "@everyone") for r in reversed(member.roles)]
        memberRole = ", ".join(mention)
        joinDate = member.joined_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        creationDate = member.created_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        memberIcon = member.display_avatar
        embed = discord.Embed(
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


def setup(client):
    client.add_cog(Slash(client))