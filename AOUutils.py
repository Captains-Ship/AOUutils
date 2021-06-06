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
    command_prefix =commands.when_mentioned_or('aou ', 'AOU ', 'Aou '),
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

"""
<:pog:850783102086807582>
<a:Yes:850974892366757930>
<a:X_:850974940282748978> these are emotes of AOUutils dev
"""

@client.group()
async def rule(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('1. No NSFW - This is a simple and basic rule that everyone needs to follow. If you post any kind of NSFW it will result in a mute. Continuing will result in a ban. (THIS INCLUDES BORDERLINE NSFW).\n\n2. No bullying - Being a jerk to others is not allowed. Bullying will result in a warn. Continuing will result in a kick.\n\n3. No harassment - If you are here just to harass others because of what they are, you need to leave. We do not accept this. Will result in a mute. Continuation will result in a ban.\n\n4. NO DRAMA - Arguments that happens in any chat will result in a mute. Continuation will result in a kick and so on. Just bring it to DM\'s please.\n\n5. No Advertising - This includes DM advertising. The only place you are allowed to advertise is in #deleted-channel. We only allow YouTube links here.\n\n6. No Impersonation - Impersonating others will result in a nickname change.\n\n7. No illegal Activity of any kind. - Any illegal activity that follows under US Laws or other countries will result in a permanent ban and we will contact Discord support.\n\n8. Follow the Discord Terms of Service. - Example: Being underage will result in a ban. No raiding either.\n\n9. HAVE COMMON SENSE. - Think before you post or ask something. Do not post any memes about tragic events like 9/11 or animal abuse. That will result in a mute. Continuation will result in a Ban. This does include keeping stuff in the correct channel.\n\n10. No ghost pinging. - Ghost pinging is pinging someone and then deleting the ping. Will result in a warn. Spam pinging will result in a mute./n/n11. No loophooling. - Loopholing is basically breaking a rule and saying how something isn\'t a rule even though it is. This will result in a warn or ban.\n\n12. No videos that crash peoples clients. - Videos that crashes peoples discord application will result it from being deleted and you will get muted.')

@rule.command(name='1')
async def _1(ctx):
    await ctx.send('No NSFW - This is a simple and basic rule that everyone needs to follow. If you post any kind of NSFW it will result in a mute. Continuing will result in a ban. (THIS INCLUDES BORDERLINE NSFW).')

@rule.command(name='2')
async def _2(ctx):
    await ctx.send('No bullying - Being a jerk to others is not allowed. Bullying will result in a warn. Continuing will result in a kick.')

@rule.command(name='3')
async def _3(ctx):
    await ctx.send('No harassment - If you are here just to harass others because of what they are, you need to leave. We do not accept this. Will result in a mute. Continuation will result in a ban.'
)
@rule.command(name='4')
async def _4(ctx):
    await ctx.send('NO DRAMA - Arguments that happens in any chat will result in a mute. Continuation will result in a kick and so on. Just bring it to DM\'s please.')

@rule.command(name='5')
async def _5(ctx):
    await ctx.send('No Advertising - This includes DM advertising.')


@rule.command(name='6')
async def _6(ctx):
    await ctx.send('No Impersonation - Impersonating others will result in a nickname change.')



@rule.command(name='7')
async def _7(ctx):
    await ctx.send('No illegal Activity of any kind. - Any illegal activity that follows under US Laws or other countries will result in a permanent ban and we will contact Discord support.')

@rule.command(name='8')
async def _8(ctx):
    await ctx.send('Follow the Discord Terms of Service. - Example: Being underage will result in a ban. No raiding either.')


@rule.command(name='9')
async def _9(ctx):
    await ctx.send('HAVE COMMON SENSE. - Think before you post or ask something. Do not post any memes about tragic events like 9/11 or animal abuse. That will result in a mute. Continuation will result in a Ban. This does include keeping stuff in the correct channel.')




@rule.command(name='10')
async def _10(ctx):
    await ctx.send('No ghost pinging. - Ghost pinging is pinging someone and then deleting the ping. Will result in a warn. Spam pinging will result in a mute.')



@rule.command(name='11')
async def _11(ctx):
    await ctx.send('No loophooling. - Loopholing is basically breaking a rule and saying how something isn\'t a rule even though it is. This will result in a warn or ban.')

@rule.command(name='12')
async def _12(ctx):
    await ctx.send('No videos that crash peoples clients. - Videos that crashes peoples discord application will result it from being deleted and you will get muted.')




@client.command()
async def tou(ctx):
    await ctx.send('We are **NOT** Town Of Us, We are **All Of Us**.')



@client.command(aliases=['timezone', 'timesones', 'timesone'])
async def timezones(ctx):
    await ctx.send('```UTC+5: Vedant (Moderator)\n\nUTC+2: Captain (Head Staff)\n\nUTC+1: Wulfstrex (Moderator), EnderBoyHD (Admin), Mathew (Moderator)\n\nUTC0: Ariana Pierer (Community Manager), Shadows (Moderator)\n\nUTC-3: funnynumber (Main-Dev), XtraCube (Main-Dev), Ruthless (Moderator), Neil (Moderator)\n\nUTC-4: Doggo (Moderator), TheDreamChicken (Admin)\n\nUTC-5: Pure (Owner), angxl wtf (Owner), Joshua TDM (Community Manager), Skylario (Head Staff), Jameyiscool (Moderator), Pikanaruto (Admin)\n\nUTC-7: Popcat (Moderator)```')


@client.command()
async def screenshot(ctx):
    await ctx.send('To take a screenshot:\nwindows: hold Windows key + SHIFT + S\nMacOS: cmd + shift + 4')


@client.command()
async def purge(ctx, limit=0):
    if limit != 0 and limit < 301:
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f'Purged {limit}', delete_after=5)
    else:
        await ctx.reply('Either you purged nothing or above 300 messages.')


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
