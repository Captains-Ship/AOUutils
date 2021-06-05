import discord
import random
from discord.ext import commands
from discord.ext.commands import cog
from discord.ext import tasks
from itertools import cycle
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
from traceback import format_exception
import io
import contextlib
from io import BytesIO
from pprint import pprint
import os
import textwrap
import asyncio
import json
import datetime
import urllib.request
from utilities.utils import *
def linecount():
    with open('AOUutils.py', 'r') as file:
        for i, l in enumerate(file):
            pass
    return i + 1
with open('config.json', 'r') as conf:
    token = json.load(conf)


client = commands.Bot(
    command_prefix =commands.when_mentioned_or("aou "),
    case_insensitive=True,
    status=discord.Status.dnd,
    activity=discord.Game(f"AOU"),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True
        )
)

client.remove_command('help')
bot = client



@client.command()
async def help(ctx):
    await ctx.send('To get help dont just say "help me" or "it doesnt work". Please __State your issue__,')


@client.command()
async def ping(ctx):
    await ctx.send(str(round(client.latency * 100)) + "ms")


@client.command()
async def pog(ctx):
    await ctx.send('<:pog:850783102086807582>')



@client.command()
async def cracked(ctx):
    await ctx.send('We do not support cracked versions of the game. Please buy it.')



@client.command()
async def ban(ctx):
    await ctx.send('http://bit.ly/launchpadbanappeal')



@client.command()
async def epic(ctx):
    await ctx.send('The mod and 100 player battle royale works on epic games')

@client.command()
async def helpme(ctx):
    await ctx.send('if you need help go to <#809192430935080960>')

@client.command()
async def ticket(ctx):
    await ctx.send('In the next 24 hours, please either close this ticket or state your issue, or we will consider it a troll ticket and warn you. Thanks!')


@client.command()
async def warn(ctx):
    await ctx.send('1st warning: nothing \n2nd warning: nothing \n3rd warning: mute 1d \n4th warning: temp ban 7 days \n5th warning: perm ban')


async def setpres():
    guild = client.get_guild(794950428756410429)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

@client.command()
@commands.has_permissions(manage_messages=True)
async def echo(ctx, *, text=" "):
    if text != ' ':
        await ctx.send(text)
    else:
        await ctx.reply('I cannot send nothing')
        
@client.command(aliases=['utils', 'util'])
async def utilities(ctx):
    embed = discord.Embed(
        title='About the bot',
        description = 'I am a bot coded by GingerGigiCat and Captain designed for AOU',
        colour = discord.Colour.red()
        )
    embed.add_field(name='Lines:', value=str(linecount()))
    await ctx.reply(embed=embed)


@client.event
async def on_member_join(member):
    guild = client.get_guild(794950428756410429)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

@client.event
async def on_member_remove(member):
    guild = client.get_guild(794950428756410429)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

@client.command()
async def info(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title = 'Info about AOU',
        description=f'Owner: {guild.owner}.\nMembercount: {guild.member_count}',
        colour = discord.Colour.red(),
        timestamp = datetime.datetime.now()
        )
    memcount = int(len(onlinecount(guild))) - 1
    embed.add_field(name='Role Count', value=len(guild.roles))
    embed.add_field(name='Channel Count', value=len(guild.channels))
    embed.add_field(name='Members Online:', value=memcount)
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'requested by {ctx.author}')
    await ctx.reply(embed=embed)

@client.event
async def on_ready():
    await setpres()
    print(f'Bot is now online!')



@client.command()
async def html(ctx):
    await ctx.send('HTML is not a programming language. it is a markdown language. theres a difference.')



@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild == None:
        return
    if "mobile" in message.content.lower() and "aou" in message.content.lower():
        await message.reply('The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')

    await client.process_commands(message)




client.run(token['token'])
