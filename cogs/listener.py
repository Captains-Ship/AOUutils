from discord.ext import commands
import discord
import traceback
import datetime
from discord.ext.commands import *
import json
class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print('AOUUtils is ready')
        chandler = self.client.get_channel(854333051852685333)
        await chandler.send('Bot is now up!')
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    #flags a message for steam scam
    async def flag(self, message: discord.Message):
        member = message.author
        if message.guild.id == 794950428756410429:
            channel = self.client.get_channel(853191467941494784)
            embed = discord.Embed(
                title = 'Possible Steam Scam!',
                description = f'{member} sent the following in {message.channel.mention}:\n`{message.content}`\n\nTo ban the user to the following:\n`aou ban {message.author.id} Steam Scam`',
                colour = discord.Colour.red()
            )
            await message.delete()
            await channel.send(embed=embed)
            await member.send(f'You have been automatically flagged for `Steam Scam` by the automod. Sorry if its too strict but try it doesnt autoban/automute, it only flags it for the moderators to see. the moderators have common sense so you will probably be alright.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
            print('h')
        if "https://steancomunnity.ru/" in message.content.lower() and not message.author.guild_permissions.administrator:
            await self.flag(message)
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply('The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')
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
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id != 347366054806159360:
                if ctx.command.name == 'work':
                    try:
                        with open('cur.json', 'r') as f:
                            jason = json.load(f)
                            if str(jason[str(ctx.author.id)]) != '500': 
                                timeleftins = error.retry_after
                                timeleftformat = str(datetime.timedelta(seconds=timeleftins))
                                timelol = timeleftformat.split(':')
                                s3 = timelol[2]
                                s2 = s3.split('.')
                                s = s2[0]
                                m = timelol[1]
                                await ctx.send(f'This command is on cooldown. Please wait {m} minutes and {s} seconds.')
                            else:
                                await ctx.reinvoke()
                    except:
                        await ctx.reply('You dont have an account! do `aou start`')
                else:
                    await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')
            else:
                await ctx.reinvoke()
        elif isinstance(error, commands.CommandNotFound):
            pass
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
            await ctx.reply(f'Error executing command! \n{error}\nYou should never receive this message. Contact Captain#3175 about this and he will hopefully add an error handler for that.')

    @commands.command()
    @commands.is_owner()
    async def debugger(self, ctx):
        if self.client.debug == False:
            self.client.debug = True
        else:
            self.client.debug = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "h0nde" in member.name.lower() or "h0nda" in member.name.lower():
            chandler = member.guild.get_channel(852186132111556690)
            await chandler.send(f'{member.mention} has been banned due to the keyword "h0nde"')
            await member.send('Hi! you have been removed from the server due to a keyword, if this was a mistake add Captain#3175')
            await member.guild.ban(member, reason='h o n d a')
def setup(client):
    client.add_cog(Listener(client))
