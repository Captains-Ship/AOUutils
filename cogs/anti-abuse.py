import datetime

import discord
from discord.ext import commands


class AntiAbuse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, b, a):
        if a.guild.id != 794950428756410429: return
        ch = self.client.get_channel(846389772166758432)
        br = b.roles
        ar = a.roles
        if b.roles != a.roles:
            if len(b.roles) > len(a.roles):
                async for entry in b.guild.audit_logs(
                        action=discord.AuditLogAction.member_role_update,
                        limit=1,
                        after=datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
                ):
                    if entry.user.id == a.id:
                        embed = discord.Embed(
                            title="Possible abuse detected!",
                            description=f"{a} removed {''.join([role.mention for role in br if role not in ar])} from themselves",
                            colour=discord.Colour.red()
                        )
                        await ch.send(embed=embed)
            elif len(b.roles) < len(a.roles):
                async for entry in a.guild.audit_logs(
                        action=discord.AuditLogAction.member_role_update,
                        limit=1,
                        after=datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
                ):
                    if entry.user.id == a.id:
                        embed = discord.Embed(
                            title="Possible abuse detected!",
                            description=f"{a} added {''.join([role.mention for role in ar if role not in br])} to themselves",
                            colour=discord.Colour.red()
                        )
                        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, c):
        if c.guild.id != 794950428756410429: return
        async for entry in c.guild.audit_logs(
                action=discord.AuditLogAction.channel_delete,
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        ):
            ch = self.client.get_channel(846389772166758432)
            embed = discord.Embed(
                title="A channel was deleted!",
                description=f"`{entry.user}` Deleted the channel `#{c}`",
                colour=discord.Colour.red()
            )
            await ch.send(embed=embed)  # dont forget to send it again stupidtain

    @commands.Cog.listener()
    async def on_guild_channel_create(self, c):
        if c.guild.id != 794950428756410429: return
        async for entry in c.guild.audit_logs(
                action=discord.AuditLogAction.channel_create,
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        ):
            ch = self.client.get_channel(846389772166758432)
            embed = discord.Embed(
                title="A channel was created!",
                description=f"`{entry.user}` Created the channel `#{c}` (link: {c.mention})",
                colour=discord.Colour.red()
            )
            await ch.send(embed=embed)  # dont forget to send it again stupidtain


    @commands.group()
    @commands.has_permissions(administrator=True)
    async def abuse(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            if ctx.message.content.rstrip(ctx.prefix + ctx.invoked_with) == "":
                description = [
                    "The Anti-Abuse module was rewritted from Captains [Anti-Abuse+](https://github.com/captains-ship/anti-abuse-plus) bot.",
                    "It logs stuff like people assigning roles to themselves, creating/deleting channels, bots added/removed etc.",
                    "if you think something isnt working, run `aou abuse heartbeat` for debugging."
                ]
                embed = discord.Embed(
                    title="Anti-Abuse",
                    description="\n".join(description),
                    color=discord.Colour.red()
                )
                await ctx.reply(embed=embed)
                return
            await ctx.reply("Unknown subcommand!")

    @abuse.command()
    async def heartbeat(self, ctx):
        embed = discord.Embed(
            title="Heartbeat"
        )
        ch = self.client.get_channel(846389772166758432)
        if ch is None:
            embed.add_field(name="/!\\ CRITICAL",
                            value="Your server is missing an anti-abuse logging channel, please create it now.")
            embed.colour = discord.Colour.red()

        if len(embed.fields) == 0:
            embed.add_field(name="all good!", value="no issues found!")
            embed.colour = discord.Colour.green()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AntiAbuse(client))
