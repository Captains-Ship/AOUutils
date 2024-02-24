
import discord
from discord.ext import commands
import datetime

from utility.utils import *


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @Command(description='Makes the bot say something.')
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, *, text: str = None):
        if text:
            await ctx.send(text)
        else:
            await ctx.reply(Response(ctx.locale).cant_echo_blank)

    @Command(description='Converts a hexadecimal string into an ASCII string.',
                      usage='<hexadecimal string>\n`hexadecimal string`: The string that is to be converted into ASCII. This is a required argument.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def hex(self, ctx, *, hexed: str):
        resp = Response(ctx.locale)
        hex_string = hexed
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        embed = discord.Embed(
            title=resp.conv_hex_to_ascii,
            description=f'{ascii_string}',
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=resp.req_by.format(ctx.author.name))
        await ctx.reply(embed=embed)

    @Command(aliases=['bin'], description='Converts a binary string into an ASCII string.',
                      usage='<binary string>\n`binary string`: The string that is to be converted into ASCII. This is a required argument.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def binary(self, ctx, *, bin: str):
        resp = Response(ctx.locale)
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
                title=resp.conv_bin_to_ascii,
                description=f"{ascii_string}",
                colour=discord.Colour.red()
            )
            embed.set_footer(icon_url=ctx.message.author.display_avatar.url, text=resp.req_by.format(ctx.author.name))
            await ctx.reply(embed=embed)

    @Command(help='info about AOU')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def info(self, ctx):
        resp = Response(ctx.locale)
        embed = discord.Embed(
            title=resp.info_title.format(ctx.guild.name),
            description=resp.info_owner.format(ctx.guild.owner.name),
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name=resp.channels, value=len(ctx.guild.channels))
        embed.add_field(name=resp.roles, value=len(ctx.guild.roles))
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=resp.req_by.format(ctx.author.name))
        embed.add_field(name=resp.member_count, value=memcount(ctx.guild))
        embed.add_field(name=resp.members_online, value=countOnlineMember(ctx.guild))
        await ctx.reply(embed=embed)

    @Command(name="ping", description='Returns the latency between the bot and Discord.')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def ping(self, ctx):
        resp = Response(ctx.locale)
        embed = discord.Embed(
            title=resp.ping,
            description=str(round(self.client.latency * 1000)) + "ms",
            colour=discord.Colour.red()
        )
        await ctx.reply(embed=embed)


    @Command(description='Returns information about you or that of the mentioned user.',
                      usage='<user>\n`user`: The user whose information you want to see. This is an optional argument and can be either a mention or a user ID')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        resp = Response(ctx.locale)
        member = member or ctx.author
        mention = [r.mention.replace(f"<@&{ctx.guild.id}>", "@everyone") for r in reversed(member.roles)]
        memberRole = ", ".join(mention)
        joinDate = member.joined_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        creationDate = member.created_at.strftime("%a, %b %d %Y \n%H:%M:%S %p")
        memberIcon = member.display_avatar
        authorIcon = ctx.message.author.display_avatar
        embed = discord.Embed(
            title=str(member),
            description=f'ID: {member.id}',
            colour=member.colour
        )
        embed.add_field(name=resp.join_date, value=joinDate)
        embed.add_field(name=resp.creation_date, value=creationDate, inline=True)
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name=resp.roles, value=memberRole)
        embed.set_thumbnail(url=memberIcon)
        embed.set_footer(icon_url=authorIcon, text=resp.req_by.format(ctx.author.name))
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Misc(client))
