import datetime
from traceback import *

import crayons
import discord
from aiohttp import ClientSession as cs
from discord import app_commands
from discord.ext import commands

import config
from logger import logger
from utility.paginators import ButtonPaginator as Paginator
from utility.utils import database, Response


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.debug = False
        self.w = 794950846168432650
        self.og_on_error = None

    @commands.Cog.listener()
    async def on_ready(self):
        # tags database initialization
        self.client.tag_db = await database.init("tags")
        await self.client.tag_db.execute("CREATE TABLE IF NOT EXISTS tags (name, content, creator)")

        logger.info(f'Logged in as {self.client.user}. Good Morning.')

        startup_channel = self.client.get_channel(854333051852685333)
        await startup_channel.send('Bot is now up!')
        aou_guild = self.client.get_guild(794950428756410429)
        try:
            await self.client.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(type=discord.ActivityType.watching,
                                          name=f'AOU | {aou_guild.member_count} members')
            )
        except:  # noqa
            pass
            # The bot isn't in the AOU server, so we can't access the member count.
            # This is fine, we can just ignore it.

        async with cs() as ClientSession:
            URLs = await ClientSession.get(
                "https://raw.githubusercontent.com/xXBuilderBXx/DiscordScamBrowserFilter/main/filterlist.txt")
            URLsPlaintext = await URLs.text()
            UrlsArray = []
            for index, line in enumerate(URLsPlaintext.split("\n")):
                if index < 13:
                    continue
                UrlsArray.append(line.lstrip("||").split("^")[0])
        self.client.scams = UrlsArray

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f'AOU | {guild.member_count} members')
        )
        welcome = self.client.get_channel(self.w)
        embed = discord.Embed(
            title=f"Welcome, {member}!",
            description=f"{member.mention} has joined the server!\nWe are now at {member.guild.member_count} members.",
            color=0xFF0000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name="All Of Us", icon_url=member.guild.icon.url)
        await welcome.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f'AOU | {guild.member_count} members')
        )
        welcome = self.client.get_channel(self.w)
        embed = discord.Embed(
            title=f"Goodbye, {member} :(",
            description=f"{member.mention} has left the server.\nWe are now at {member.guild.member_count} members.",
            color=0xFF0000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name="All Of Us", icon_url=member.guild.icon.url)
        await welcome.send(embed=embed)

    # flags a message for steam scam
    # TODO: rewrite the entire flag system
    async def flag(self, message: discord.Message):
        _scam = False
        for scam in self.client.scams:
            if scam.lower() in message.content.lower():
                if scam == "":
                    continue
                _scam = True
                break

        if _scam:
            reason = "Scam; Your account may be hacked, please change your password. You may rejoin at <https://discord.gg/MCfSX48Wtd> after securing your account."
            channel = self.client.get_channel(853191467941494784)
            member = message.author
            embed = discord.Embed(
                title=f'Message Flagged for scam!',
                description=f'{member} ({member.id}) sent the following in {message.channel.mention}:\n```{message.content}```\n\nTo ban the user run the following command:\n```{message.guild.me.mention} softban {message.author.id} {reason}```',
                colour=discord.Colour.red()
            )
            await message.delete()
            await channel.send(f"aou ban {message.author.id} {reason}", embed=embed)
            await member.send(f'You have been automatically flagged for `scam` by the automod.')

    @commands.Cog.listener('on_message')
    async def keyword_listener(self, message):
        if message.author.bot:
            return
        keywords = [
            (["mobile", "aou"], "The AOU mod is not for mobile.")
        ]
        for kwords, response in keywords:
            send = True
            for word in kwords:
                if not word.lower() in message.content:
                    send = False
            if send:
                await message.reply(response)

        await self.flag(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        resp = Response(ctx.locale)

        if isinstance(error, commands.CommandInvokeError):
            error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in self.client.get_bot_devs():
                await ctx.reinvoke()
            else:
                if not ctx.author.guild_permissions.administrator:
                    timeleftins = error.retry_after
                    timeleftformat = str(datetime.timedelta(seconds=timeleftins))
                    timelol = timeleftformat.split(':')
                    s3 = timelol[2]
                    s2 = s3.split('.')
                    s = s2[0]
                    m = timelol[1]
                    await ctx.send(
                        resp.cooldown_min.format(m, s) if str(m) != "0" else resp.cooldown_sec.format(s))
                else:
                    if ctx.command.name.lower() != 'jishaku':
                        if str(ctx.command.cog).lower() != 'admin':
                            await ctx.reinvoke()

        elif isinstance(error, commands.CommandNotFound):
            h = ctx.invoked_with
            embed = discord.Embed(
                title=resp.unknown_command.format(h),
                description=resp.unknown_cmd_long.format(ctx.prefix),
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=self.client.user.display_avatar.url)
            await ctx.send(
                embed=embed
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'Missing permissions: {", ".join([perm.title().replace("_", " ") for perm in error.missing_permissions])}')
            
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(resp.unowner)

        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(resp.member_not_found)

        elif ctx.command.name.lower() == 'purge':
            if not isinstance(error, commands.MissingPermissions):
                await ctx.send(resp.not_int)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(resp.missing_arg.format(error.param))

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(resp.check_fail)

        elif isinstance(error, ValueError):
            print(error.args)
        else:
            # await ctx.reply(f'Error executing command! \n{error}\nYou should never receive this message. Contact Captain#3175 about this and he will hopefully add an error handler for that.')
            errorlog = self.client.get_channel(908402845383004171)
            e = discord.Embed(
                title="Error!",
                description=ctx.message.content,
                colour=discord.Colour.red()
            )
            e.add_field(name="error", value=error)
            await errorlog.send(embed=e)
            await ctx.reply(resp.unknown_error.format(str(error)))
            cmdlog = self.client.get_channel(896394252962123806)
            embed = discord.Embed(
                title="Error!",
                description=error,
                colour=discord.Colour.red()
            )
            embed.add_field(name="Content", value=ctx.message.content)
            e = error
            logger.error(f'An error was Caught!\n{crayons.white("".join(format_exception(e, e, e.__traceback__)))}')
            h = "".join(format_exception(e, e, e.__traceback__))
            if ctx.author.id not in self.client.get_bot_devs():
                return
            pager = Paginator(ctx, timeout=100, pages=[h[i: i + 2000] for i in range(0, len(h), 2000)],
                              prefix="AOUutils has encountered an Exception:```py\n", suffix="```")

            await pager.start()

    async def on_error(self, interaction: discord.Interaction,
                       error: app_commands.AppCommandError):
        
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                f'Missing permissions: {", ".join([perm.title().replace("_", " ") for perm in error.missing_permissions])}')
            
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                f'I am missing the following permissions: {", ".join([perm.title().replace("_", " ") for perm in error.missing_permissions])}')
            
        elif isinstance(error, app_commands.CommandNotFound):
            await interaction.response.send_message(
                f'This command may have been removed, you shouldn\'t be seeing this message again.')
            await self.client.tree.sync(guild=interaction.guild if interaction.guild else config.slash_guild)
        else:
            errorlog = self.client.get_channel(908402845383004171)
            e = discord.Embed(
                title="Error!",
                description=f"Interaction Data: ```py\n{interaction.data}\n```",
                colour=discord.Colour.red()
            )
            e.add_field(name="error", value=error)
            try:
                await errorlog.send(embed=e)
            except AttributeError:
                pass
            await interaction.response.send_message(f'Error, This has been reported to the developers!\n{error}')
            cmdlog = self.client.get_channel(896394252962123806)
            embed = discord.Embed(
                title="Error!",
                description=error,
                colour=discord.Colour.red()
            )
            embed.add_field(name="Interaction Data", value=f"```py\n{interaction.data}\n```")
            embed.add_field(name="Command", value=interaction.command.name)
            e = error
            logger.error(f'An error was Caught!\n{crayons.white("".join(format_exception(e, e, e.__traceback__)))}')
            h = "".join(format_exception(e, e, e.__traceback__))
            if interaction.user.id not in self.client.get_bot_devs():
                return
            pager = Paginator(interaction=interaction, timeout=100,
                              pages=[h[i: i + 2000] for i in range(0, len(h), 2000)],
                              prefix="AOUutils has encountered an Exception:```py\n", suffix="```")

            await pager.start()

    async def cog_load(self) -> None:
        self.og_on_error = self.client.tree.on_error
        self.client.tree.on_error = self.on_error

    async def cog_unload(self) -> None:
        self.client.tree.on_error = self.og_on_error


async def setup(client):
    await client.add_cog(Listener(client))
