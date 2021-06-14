from discord.ext import commands
import discord
import traceback
import datetime
from discord.ext.commands import *

class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print('AOUUtils is ready')
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
            print('h')
        if "cs:go" in message.content.lower():
            if "trade" in message.content.lower():
                if "giving" in message.content.lower():
                    if "http" in message.content.lower():
                        if not message.author.guild_permissions.administrator:
                            if not message.author.bot:
                                await message.delete()
                                await message.author.send('You have been warned by the automatic Anti-Steam-Scam system')
                                chandler = self.client.get_channel(853191467941494784)
                                await chandler.send(f'{message.author.mention} Sent a steam scam!')
                                muterole = message.guild.get_role(799839676479176705)
                                await message.author.add_roles(muterole)

        
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
            await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')
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



    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "h0nde" in member.name.lower() or "h0nda" in member.name.lower():
            chandler = member.guild.get_channel(852186132111556690)
            await chandler.send(f'{member.mention} has been banned due to the keyword "h0nde"')
            await member.send('Hi! you have been removed from the server due to a keyword, if this was a mistake add Captain#3175')
            await member.guild.ban(member, reason='h o n d a')
def setup(client):
    client.add_cog(Listener(client))
