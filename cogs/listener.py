from discord.ext import commands
import discord
import traceback
import datetime


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
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply('The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title='Error!',
                description='Command Not Found!',
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            await ctx.reply(embed=embed)
        else:
            if ctx.author.guild_permissions.administrator:
                try:
                    embed = discord.Embed(
                        title='Error!',
                        description=''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                        colour=discord.Colour.red())
                except:
                    print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
            else:
                embed = discord.Embed(
                    title='Error!',
                    #description=''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                    colour=discord.Colour.red())

            embed.add_field(name='Simplified Error!', value=error)
            await ctx.reply(embed=embed)
            print(''.join(traceback.format_exception(type(error), error, error.__traceback__))) 

def setup(client):
    client.add_cog(Listener(client))
