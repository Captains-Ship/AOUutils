import discord
from discord import app_commands
from discord.ext import commands
from config import slash_guild
# from utility.rules import rules, ruleshort
import config
from utility.utils import Command


class Rule(commands.Cog):

    def __init__(self, client):
        self.client = client

    rules = [

        "No NSFW - This is a simple and basic rule that everyone needs to follow. If you post any kind of NSFW it will "
        "result in a mute. Continuing will result in a ban. (THIS INCLUDES BORDERLINE NSFW).",

        "No bullying - Being a jerk to others is not allowed. Bullying will "
        "result in a warn. Continuing will result in a kick.",

        "No harassment - If you are here just to harass others because of what they are, you need to leave. We do not "
        "accept this. Will result in a mute. Continuation will result in a ban.",

        "NO DRAMA - Arguments that happens in any chat will result in a mute. Continuation will result in a kick and "
        "so "
        "on. Just bring it to DM's please.",

        "No Advertising - This includes DM advertising.",

        "No Impersonation - Impersonating others will result in a nickname change.",

        "No illegal Activity of any kind. - Any illegal activity that follows "
        "under US Laws or other countries will result in a permanent ban and we will contact Discord support.",

        "Follow the Discord Terms of Service. - Example: Being underage "
        "will result in a ban. No raiding either.",

        "HAVE COMMON SENSE. - Think before you post or ask something. "
        "Do not post any memes about tragic events like 9/11 or animal "
        "abuse. That will result in a mute. Continuation will result in "
        "a Ban. This does include keeping stuff in the correct channel.",

        "No ghost pinging. - Ghost pinging is pinging someone and then "
        "deleting the ping. Will result in a warn. Spam pinging will "
        "result in  mute.",

        "No loophooling. - Loopholing is basically breaking a rule and saying "
        "how something isn't a rule even though it is. This will result in a warn or ban.",

        "No videos that crash peoples clients. - Videos that crashes peoples discord "
        "application will result it from being deleted and you will get muted."

    ]

    ruleshort = [

        "No NSFW - (THIS INCLUDES BORDERLINE NSFW).",

        "No bullying - Being a jerk to others is not allowed.",

        "No harassment - If you are here just to harass others because of what they are, you need to leave.",

        "NO DRAMA - Just bring it to DM's please.",

        "No Advertising - This includes DM advertising",

        "No Impersonation - Impersonating others will result in a nickname change.",

        "No illegal Activity of any kind. - Any illegal activity that follows "
        "under US Laws or other countries will result in a permanent ban and we will contact Discord support.",

        "Follow the Discord Terms of Service. - Example: Being underage "
        "will result in a ban. No raiding either.",

        "HAVE COMMON SENSE. - This does include keeping stuff in the correct channel.",

        "No ghost pinging. - Ghost pinging is pinging someone and then "
        "deleting the ping",

        "No loophooling. - Loopholing is basically breaking a rule and saying "
        "how something isn't a rule even though it is. This will result in a warn or ban.",

        "No videos that crash peoples clients. - will result it from being deleted and you will get muted."

    ]

    @Command(name="rule", description="Get the rules for the server.",
                             usage="[rule number]\n`rule number`: The specific rule that you want to view. This is an optional argument and must be an integer.")
    async def rule(self, ctx, rule: int = -1):
        try:
            if rule == -1:
                embed = discord.Embed(
                    title='Rules',
                    colour=discord.Colour.red()
                )
                rulength = len(self.ruleshort)
                for i in range(0, rulength):
                    embed.add_field(name=f'Rule #{i + 1}', value=self.rules[i], inline=False)
                await ctx.send(embed=embed)
            else:
                rulelul = rule - 1
                embed = discord.Embed(
                    title=f'Rule #{rule}',
                    description=self.rules[rulelul],
                    colour=discord.Colour.red()
                )
                await ctx.send(embed=embed)
        except:
            await ctx.send('Unknown rule.')

    @rule.autocomplete('rule')
    async def rule_ac(self, interaction: discord.Interaction, current: int):
        return []


async def setup(client):
    await client.add_cog(Rule(client))
