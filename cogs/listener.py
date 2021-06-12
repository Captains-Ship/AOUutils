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
        # check binary, smh imagine not using // as comments3
        is_binary = True
        for letter in message.content.replace(" ", ""):
            if letter != "0" and letter != "1":  # this syntax is cringe
                is_binary = False  # imagine using `False` and not `false`

        if is_binary and not message.attachments:
            array = message.content.split()
            ascii_string = ""
            for binary_value in array:
                an_integer = int(binary_value, 2)
                ascii_character = chr(an_integer)
                ascii_string += ascii_character

            embed = discord.Embed(
                title="Converted Binary to ASCII",
                description=f"{ascii_string}",
                colour=discord.Colour.red()
            )
            embed.set_footer(icon_url=message.author.avatar_url, text=f'Requested by {message.author.name}')
            await message.reply(embed=embed)
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
            devserv = self.client.get_guild(850668209148395520)
            if ctx.author in devserv.members:
                """
                try:
                    embed = discord.Embed(
                        title='Error!',
                        description=''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                        colour=discord.Colour.red())
                except:
                    print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
                    embed = discord.Embed(
                        title='Error!',
                        #description=''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                        colour=discord.Colour.red())
                """
                paginator = commands.Paginator()
                paginator.add_line(''.join(traceback.format_exception(type(error), error, error.__traceback__)))


                for page in paginator.pages:
                    await ctx.send(page)
            else:
                embed = discord.Embed(
                    title='Error!',
                    #description=''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                    colour=discord.Colour.red())

            embed.add_field(name='The Error:', value=error)
            await ctx.send(embed=embed)
            print(''.join(traceback.format_exception(type(error), error, error.__traceback__))) 



    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "h0nde" in member.name.lower() or "h0nda" in member.name.lower():
            chandler = member.guild.get_channel(852186132111556690)
            await chandler.send(f'{member.mention} has been banned due to the keyword "h0nde"')
            await member.send('Hi! you have been removed from the server due to a keyword, if this was a mistake add Captain#3175')
            await member.guild.ban(member, reason='h o n d a')
def setup(client):
    client.add_cog(Listener(client))
