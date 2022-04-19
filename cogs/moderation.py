import asyncio
import datetime
import json
import typing
import uuid
from asyncio import sleep

import discord
from discord import app_commands
from discord.ext import commands

import config
from utility.paginators import ButtonPaginator as Paginator
from utility.utils import DurationConverter, DurationTransformer, Duration, Response


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx):  # rip bots=True
        await sleep(0.5)
        await ctx.channel.purge(limit=15, check=lambda m: m.author.bot)

    @app_commands.command(name="clean", description="Remove messages sent by bots in the current channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.guilds(config.slash_guild)
    async def clean_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await sleep(0.5)
        await interaction.followup.send(
            f"Cleared {len(await (self.client.get_channel(interaction.channel_id)).purge(limit=15, check=lambda m: m.author.bot))} messages.")

    @commands.command(description='Purges messages from the current channel.',
                      usage='<amount>\n`amount`: The number of messages to be purged. This is a required argument and must be an integer.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 0):
        resp = Response(ctx.locale)
        if limit < 301:
            if limit > 0:
                await ctx.channel.purge(limit=limit + 1)
                embed = discord.Embed(
                    title=resp.purge_cmd,
                    description=resp.purged.format(limit),
                    colour=discord.Colour.red()
                )
                embed.set_footer(icon_url=ctx.author.display_avatar.url,
                                 text=resp.req_by.format(ctx.author.name))
                await ctx.send(embed=embed)
            else:
                await ctx.reply(resp.purge_none)
        else:
            await ctx.reply(resp.max_purge)

    @commands.command(description="Bans a specified user.",
                      usage="<user> [duration] [reason]\n`user`: The user to be banned. This is a required argument and can either be a mention or a user ID.\n`duration`: The duration for which the user should be banned. This is an optional argument.\n`reason`: The reason why the user is getting banned. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, duration: typing.Optional[DurationConverter] = -1, *,
                  reason=None):
        resp = Response(ctx.locale)
        if ctx.author.id != 742976057761726514:
            if member != None:
                if ctx.author.top_role > member.top_role:
                    embed = discord.Embed(
                        # since this isn't for the invoker, we dont need to translate this
                        title=f'You were banned from {ctx.guild.name}',
                        description=f'Reason:\n{reason}' if reason is not None else "** **",
                        colour=discord.Colour.red()
                    )
                    embed.add_field(name='Appeal At:', value='http://bit.ly/launchpadbanappeal')
                    try:
                        await member.send(embed=embed)
                    except:
                        pass
                    try:
                        await ctx.guild.ban(member, reason=reason)
                        # same here, we dont need to translate this, since this isn't specifically for
                        # the invoker of the command
                        await ctx.send(f'**{ctx.author}** Yeeted **{member}' + (
                            f" for {str(duration)}.**" if int(duration) > 0 else "**"))
                        if (duration := int(duration)) > 0:
                            await asyncio.sleep(duration)
                            await ctx.guild.unban(discord.Object(id=member.id), reason="Tempban has expired!")
                            try:
                                await member.send(f'You have been unbanned from {ctx.guild.name}')
                            except discord.Forbidden:
                                pass
                    except discord.Forbidden:
                        await ctx.send(resp.bot_cant_ban)
                else:
                    await ctx.reply(resp.role_hierachy)
            else:
                await ctx.send('http://bit.ly/launchpadbanappeal')
        else:
            # for toasty, we dont need to translate this, since no ban perms for toasty anymore
            # lazy 100
            await ctx.send('Nah mate you have banned too many people by accident')

    @commands.command(description="Kicks a specified user.",
                      usage="<user> [reason]\n`user`: The user to be kicked. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting kicked. This is an optional argument.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        resp = Response(ctx.locale)
        embed = discord.Embed(
            title=f'You were kicked from {ctx.guild.name}',
            description=f'Reason:\n{reason}',
            colour=discord.Colour.red()
        )
        if member != None:
            if ctx.author.top_role > member.top_role:
                try:
                    await member.send(embed=embed)
                except:
                    pass
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f'**{ctx.author}** Slapped **{member}** out of the server')
            else:
                await ctx.reply(resp.role_hierachy)
        else:
            await ctx.reply(resp.kick_none)

    @commands.command(description="Kicks a specified user and deletes their messages.",
                      usage="<user> [reason]\n`user`: The user to be silenced. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting silenced. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member = None, *, reason=None):
        resp = Response(ctx.locale)
        embed = discord.Embed(
            title=f'You were kicked from {ctx.guild.name}',
            description=f'Reason:\n{reason}',
            colour=discord.Colour.red()
        )
        if member != None:
            if ctx.author.top_role > member.top_role:
                try:
                    await member.send(embed=embed)
                except discord.Forbidden:
                    pass
                await ctx.guild.ban(member, reason=reason)
                await ctx.guild.unban(discord.Object(id=member.id))
                await ctx.send(
                    f'**{ctx.author}** Slapped **{member}** out of the server\n(dont forget the censoring too)')
            else:
                await ctx.reply(resp.role_hierachy)
        else:
            # shouldn' cause any confusion, also lazy 100
            await ctx.reply(resp.kick_none)

    @commands.command(description="Unbans a specified user",
                      usage="<user> [reason]\n`user`: The user to be unbanned. This is a required argument and has to be a user ID.\n \
    `reason`: The reason why the user is getting unbanned. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id=None, *, reason=None):
        resp = Response(ctx.locale)
        if id != None:
            u = discord.Object(id=id)
            try:
                await ctx.guild.unban(u)
            except discord.NotFound:
                return await ctx.reply(resp.member_not_banned)
            await ctx.send(f'**{ctx.author}** unbanned **{await self.client.fetch_user(id)}**')
        else:
            await ctx.send(resp.missing_member)

    @commands.command(description="Mutes a specified user.",
                      usage="<user> [duration] [reason]\n`user`: The user to be muted. This is a required argument and can either be a mention or a user ID.\n`duration`: The duration for which the user should be muted. This is an optional argument. \n`reason`: The reason why the user is getting muted. This is an optional argument.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, duration: typing.Optional[DurationConverter] = -1, *,
                   reason=None):
        resp = Response(ctx.locale)
        if member is None:
            return await ctx.send(resp.missing_member)
        if ctx.author.top_role > member.top_role:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="🔇 Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="🔇 Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                                  read_message_history=True, read_messages=False)
            eh = discord.Embed(title="Muted", description=f"{member.mention} was silenced" + (
                f" for {str(duration)}." if int(duration) > 0 else ""), colour=discord.Colour.red())
            if reason is not None:
                eh.add_field(name="Reason:", value=reason, inline=False)
            await ctx.send(embed=eh)
            if int(duration) < 2419300 and int(duration) > -0:
                await member.timeout(until=datetime.timedelta(seconds=int(duration)))
                await member.send(
                    f"You have been muted in {guild.name}" + (f" for reason: {reason}" if reason is not None else ""))
            else:
                await member.add_roles(mutedRole, reason=reason)
                if (duration := int(duration)) > 0:
                    await asyncio.sleep(duration)
                    try:
                        await member.remove_roles(mutedRole, reason="Tempmute has expired!")
                        await member.send(f"You have been unmuted in {guild.name}")
                    except discord.NotFound:  # Poor guy left the scene.
                        pass
        else:
            await ctx.send(resp.role_hierachy)

    @commands.command(description="Unmutes a specified user.",
                      usage="<user>\n`user`: The user to be unmuted. This is a required argument and can either be a mention or a user ID.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send(resp.missing_member)
        mutedRole = discord.utils.get(ctx.guild.roles, name="🔇 Muted")
        await self.client.http.edit_member(ctx.guild.id, member.id,
                                           communication_disabled_until=datetime.datetime.utcnow().isoformat())
        try:
            await member.remove_roles(mutedRole)
        except:
            pass
        he = discord.Embed(title="unmute", description=f"{ctx.author} unsilenced {member.mention}",
                           colour=discord.Colour.blurple())
        await ctx.send(embed=he)

    @commands.command(description="Warns the specified user.",
                      usage="<user> <reason>\n`user`: The user to be warned. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting warned. This is a required argument.")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        resp = Response(ctx.locale)
        # If no member is specified.
        reason = reason or "No reason specified."
        if member is None:
            await ctx.send(resp.missing_member)
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
            await ctx.send(resp.role_hierachy)

    @commands.command(description="Shows the warnings against a user.",
                      usage="<user>\n`user`: The user to view the warnings of. This is a required argument and can either be a mention or a user ID.")
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member):
        resp = Response(ctx.locale)
        # We DO want a member.
        if member is None:
            await ctx.send(resp.missing_member)
            return

        with open('warns.json', 'r') as f:
            warns = json.loads(f.read())

        # Test if member had been warned before.
        try:
            warns[str(member.id)]
        except KeyError:
            await ctx.send(resp.member_not_warned)
            return

        # Get warnings and build embed
        embed = discord.Embed(title=f"Warnings against {member}", colour=discord.Colour.dark_blue())

        # Moved from discord.ext.buttons to Cap's paginator
        entries = [f"There are {len(warns[str(member.id)])} warning(s) logged against this user.\n"] + [f"**{i + 1} - {warns[str(member.id)][key]['reason']}**\n"
                f"Warning ID: {key} | Moderator: {warns[str(member.id)][key]['moderator']} "
                f"| Warned at <t:{warns[str(member.id)][key]['time']}:F>\n" for i, key in
                enumerate(warns[str(member.id)])]

        # Setup paginator
        paginator = Paginator(
            ctx,
            title=f"Warnings against {member}",
            pages=Paginator.entries_to_pages(entries),
            force_embed=True,
            timeout=120
        )

        # Start paginator
        await paginator.start()

    @commands.command(aliases=["delwarn"], description="Deletes a warning against a user.",
                      usage="<warning id>\n`warning id`: The ID of the warning to delete. This is a required argument and must be a warning ID.")
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx, warn_id: str):
        resp = Response(ctx.locale)
        # We need a warn ID.
        if warn_id is None:
            await ctx.send(resp.missing_id)
            return

        with open('warns.json', 'r+') as f:
            warns = json.loads(f.read())

            # Definitely not the most elegant method.
            for member in warns:
                if warn_id in warns[member].keys():
                    # Man, MemberCacheFlags weren't enabled?
                    try:
                        member = await ctx.guild.fetch_member(int(member))
                    except discord.NotFound:
                        await ctx.send(resp.member_gone)
                        return
                    if ctx.author.top_role > member.top_role:
                        warns[str(member.id)].pop(warn_id)
                        await ctx.send(
                            resp.warn_revoked.format(warn_id, str(member)))
                        f.seek(0)
                        f.write(json.dumps(warns))
                        f.truncate()
                        return
                    else:
                        await ctx.send(resp.role_hierachy)
                        return
            await ctx.send(resp.invalid_id)

    @commands.command(description="Removes all warnings against a user.",
                      usage="<user>\n`user`: The user to remove all warnings from. This is a required argument and can either be a mention or a user ID.")
    @commands.has_permissions(kick_members=True)
    async def clearwarns(self, ctx, member: discord.Member):
        resp = Response(ctx.locale)
        # We DO want a member.
        if member is None:
            await ctx.send(resp.missing_member)
            return

        if ctx.author.top_role > member.top_role:
            with open('warns.json', 'r+') as f:
                warns = json.loads(f.read())

                # Test if member had been warned before.
                try:
                    warns[str(member.id)]
                except KeyError:
                    await ctx.send(resp.member_not_warned)
                    return

                warns[str(member.id)] = {}
                f.seek(0)
                f.write(json.dumps(warns))
                f.truncate()
                await ctx.send(resp.warns_cleared.format(member))
        else:
            await ctx.send(resp.role_hierachy)

async def setup(client):
    await client.add_cog(Moderation(client))
