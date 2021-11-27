import discord
from discord.ext import commands
import datetime
from utility.utils import *
from logger import logger
from urllib.parse import quote
import aiohttp

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command(description="Chatbot")
    @commands.cooldown(1, 3, type=discord.ext.commands.BucketType.user)
    async def chat(self, ctx, *, text):
        async with asyncio.ClientSession() as cs:
            text = quote(text, safe="")
            key = getconfig()["tokens"]["nuggies"]
            async with cs.get(f"https://api.nuggetdev.com/chat?message={text}&key={key}") as resp:
                if resp.status == 200:
                    await ctx.send(resp.json())


    @commands.command(description='Makes the bot say something.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, *, text=" "):
        if text != ' ':
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(text)
        else:
            await ctx.reply('I cannot send nothing')
    
    @commands.command(description='Converts a hexadecimal string into an ASCII string.', usage='<hexadecimal string>\n`hexadecimal string`: The string that is to be converted into ASCII. This is a required argument.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def hex(self, ctx, *, hexed):
        hex_string = hexed
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        embed = discord.Embed(
            title="Converted Hex to ASCII",
            description=f'{ascii_string}',
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f'Requested by {ctx.message.author.name}')
        await ctx.reply(embed=embed)



    @commands.command(aliases=['bin'], description='Converts a binary string into an ASCII string.', usage='<binary string>\n`binary string`: The string that is to be converted into ASCII. This is a required argument.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def binary(self, ctx, *, bin):
        is_binary = True
        for letter in bin.replace(" ", ""):
            if letter != "0" and letter != "1":  # this syntax is cringe
                is_binary = False  # imagine using `False` and not `false`

        if is_binary:
            array = bin.split()
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
            embed.set_footer(icon_url=ctx.message.author.display_avatar.url, text=f'Requested by {ctx.message.author.name}')
            await ctx.reply(embed=embed)

    @commands.command(description='Creates an embed.', usage='<colour> <description>\n`colour`: The colour of the embed. This is a required argument.\n`colour`: The colour of the embed. This is a required argument.\n`description`: The description of the embed. This is a required argument.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, color='** **', *, emb="** **"):
        gray = '#2f3136'
        if not "#" in color:
          dahex = '#' + color.upper()
        else:
            dahex = color
        if len(color) == 7 or len(color) == 6:
            sixteenIntegerHex = int(dahex.upper().replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            embed = discord.Embed(
                description=emb,
                colour=readableHex
            )
        else:
            sixteenIntegerHex = int(gray.upper().replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            embed = discord.Embed(
                description=f'{color} {emb}',
                colour=readableHex
            )
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(help='info about AOU')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title=f'Info About {ctx.guild.name}',
            description=f'Owner: {ctx.guild.owner}',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Channels', value=len(ctx.guild.channels))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f'requested by {ctx.author}')
        embed.add_field(name='Membercount', value=memcount(ctx.guild))
        embed.add_field(name='Members Online', value=countOnlineMember(ctx.guild))
        await ctx.reply(embed=embed)
    
    @commands.command(description='Returns the latency between the bot and Discord.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=str(round(self.client.latency * 1000)) + "ms",
            colour=discord.Colour.red() 
        )
        await ctx.reply(embed=embed)

    @commands.command(description='Info about this bot.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Info about the bot.',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(icon_url=ctx.guild.icon_url, text='Devs: Captain, GingerGigiCat, EnderB0YHD, Toasty')
        embed.add_field(name='Main Linecount', value=lineCount())
        await ctx.reply(embed=embed)
    



    @commands.command(description='Returns a list of the staff members of AOU.')
    @commands.cooldown(1, 15, type=discord.ext.commands.BucketType.user)
    async def staff(self, ctx):
        embed = discord.Embed(
            title = 'Staff Team of AOU',
            description='List of all Staff of AOU',
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )

        android = ctx.guild.get_role(837697914561364008)
        dev = ctx.guild.get_role(794983920848338995)
        adm = ctx.guild.get_role(849669487783444490)
        mod = ctx.guild.get_role(795034661805359134)
        androidteam = []
        devteam = []
        admteam = []
        modteam = []
        rolelist = [837697914561364008, 794983920848338995, 849669487783444490, 795034661805359134]
        teams = ['android team', 'dev team', 'admin team', 'moderator team']
        for m in ctx.guild.members:
            memrol = []
            if m.top_role.id in rolelist:
                if m.top_role == android:
                    androidteam.append(m.name)
                if m.top_role == dev:
                    devteam.append(m.name)
                if m.top_role == adm:
                    admteam.append(m.name)
                if m.top_role == mod:
                    modteam.append(m.name)
            else:
                for role in m.roles:
                    if role.id in rolelist:
                        memrol.append(role)
                memrol.reverse()
                try:
                    if memrol[0] == android:
                        androidteam.append(m.name)
                    if memrol[0] == dev:
                        devteam.append(m.name)
                    if memrol[0] == adm:
                        admteam.append(m.name)
                    if memrol[0] == mod:
                        modteam.append(m.name)
                except:
                    pass
        androidteam = str(androidteam).replace('\', \'', '\n')
        devteam = str(devteam).replace('\', \'', '\n')
        admteam = str(admteam).replace('\', \'', '\n')
        modteam = str(modteam).replace('\', \'', '\n')
        androidteam = str(androidteam).replace('[\'', '\n')
        devteam = str(devteam).replace('[\'', '\n')
        admteam = str(admteam).replace('[\'', '\n')
        modteam = str(modteam).replace('[\'', '\n')
        androidteam = str(androidteam).replace('\']', '\n')
        devteam = str(devteam).replace('\']', '\n')
        admteam = str(admteam).replace('\']', '\n')
        modteam = str(modteam).replace('\']', '\n')
        for team in teams:
            if team == 'android team':
               embed.add_field(name=team, value=androidteam, inline=False)
            if team == 'dev team':
               embed.add_field(name=team, value=devteam, inline=False)
            if team == 'admin team':
               embed.add_field(name=team, value=admteam, inline=False)
            if team == 'moderator team':
               embed.add_field(name=team, value=modteam, inline=False)
                        

        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f'Requested by {ctx.author}')
        embed.set_author(name='Values may or may not be incorrect due to the wacky way i implemented this.')
        await ctx.reply(embed=embed)
    
    @commands.command(description='Returns information about you or that of the mentioned user.', usage='<user>\n`user`: The user whose information you want to see. This is an optional argument and can be either a mention or a user ID')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        mention = []
        for role in member.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        mention.reverse()
        memberRole = ", ".join(mention)
        joinDate = member.joined_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        creationDate = member.created_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        memberIcon = member.display_avatar
        authorIcon = ctx.message.author.display_avatar
        embed = discord.Embed(
            title=f'{member.name}#{member.discriminator}',
            description=f'ID: {member.id}',
            colour=member.colour
        )
        embed.add_field(name="Join Date", value=joinDate)
        embed.add_field(name="Creation Date", value=creationDate, inline=True)
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name="Roles", value=memberRole)
        embed.set_thumbnail(url=memberIcon)
        embed.set_footer(icon_url=authorIcon, text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)

            
def setup(client):
    client.add_cog(Misc(client))
