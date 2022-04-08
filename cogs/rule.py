import discord
from discord import app_commands
from discord.ext import commands


# from utility.rules import rules, ruleshort
import config


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

        "NO DRAMA - Arguments that happens in any chat will result in a mute. Continuation will result in a kick and so "
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

    @commands.command(description="Get the rules for the server.",
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

    @app_commands.command(name='rule', description='Get the rules for the server.')
    @app_commands.describe(rule="The specific rule that you want to view.")
    @app_commands.guilds(config.slash_guild)
    async def rule_slash(self, interaction: discord.Interaction, rule: app_commands.Range[int, 1, len(ruleshort)] = None):
        if rule is None:
            embed = discord.Embed(
                title='Rules',
                colour=discord.Colour.red()
            )
            rulength = len(self.ruleshort)
            for i in range(0, rulength):
                embed.add_field(name=f'Rule #{i + 1}', value=self.rules[i], inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            rulelul = rule - 1
            embed = discord.Embed(
                title=f'Rule #{rule}',
                description=self.rules[rulelul],
                colour=discord.Colour.red()
            )
            await interaction.response.send_message(embed=embed)

    @commands.command(description='Enforces a rule',
                      usage='<rule number>\n`rule number`: The specific rule that you want to enforce. This is a required argument and must be an integer.')
    @commands.has_permissions(kick_members=True)
    async def enforce_slash(self, ctx, user: discord.Member = None, rule: int = 9999):
        if rule == 9999:
            await ctx.send('bru nice rule man')
            return
        if user == None:
            await ctx.send('Give me a user to warn!')
            return
        try:
            embed = discord.Embed(
                title='Enforced!',
                colour=discord.Colour.red()
            )
            embed.add_field(name=f'Rule #{rule}', value=self.rules[rule - 1], inline=False)
            await ctx.send(f'{user.mention} Please follow our rules. You have been warned for rule {rule}:',
                           embed=embed)
            await user.send(f'{user.mention} Please follow our rules. You have been warned for rule {rule}:',
                            embed=embed)
        except Exception as e:
            await ctx.send(e)

    @app_commands.command(name='enforce', description='Enforces a rule')
    @app_commands.describe(member="The member that you want to warn.",
                           rule="The specific rule that you want to enforce.")
    @app_commands.guilds(config.slash_guild)
    @app_commands.checks.has_permissions(kick_members=True)
    async def enforce(self, interaction: discord.Interaction, member: discord.Member,
                      rule: app_commands.Range[int, 1, len(ruleshort)]):
        try:
            embed = discord.Embed(
                title='Enforced!',
                colour=discord.Colour.red()
            )
            embed.add_field(name=f'Rule #{rule}', value=self.rules[rule - 1], inline=False)
            await interaction.response.send_message(
                f'{member.mention} Please follow our rules. You have been warned for rule {rule}:',
                embed=embed)
            await member.send(f'{member.mention} Please follow our rules. You have been warned for rule {rule}:',
                              embed=embed)
        except Exception as e:
            await interaction.response.send_message(e)


async def setup(client):
    await client.add_cog(Rule(client))
