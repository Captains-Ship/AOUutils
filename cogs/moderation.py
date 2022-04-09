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
from utility.utils import DurationConverter, DurationTransformer, Duration


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx):  # rip bots=True
        await sleep(0.5)
        await ctx.channel.purge(limit=15, check=lambda m: m.author.bot)

    @app_commands.command(name="clean", description="Remove messages sent by bot in the current channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.guilds(config.slash_guild)
    async def clean_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await sleep(0.5)
        await interaction.response.send_message(
            f"Cleared {len(await (self.client.get_channel(interaction.channel_id)).purge(limit=15, check=lambda m: m.author.bot))} messages.")

    @commands.command(description='Purges messages from the current channel.',
                      usage='<amount>\n`amount`: The number of messages to be purged. This is a required argument and must be an integer.')
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
                embed.set_footer(icon_url=ctx.author.display_avatar.url,
                                 text=f'Requested by: {ctx.message.author.name}')
                await ctx.send(embed=embed)
            else:
                await ctx.reply('ah yes purge nothing')
        else:
            await ctx.reply('Max to purge is `300`')

    @app_commands.command(name="purge", description="Purges messages from current channel")
    @app_commands.describe(limit="The number of messages to be purged")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.guilds(config.slash_guild)
    async def purge_slash(self, interaction: discord.Interaction, limit: app_commands.Range[int, 1, 300]):
        await interaction.response.defer()
        deleted = await self.client.get_channel(interaction.channel_id).purge(
            limit=limit)  # No need for +1; no message is sent.
        embed = discord.Embed(
            title="Purge Command",
            description=f'Purged {len(deleted)} message(s)',
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=interaction.user.display_avatar.url,
                         text=f'Requested by: {interaction.user.name}')
        await interaction.response.send_message(embed=embed)

    @commands.command(description="Bans a specified user.",
                      usage="<user> [duration] [reason]\n`user`: The user to be banned. This is a required argument and can either be a mention or a user ID.\n`duration`: The duration for which the user should be banned. This is an optional argument.\n`reason`: The reason why the user is getting banned. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, duration: typing.Optional[DurationConverter] = -1, *,
                  reason=None):
        if ctx.author.id != 742976057761726514:
            if member != None:
                if ctx.author.top_role > member.top_role:
                    embed = discord.Embed(
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
                        await ctx.send('above my top role, cant ban')
                else:
                    await ctx.reply('**role hierarchy moment**')
            else:
                await ctx.send('http://bit.ly/launchpadbanappeal')
        else:
            await ctx.send('Nah mate you have banned too many people by accident')

    @app_commands.command(name="ban", description="Bans a specified user.")
    @app_commands.describe(member="The user to be banned.", duration="The duration for which the user is getting banned", reason="The reason why the user is getting banned.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.guilds(config.slash_guild)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member,
                        duration: app_commands.Transform[typing.Union[Duration, int], DurationTransformer] = -1,
                        reason: str = "No reason provided."):
        await interaction.response.defer()
        if interaction.user.id == 742976057761726514:
            return await interaction.response.send_message("Nah mate you have banned too many people by accident")
        if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
            embed = discord.Embed(
                title=f'You were banned from {interaction.guild.name}',
                description=f'Reason:\n{reason}' if reason is not None else "** **",
                colour=discord.Colour.red()
            )
            embed.add_field(name='Appeal At:', value='http://bit.ly/launchpadbanappeal')
            try:
                await member.send(embed=embed)
            except:
                pass
            try:
                await interaction.guild.ban(member, reason=reason)
                await interaction.response.send_message(f'**{interaction.user}** Yeeted **{member}' + (
                    f" for {str(duration)}.**" if int(duration) > 0 else "**"))
                if (duration := int(duration)) > 0:
                    await asyncio.sleep(duration)
                    await interaction.guild.unban(discord.Object(id=member.id), reason="Tempban has expired!")
                    try:
                        await member.send(f'You have been unbanned from {interaction.guild.name}')
                    except discord.Forbidden:
                        pass
            except discord.Forbidden:
                await interaction.response.send_message('above my top role, cant ban')
        else:
            await interaction.response.send_message('**role hierarchy moment**')

    @commands.command(description="Kicks a specified user.",
                      usage="<user> [reason]\n`user`: The user to be kicked. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting kicked. This is an optional argument.")
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
                except:
                    pass
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f'**{ctx.author}** Slapped **{member}** out of the server')
            else:
                await ctx.reply('**role hierarchy moment**')
        else:
            await ctx.reply("You need to specify a user to kick.")

    @app_commands.command(name="kick", description="Kicks a specified user.")
    @app_commands.describe(member="The user to be kicked.", reason="The reason why the user is getting kicked.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.guilds(config.slash_guild)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        await interaction.response.defer()
        if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
            embed = discord.Embed(
                title=f'You were kicked from {interaction.guild.name}',
                description=f'Reason:\n{reason}',
                colour=discord.Colour.red()
            )
            embed.add_field(name='Appeal At:', value='http://bit.ly/launchpadkickappeal')
            try:
                await member.send(embed=embed)
            except:
                pass
            await interaction.guild.kick(member, reason=reason)
            await interaction.response.send_message(f'**{interaction.user}** Slapped **{member}' + (
                f".**" if reason is not None else "**"))
        else:
            await interaction.response.send_message('**role hierarchy moment**')

    @commands.command(description="Kicks a specified user and deletes their messages.",
                      usage="<user> [reason]\n`user`: The user to be silenced. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting silenced. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member = None, *, reason=None):
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
                await ctx.reply('**role hierarchy moment**')
        else:
            await ctx.reply("You need to specify a user to softban.")

    @app_commands.command(name="softban", description="Kicks a specified user and deletes their messages.")
    @app_commands.describe(member="The user to be softbanned.", reason="The reason why the user is getting softbanned.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.guilds(config.slash_guild)
    async def softban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        await interaction.response.defer()
        embed = discord.Embed(
            title=f'You were kicked from {interaction.guild.name}',
            description=f'Reason:\n{reason}',
            colour=discord.Colour.red()
        )
        if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass
            await interaction.guild.ban(member, reason=reason)
            await interaction.guild.unban(discord.Object(id=member.id))
            await interaction.response.send_message(f'**{interaction.user}** Slapped **{member}' + (
                f".**" if reason is not None else "**"))
        else:
            await interaction.response.send_message('**role hierarchy moment**')

    @commands.command(description="Unbans a specified user",
                      usage="<user> [reason]\n`user`: The user to be unbanned. This is a required argument and has to be a user ID.\n \
    `reason`: The reason why the user is getting unbanned. This is an optional argument.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id=None, *, reason=None):
        if id != None:
            u = discord.Object(id=id)
            try:
                await ctx.guild.unban(u)
            except discord.NotFound:
                return await ctx.reply("Member isn't banned!")
            await ctx.send(f'**{ctx.author}** unbanned **{await self.client.fetch_user(id)}**')
        else:
            await ctx.send("nice member :)")

    @app_commands.command(name="unban", description="Unbans a specified user")
    @app_commands.describe(id="The user to be unbanned.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.guilds(config.slash_guild)
    async def unban_slash(self, interaction: discord.Interaction, user_id: int):
        await interaction.response.defer()
        u = discord.Object(id=user_id)
        try:
            await interaction.guild.unban(u)
        except discord.NotFound:
            return await interaction.response.send_message("Member isn't banned or you may have passed an invalid ID!")
        await interaction.response.send_message(f'**{interaction.user}** unbanned **{await self.client.fetch_user(user_id)}**')

    @commands.command(description="Mutes a specified user.",
                      usage="<user> [duration] [reason]\n`user`: The user to be muted. This is a required argument and can either be a mention or a user ID.\n`duration`: The duration for which the user should be muted. This is an optional argument. \n`reason`: The reason why the user is getting muted. This is an optional argument.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, duration: typing.Optional[DurationConverter] = -1, *,
                   reason=None):
        if member is None:
            return await ctx.send("Please specify a member to mute.")
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
            await ctx.send('**role hierarchy moment**')

    @app_commands.command(name="mute", description="Mutes a specified user.")
    @app_commands.describe(id="The user to be muted.", duration="The duration for which the user should be muted.", reason="The reason why the user is getting muted.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True, moderate_members=True)
    @app_commands.guilds(config.slash_guild)
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, duration: app_commands.Transform[typing.Union[Duration, int], DurationTransformer] = None, reason: str = "No reason provided."):
        await interaction.response.defer()
        guild = interaction.guild
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
        await interaction.response.send_message(embed=eh)
        if int(duration) < 2419300 and int(duration) > -0:
            await member.timeout(datetime.timedelta(seconds=int(duration)), reason=reason)
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


    @commands.command(description="Unmutes a specified user.",
                      usage="<user>\n`user`: The user to be unmuted. This is a required argument and can either be a mention or a user ID.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("Please specify a member to unmute.")
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

    @app_commands.command(name="unmute", description="Unmutes a specified user.")
    @app_commands.describe(id="The user to be unmuted.", reason="The reason why the user is getting unmuted.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True, moderate_members=True)
    @app_commands.guilds(config.slash_guild)
    async def unmute_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        await interaction.response.defer()
        guild = interaction.guild
        mutedRole = discord.utils.get(guild.roles, name="🔇 Muted")
        await member.timeout(None, reason=reason)
        try:
            await member.remove_roles(mutedRole)
        except:
            pass
        he = discord.Embed(title="unmute", description=f"{interaction.user} unsilenced {member.mention}",
                           colour=discord.Colour.blurple())
        await interaction.response.send_message(embed=he)

    @commands.command(description="Warns the specified user.",
                      usage="<user> <reason>\n`user`: The user to be warned. This is a required argument and can either be a mention or a user ID.\n`reason`: The reason why the user is getting warned. This is a required argument.")
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

    @app_commands.command(name="warn", description="Warns the specified user.")
    @app_commands.describe(id="The user to be warned.", reason="The reason why the user is getting warned.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.guilds(config.slash_guild)
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
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
                    "moderator": str(interaction.user),
                    "time": int(datetime.datetime.utcnow().timestamp())
                }

                # Better save this now.
                f.seek(0)
                f.write(json.dumps(warns))
                f.truncate()

            # Build Embed to send to member's DM
            embed = discord.Embed(
                title=f"You have been warned at {interaction.guild.name}",
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
            await interaction.response.send_message(f"**{member}** has been warned. This is their **{str(warncount) + suffix}** warning.")
        else:
            await interaction.response.send_message("**role hierarchy moment**")

    @commands.command(description="Shows the warnings against a user.",
                      usage="<user>\n`user`: The user to view the warnings of. This is a required argument and can either be a mention or a user ID.")
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
        paginator = Paginator(
            ctx,
            title=f"Warnings against {member}",
            pages=[f"There are {len(warns[str(member.id)])} warning(s) logged against this user.\n"] +
                  [f"**{i + 1} - {warns[str(member.id)][key]['reason']}**\n"
                   f"Warning ID: {key} | Moderator: {warns[str(member.id)][key]['moderator']} "
                   f"| Warned at <t:{warns[str(member.id)][key]['time']}:F>\n" for i, key in
                   enumerate(warns[str(member.id)])],
            timeout=120
        )

        # Start paginator
        await paginator.start()

    @app_commands.command(name="warnings", description="Shows the warnings against a user.")
    @app_commands.describe(member="The user to view the warnings of.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.guilds(config.slash_guild)
    async def warnings_slash(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        with open('warns.json', 'r') as f:
            warns = json.loads(f.read())

        # Test if member had been warned before.
        try:
            warns[str(member.id)]
        except KeyError:
            await interaction.response.send_message("This member has not been warned before!")
            return

        # Get warnings and build embed
        embed = discord.Embed(title=f"Warnings against {member}", colour=discord.Colour.dark_blue())

        # Setup paginator
        paginator = Paginator(
            interaction=interaction,
            title=f"Warnings against {member}",
            pages=[f"There are {len(warns[str(member.id)])} warning(s) logged against this user.\n"] +
                  [f"**{i + 1} - {warns[str(member.id)][key]['reason']}**\n"
                   f"Warning ID: {key} | Moderator: {warns[str(member.id)][key]['moderator']} "
                   f"| Warned at <t:{warns[str(member.id)][key]['time']}:F>\n" for i, key in
                   enumerate(warns[str(member.id)])],
            timeout=120
        )

        # Start paginator
        await paginator.start()

    @commands.command(aliases=["delwarn"], description="Deletes a warning against a user.",
                      usage="<warning id>\n`warning id`: The ID of the warning to delete. This is a required argument and must be a warning ID.")
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
                    try:
                        member = await ctx.guild.fetch_member(int(member))
                    except discord.NotFound:
                        await ctx.send("This person is no longer in this server!")
                        return
                    if ctx.author.top_role > member.top_role:
                        warns[str(member.id)].pop(warn_id)
                        await ctx.send(
                            f"Warning with ID {warn_id} logged against **{member}** has been revoked.")
                        f.seek(0)
                        f.write(json.dumps(warns))
                        f.truncate()
                        return
                    else:
                        await ctx.send("**role hierarchy moment**")
                        return
            await ctx.send("That warning ID doesn't exist!")

    @app_commands.command(name="delwarn", description="Deletes a warning against a user.")
    @app_commands.describe(warn_id="The ID of the warning to delete. This is a required argument and must be a warning ID.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.guilds(config.slash_guild)
    async def removewarn_slash(self, interaction: discord.Interaction, warn_id: str):
        await interaction.response.defer()
        with open('warns.json', 'r+') as f:
            warns = json.loads(f.read())

            # Definitely not the most elegant method.
            for member in warns:
                if warn_id in warns[member].keys():
                    try:
                        member = await interaction.guild.fetch_member(int(member))
                    except discord.NotFound:
                        await interaction.response.send_message("This person is no longer in this server!")
                        return
                    if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
                        warns[str(member.id)].pop(warn_id)
                        await interaction.response.send_message(
                            f"Warning with ID {warn_id} logged against **{member}** has been revoked.")
                        f.seek(0)
                        f.write(json.dumps(warns))
                        f.truncate()
                        return
                    else:
                        await interaction.response.send_message("**role hierarchy moment**")
                        return
            await interaction.response.send_message("That warning ID doesn't exist!")

    @commands.command(description="Removes all warnings against a user.",
                      usage="<user>\n`user`: The user to remove all warnings from. This is a required argument and can either be a mention or a user ID.")
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

    @app_commands.command(name="clearwarns", description="Removes all warnings against a user.")
    @app_commands.describe(member="The user to remove all warnings from. This is a required argument and can either be a mention or a user ID.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.guilds(config.slash_guild)
    async def clearwarns_slash(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        if interaction.guild.get_member(interaction.user.id).top_role > member.top_role:
            with open('warns.json', 'r+') as f:
                warns = json.loads(f.read())

                # Test if member had been warned before.
                try:
                    warns[str(member.id)]
                except KeyError:
                    await interaction.response.send_message("This member has not been warned before!")
                    return

                warns[str(member.id)] = {}
                f.seek(0)
                f.write(json.dumps(warns))
                f.truncate()
                await interaction.response.send_message(f"All warnings against **{member}** have been revoked.")
        else:
            await interaction.response.send_message("**role hierarchy moment**")


async def setup(client):
    await client.add_cog(Moderation(client))
