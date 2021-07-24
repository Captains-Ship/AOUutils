import discord
from discord.ext import commands
import datetime
from utility.utils import *
from logger import logger

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(help='makes the bot say something.')
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
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def hex(self, ctx):
        hex_string = ctx.message.content.replace("aou hex ", "")
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        embed = discord.Embed(
            title="Converted Hex to ASCII",
            description=f'{ascii_string}',
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f'Requested by {ctx.message.author.name}')
        await ctx.reply(embed=embed)



    @commands.command(aliases=['bin'])
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
            embed.set_footer(icon_url=ctx.message.author.avatar.url, text=f'Requested by {ctx.message.author.name}')
            await ctx.reply(embed=embed)

    @commands.command()
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
            title='Info About All Of Us',
            description=f'Owner: {ctx.guild.owner}',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Channels', value=len(ctx.guild.channels))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f'requested by {ctx.author}')
        embed.add_field(name='Membercount', value=memcount(ctx.guild))
        embed.add_field(name='Members Online', value=countOnlineMember(ctx.guild))
        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=str(round(self.client.latency * 1000)) + "ms",
            colour=discord.Colour.red() 
        )
        await ctx.reply(embed=embed)
    @commands.command()
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
    



    @commands.command()
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
                        

        embed.set_footer(icon_url=ctx.author.avatar.url, text=f'Requested by {ctx.author}')
        embed.set_author(name='Values may or may not be incorrect due to the wacky way i implemented this.')
        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is not None:
            mention = []
            for role in member.roles:
                if role.name != "@everyone":
                    mention.append(role.mention)

            memberRole = ", ".join(mention)
            joinDate = member.joined_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
            creationDate = member.created_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
            memberIcon = member.avatar_url
            authorIcon = ctx.message.author.avatar_url
            embed = discord.Embed(
                title=f'{member.name}#{member.discriminator}',
                description=f'ID: {member.id}',
                colour=discord.Colour.random()
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
