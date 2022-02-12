from discord.ext import commands
import discord
import traceback
import datetime
from discord.ext.commands import *
import json
from traceback import *
import crayons
from logger import logger
from discord.ext.buttons import Paginator as pag
from utility.utils import database
import asyncio
from aiohttp import ClientSession as cs



class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.debug = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.tag_db = await database.init("tags")
        await self.client.tag_db.execute("CREATE TABLE IF NOT EXISTS tags (name, content, creator)")
        logger.info(f'Logged in as {self.client.user}. Good Morning.')
        chandler = self.client.get_channel(854333051852685333)
        await chandler.send('Bot is now up!')
        guild = self.client.get_guild(794950428756410429)
        try:
            await self.client.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(type=discord.ActivityType.watching,
                                          name=f'AOU | {guild.member_count} members')
            )
        except:  # noqa
            pass
            # The bot isn't in the AOU server, so we can't access the member count.
            # This is fine, we can just ignore it.
        await self.client.refreshHttp()

        async with cs() as c:
            x = await c.get("https://raw.githubusercontent.com/xXBuilderBXx/DiscordScamBrowserFilter/main/filterlist.txt")
            e = await x.text()
            b = []
            for index, line in enumerate(e.split("\n")):
                if index < 13:
                    continue
                b.append(line.lstrip("||").split("^")[0])
        self.scams = b

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f'AOU | {guild.member_count} members')
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f'AOU | {guild.member_count} members')
        )

    # flags a message for steam scam
    async def flag(self, message: discord.Message):
        _scam = False
        for scam in self.scams:
            if scam.lower() in message.content.lower():
                _scam = True
        
        if _scam:
            reason = "scam"
            channel = self.client.get_channel(868522732759949382)#853191467941494784)
            embed = discord.Embed(
                title=f'Message Flagged for {reason}!',
                description=f'{member} ({member.id}) sent the following in {message.channel.mention}:\n```{message.content}```\n\nTo ban the user run the following command:\n```aou ban {message.author.id} {reason}```',
                colour=discord.Colour.red()
            )
            await message.delete()
            await channel.send(f"aou ban {message.author.id} {reason}", embed=embed)
            await member.send(f'You have been automatically flagged for `{reason}` by the automod.')


    @commands.Cog.listener('on_message')
    async def on_message_two(self, message):
        if message.author.bot:
            return
        """
        if self.client.http.token in message.content:
            cap = self.client.get_user(347366054806159360)
            await cap.send('OH GOD OH FUCK RESET THE FUCKING TOKEN NOW ITS BEEN LEAKED')
            try:
                await message.delete()
            except:
                pass
        """
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply('The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')

        await self.flag(message, "Scam; Hacked account")

        """
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title='Error!',
                description='Command Not Found!',
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.reply(embed=embed)
        """

    # anti hoist
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        for member in guild.members:
            if member.display_name.startswith('.'):
                await member.edit(nick=member.display_name.replace('.', ''))
            elif member.display_name.startswith('\''):
                await member.edit(nick=member.display_name.replace('\'', ''))
            elif member.display_name.startswith('!'):
                await member.edit(nick=member.display_name.replace('!', ''))

    @commands.Cog.listener()
    async def on_member_update(self, b, a):
        member = a
        guild = member.guild
        if member.display_name.startswith('.'):
            await member.edit(nick=member.display_name.replace('.', ''))
        elif member.display_name.startswith('\''):
            await member.edit(nick=member.display_name.replace('\'', ''))
        elif member.display_name.startswith('!'):
            await member.edit(nick=member.display_name.replace('!', ''))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in self.client.get_bot_devs():
                await ctx.reinvoke()
            else:
                if not ctx.author.guild_permissions.administrator:
                    if ctx.command.name == 'work':
                        try:
                            with open('cur.json', 'r') as f:
                                jason = json.load(f)
                                if str(jason[str(ctx.author.id)]['wallet']) != '500':
                                    timeleftins = error.retry_after
                                    timeleftformat = str(datetime.timedelta(seconds=timeleftins))
                                    timelol = timeleftformat.split(':')
                                    s3 = timelol[2]
                                    s2 = s3.split('.')
                                    s = s2[0]
                                    m = timelol[1]
                                    if str(m) != "0":
                                        await ctx.send(
                                            f'This command is on cooldown. Please wait {m} minutes and {s} seconds.')
                                    else:
                                        await ctx.send(
                                            f'This command is on cooldown. Please wait {s} seconds.')

                                else:
                                    await ctx.reinvoke()
                        except:
                            await ctx.reply('You dont have an account! do `aou start`')
                    else:
                        timeleftins = error.retry_after
                        timeleftformat = str(datetime.timedelta(seconds=timeleftins))
                        timelol = timeleftformat.split(':')
                        s3 = timelol[2]
                        s2 = s3.split('.')
                        s = s2[0]
                        m = timelol[1]
                        await ctx.send(
                            f'Error 429: You are being ratelimited. \nTry in a few minutes.')  # Please wait {m} minutes and {s} seconds.')
                else:
                    if ctx.command.name.lower() != 'jishaku':
                        if str(ctx.command.cog).lower() != 'admin':
                            await ctx.reinvoke()
        elif isinstance(error, commands.CommandNotFound):
            h = ctx.invoked_with
            embed = discord.Embed(
                title=f'Unknown Command "{h}"',
                description=f'I do not recognize this command. run `{ctx.prefix}help` for a list of commands.',
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=self.client.user.display_avatar.url)
            await ctx.send(
                'Error!',
                embed=embed
            )
        elif isinstance(error, commands.MissingPermissions):
            if ctx.author.id == 347366054806159360:
                await ctx.reinvoke()
            else:
                if ctx.guild is None and ctx.command.name.lower() != 'jishaku' and ctx.command.cog_name.lower() != 'admin':
                    await ctx.reinvoke()
                else:
                    await ctx.send(f'Missing permissions: {", ".join([perm.title().replace("_", " ") for perm in error.missing_permissions])}')
        elif isinstance(error, commands.NotOwner):
            await ctx.reply('Unowner moment')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply('The member that you\'ve mentioned isn\'t in this server or does not exist.')
        elif ctx.command.name.lower() == 'purge':
            if not isinstance(error, MissingPermissions):
                await ctx.send('Nice integer Mate, next time gimmie a number')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'missing argument(s) `{error.param}`')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('You are probably not allowed to use this command.')
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
            await ctx.reply(f'Error, This has been reported to the developers!\n{error}')
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
            pager = discord.ext.buttons.Paginator(timeout=100, entries=[h[i: i + 2000] for i in range(0, len(h), 2000)], length=1,
                        prefix="AOUutils has encountered an Exception:```py\n", suffix="```")

            await pager.start(ctx)

    @commands.command()
    @commands.is_owner()
    async def debugger(self, ctx):
        self.client.debug = not self.client.debug
        await ctx.send(f"toggled debug to {self.client.debug}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logger.info("a member has joined AOU")
        if "h0nde" in member.name.lower() or "h0nda" in member.name.lower():
            chandler = member.guild.get_channel(852186132111556690)
            await chandler.send(f'{member.mention} has been banned due to the keyword "h0nde"')
            await member.send(
                'Hi! you have been removed from the server due to a keyword, if this was a mistake add Captain#3175')
            await member.guild.ban(member, reason='h o n d a')
        else:
            with open('memcount.json', 'r') as f:
                memcount = json.load(f)
                memcount['membercount'] = member.guild.member_count
            with open('memcount.json', 'w') as f:
                json.dump(memcount, f, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logger.info("A member has left AOU")
        with open('memcount.json', 'r') as f:
            memcount = json.load(f)
            memcount['membercount'] = member.guild.member_count
        with open('memcount.json', 'w') as f:
            json.dump(memcount, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.debug:
            logger.info(
                f"{message.author} ({message.author.id}): \n{message.content}\n\nthe message contains {len(message.embeds)} embed(s)")


def setup(client):
    client.add_cog(Listener(client))
