import datetime
import json
from logger import logger
import discord
from discord.ext import commands
from discord.ext.buttons import Paginator
import uuid


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 0):
        if limit < 301:
            if limit > 0:
                await ctx.channel.purge(limit=limit + 1)
                embed = discord.Embed(
                    title="Purge Command",
                    description=f'Purged {limit} message(s)',
                    colour=discord.Colour.red()
                )
                embed.set_footer(icon_url=ctx.author.avatar.url, text=f'Requested by: {ctx.message.author.name}')
                await ctx.send(embed=embed)
            else:
                await ctx.reply('ah yes purge nothing')
        else:
            await ctx.reply('Max to purge is `300`')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.author.id != 742976057761726514:
            if member != None:
                if ctx.author.top_role > member.top_role:
                    embed = discord.Embed(
                        title=f'You were banned from {ctx.guild.name}',
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
                    await ctx.reply('**role hierarchy moment**')
            else:
                await ctx.send('http://bit.ly/launchpadbanappeal')
        else:
            await ctx.send('Nah mate you have banned too many people by accident')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        embed = discord.Embed(
            title=f'You were kicked from {ctx.guild.name}',
            description=f'Reason:\n{reason}',
            colour=discord.Colour.red()
        )
        if member != None:
            if ctx.author.top_role > member.top_role:
                try:
                    await member.send(embed=embed)
                    await ctx.guild.kick(member, reason=reason)
                    await ctx.send(f'**{ctx.author} Kicked {member}**')
                except discord.Forbidden:
                    await ctx.reply('their role is above mine')
            else:
                await ctx.reply('**role hierarchy moment**')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role > member.top_role:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="🔇 Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="🔇 Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                                  read_message_history=True, read_messages=False)
            eh = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.red())
            eh.add_field(name="reason:", value=reason, inline=False)
            await ctx.send(embed=eh)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(f" you have been muted from: {guild.name} reason: {reason}")
        else:
            await ctx.send('**role hierarchy moment**')

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="🔇 Muted")

        await member.remove_roles(mutedRole)
        he = discord.Embed(title="unmute", description=f" unmuted {member.mention}", colour=discord.Colour.blurple())
        await ctx.send(embed=he)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        # If no member is specified.
        if member is None:
            await ctx.send("Next time, actually get me a member to warn.")
            return
        # If no reason is specified.
        if reason is None:
            await ctx.send("What did you want to warn that guy for?")
            return
        if ctx.author.top_role > member.top_role:
            with open('warns.json', 'r+') as f:
                warns = json.loads(f.read())

                # Test if the user has been warned before, if not, create their entry.
                try:
                    warns[str(member.id)]
                except KeyError:
                    warns[str(member.id)] = {}

                # Log warning to file.
                warns[str(member.id)][str(uuid.uuid1())] = {
                    "reason": reason,
                    "moderator": str(ctx.author),
                    "time": int(datetime.datetime.utcnow().timestamp())
                }

                # Better save this now.
                f.seek(0)
                f.write(json.dumps(warns))
                f.truncate()

            # Build Embed to send to member's DM
            embed = discord.Embed(
                title=f"You have been warned at {ctx.guild.name}",
                description=f"Reason: {reason}",
                colour=discord.Colour.red(),
            )

            # Send it.
            try:
                await member.send(embed=embed)
            except discord.Forbidden:  # Man, they got their DMs off.
                pass
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min((warncount := len(warns[str(member.id)])) % 10, 4)]
            if 11 <= (warncount % 100) <= 13:
                suffix = 'th'
            await ctx.send(f"**{member}** has been warned. This is their **{str(warncount) + suffix}** warning.")
        else:
            await ctx.send("**role hierarchy moment**")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member = None):
        # We DO want a member.
        if member is None:
            await ctx.send("Whose warnings did you want to see again?")
            return

        with open('warns.json', 'r') as f:
            warns = json.loads(f.read())

        # Test if member had been warned before.
        try:
            warns[str(member.id)]
        except KeyError:
            await ctx.send("This member has not been warned before!")
            return

        # Get warnings and build embed
        embed = discord.Embed(title=f"Warnings against {member}", colour=discord.Colour.dark_blue())

        # Setup paginator
        paginator = Pag(
            title=f"Warnings against {member}",
            colour=discord.Colour.dark_blue(),
            entries=[f"There are {len(warns[str(member.id)])} warning(s) logged against this user.\n"] +
                    [f"**{i + 1} - {warns[str(member.id)][key]['reason']}**\n"
                     f"Warning ID: {key} | Moderator: {warns[str(member.id)][key]['moderator']} "
                     f"| Warned at <t:{warns[str(member.id)][key]['time']}:F>\n" for i, key in
                     enumerate(warns[str(member.id)])],
            timeout=120
        )

        # Start paginator
        await paginator.start(ctx)

    @commands.command(aliases=["delwarn"])
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx, warn_id: str = None):
        # We need a warn ID.
        if warn_id is None:
            await ctx.send("Man, I need a warning ID.")
            return

        with open('warns.json', 'r+') as f:
            warns = json.loads(f.read())

            # Definitely not the most elegant method.
            for member in warns:
                if warn_id in warns[member].keys():
                    # Man, MemberCacheFlags weren't enabled?
                    member = await ctx.guild.fetch_member(member)
                    if ctx.author.top_role > member.top_role:
                        warns[member].pop(warn_id)
                        await ctx.send(
                            f"Warning with ID {warn_id} logged against **{member}** has been revoked.")
                        f.seek(0)
                        f.write(json.dumps(warns))
                        f.truncate()
                    else:
                        await ctx.send("**role hierarchy moment**")
                    break

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def clearwarns(self, ctx, member: discord.Member = None):
        # We DO want a member.
        if member is None:
            await ctx.send("Whose warnings did you want to clear?")
            return

        if ctx.author.top_role > member.top_role:
            with open('warns.json', 'r+') as f:
                warns = json.loads(f.read())

                # Test if member had been warned before.
                try:
                    warns[str(member.id)]
                except KeyError:
                    await ctx.send("This member has not been warned before!")
                    return

                warns[str(member.id)] = {}
                f.seek(0)
                f.write(json.dumps(warns))
                f.truncate()
                await ctx.send(f"All warnings against **{member}** have been revoked.")
        else:
            await ctx.send("**role hierarchy moment**")


class Pag(Paginator):  # from discord.ext.buttons import Paginator
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


def setup(client):
    client.add_cog(Moderation(client))
