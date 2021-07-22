from discord.ext import commands
import discord
import traceback
import datetime
from discord.ext.commands import *
import json
from traceback import *
import crayons


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.debug = False

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{crayons.yellow('[AOUutils/listener/ready]')} AOUUtils is ready")
        chandler = self.client.get_channel(854333051852685333)
        await chandler.send('Bot is now up!')
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd,
                                          activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd,
                                          activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd,
                                          activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=f'AOU | {guild.member_count} members'))

    # flags a message for steam scam
    async def flag(self, message: discord.Message, reason='Unspecified'):
        print(f"{crayons.cyan('[AOUutils/listener/Flagger]')} A message was flagged!")
        member = message.author
        if message.guild.id == 794950428756410429:
            channel = self.client.get_channel(853191467941494784)
            embed = discord.Embed(
                title=f'Message Flagged for {reason}!',
                description=f'{member} sent the following in {message.channel.mention}:\n```{message.content}```\n\nTo ban the user to the following:\n```aou ban {message.author.id} {reason}```',
                colour=discord.Colour.red()
            )
            await message.delete()
            await channel.send(embed=embed)
            await member.send(f'You have been automatically flagged for `{reason}` by the automod.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.client.http.token in message.content:
            cap = self.client.get_user(347366054806159360)
            await cap.send('OH GOD OH FUCK RESET THE FUCKING TOKEN NOW ITS BEEN LEAKED')
            try:
                await message.delete()
            except:
                pass
        try:
            role = message.guild.get_role(795034661805359134)
            admin = message.guild.get_role(849669487783444490)
        except:
            pass
        if "cs:go" in message.content.lower() and not role in message.author.roles or "csgo" in message.content.lower() and not role in message.author.roles and not admin in message.author.roles:
            await self.flag(message, reason='Steam Scam')
        if "y.ru" in message.content.lower() and not role in message.author.roles or "t.ru" in message.content.lower() and not role in message.author.roles and not admin in message.author.roles:
            await self.flag(message, reason='Steam Scam')
        if "steancomunnity" in message.content.lower() and not role in message.author.roles and not admin in message.author.roles:
            await self.flag(message, reason='Steam Scam')
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply(
                'The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')
        if "discord-gifts.us" in message.content.lower() and not role in message.author.roles and not admin in message.author.roles:
            await self.flag(message, reason="Nitro Scam")
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
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == 347366054806159360:
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
                                    await ctx.send(
                                        f'This command is on cooldown. Please wait {m} minutes and {s} seconds.')
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
                            f'Error 429: You are being ratelimited. \nPlease wait {m} minutes and {s} seconds.')
                else:
                    if ctx.command.name.lower() != 'jishaku':
                        if str(ctx.command.cog).lower() != 'admin':
                            await ctx.reinvoke()
        elif isinstance(error, commands.CommandNotFound):
            h = ctx.message.content.replace(ctx.prefix, '').split()[0]
            embed = discord.Embed(
                title=f'Unknown Command "{h}"',
                description=f'I do not recognize this command. run `{ctx.prefix}help` for a list of commands.',
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=self.client.user.avatar.url)
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
                    await ctx.send(f'Missing permissions: {error.missing_permissions}')
        elif isinstance(error, commands.NotOwner):
            await ctx.reply('Unowner moment')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply('unknown member')
        elif ctx.command.name.lower() == 'purge':
            if not isinstance(error, MissingPermissions):
                await ctx.send('Nice integer Mate, next time gimmie a number')
        elif isinstance(error, OverflowError):
            await ctx.send('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        else:
            #            await ctx.reply(f'Error executing command! \n{error}\nYou should never receive this message. Contact Captain#3175 about this and he will hopefully add an error handler for that.')
            await ctx.reply(f'Error!\n{error}')
            e = error
            print(f"{crayons.red('[AOUutils/listener/Exception]')} An error was caught!")
            print("".join(format_exception(e, e, e.__traceback__)))

    @commands.command()
    @commands.is_owner()
    async def debugger(self, ctx):
        if self.client.debug == False:
            self.client.debug = True
        else:
            self.client.debug = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{crayons.yellow('[AOUutils/listener/info]')} A member has joined AOU")
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
        print(f"{crayons.yellow('[AOUutils/listener/info]')} A member has left AOU")
        with open('memcount.json', 'r') as f:
            memcount = json.load(f)
            memcount['membercount'] = member.guild.member_count
        with open('memcount.json', 'w') as f:
            json.dump(memcount, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.debug:
            print(
                f"{crayons.green('[AOUutils/listener/OnMessage]')} {message.author} ({message.author.id}) in #{message.channel.name}: \n{message.content}\n\nthe message contains {len(message.embeds)} embed(s)")




def setup(client):
    client.add_cog(Listener(client))
