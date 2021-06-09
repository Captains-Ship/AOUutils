import discord
from discord.ext import commands


class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def man(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851472289542307870/unknown.png')

    @commands.command(aliases=['oldtimes', 'old'])
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def nostalgia(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851499238839418970/unknown.png')
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def man2(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851491959273291776/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def html(self, ctx):
        await ctx.send('HTML ISNT A PROGRAMMING LANGUAGE')
    


    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def timezones(self, ctx):
        await ctx.reply('```UTC+5: Vedant (🔰Helper), Toasty (👨‍💻Developer)\n\nUTC+2: Captain (🔰Head Staff)\n\nUTC+1: Wulfstrex (🔰Helper), EnderBoyHD (🔰Staff), Mathew (🔰Helper)\n\nUTC0: Ariana Pierer (🔰Co-Owner), Shadows (🔰Staff)\n\nUTC-3: funnynumber (👨‍💻Main-Dev), XtraCube (🔰Co-Owner), Ruthless (🔰Staff), Neil (🔰Helper)\n\nUTC-4: Doggo (🔰Helper), TheDreamChicken (🔰Staff)\n\nUTC-5: Pure (🔰Owner), angxl wtf (🔰Owner), Joshua TDM (👥Community Manager), Skylario (🔰Head Staff), Jameyiscool (🔰Helper), Pikanaruto (🔰Staff)\n\nUTC-7: Popcat (🔰Staff)```')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def virus(self, ctx):
        await ctx.send('The mod is not a virus. Some antivirus software dont like `dll` files. please disable your antivirus or add an exception.')



    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def idw(self, ctx):
        await ctx.send('To get help dont just say "help me" or "it doesnt work". Please __State your issue__!')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def appeal(self, ctx):
        await ctx.send('http://bit.ly/launchpadbanappeal')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def epic(self, ctx):
        await ctx.send('The mod and 100 player battle royale works on epic games')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def helpMe(self, ctx):
        await ctx.send('If you need help go to <#809192430935080960>')

    @commands.command(aliases=['ticket'])
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def blankTicket(self, ctx):
        await ctx.send('In the next **24 hours**, please either close this ticket or state your issue, or we will consider it a troll ticket and warn you. Thanks!')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def punishment(self, ctx):
        embed = discord.Embed(
            title='Punishments',
            colour=discord.Colour.dark_red()
        )
        embed.add_field(name="1st Warning", value="Nothing will happen", inline=False)
        embed.add_field(name="2nd Warning", value="Nothing will happen", inline=False)
        embed.add_field(name="3rd Warning", value="Mute for 1 day", inline=False)
        embed.add_field(name="4th Warning", value="Temporarily ban for 7 days", inline=False)
        embed.add_field(name="5th Warning", value="Permanent ban", inline=True)

        await ctx.send(embed=embed)

    @commands.group()
    async def rule(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.message.content.lower() == "aou rule":
                embed = discord.Embed(
                    title='Rules',
                    colour=discord.Colour.red()
                )
                embed.add_field(name="Rule #1", value="No NSFW - This is a simple and basic rule that everyone needs "
                                                      "to "
                                                      "follow. If you post any kind of NSFW it will result in a mute. "
                                                      "Continuing will result in a ban. (THIS INCLUDES BORDERLINE "
                                                      "NSFW).",
                                inline=False)

                embed.add_field(name="Rule #2", value="No bullying - Being a jerk to others is not allowed. Bullying "
                                                      "will "
                                                      "result in a warn. Continuing will result in a kick.", inline=False)

                embed.add_field(name="Rule #3",
                                value="No harassment - If you are here just to harass others because of what "
                                      "they are, you need to leave. We do not accept this. Will result in a "
                                      "mute. Continuation will result in a ban.", inline=False)

                embed.add_field(name="Rule #4",
                                value="NO DRAMA - Arguments that happens in any chat will result in a mute. "
                                      "Continuation will result in a kick and so on. Just bring it to DM's "
                                      "please.", inline=False)

                embed.add_field(name="Rule #5",
                                value="No Advertising - This includes DM advertising. The only place you are "
                                      "allowed to advertise is in #deleted-channel. We only allow YouTube "
                                      "links here.", inline=False)

                embed.add_field(name="Rule #6", value="No Impersonation - Impersonating others will result in a "
                                                      "nickname "
                                                      "change.", inline=False)

                embed.add_field(name="Rule #7",
                                value="No illegal Activity of any kind. - Any illegal activity that follows "
                                      "under US Laws or other countries will result in a permanent ban and we"
                                      " will contact Discord support.", inline=False)

                embed.add_field(name="Rule #8", value="Follow the Discord Terms of Service. - Example: Being underage "
                                                      "will "
                                                      "result in a ban. No raiding either.", inline=False)

                embed.add_field(name="Rule #9", value="HAVE COMMON SENSE. - Think before you post or ask something. "
                                                      "Do not post any memes about tragic events like 9/11 or animal "
                                                      "abuse. That will result in a mute. Continuation will result in "
                                                      "a Ban. This does include keeping stuff in the correct channel.", inline=False)

                embed.add_field(name="Rule #10", value="No ghost pinging. - Ghost pinging is pinging someone and then "
                                                       "deleting the ping. Will result in a warn. Spam pinging will "
                                                       "result in "
                                                       " a mute.", inline=False)

                embed.add_field(name="Rule #11",
                                value="No loophooling. - Loopholing is basically breaking a rule and saying "
                                      "how something isn't a rule even though it is. This will result in a "
                                      "warn or ban.", inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Rules',
                    description="Unknown Rule",
                    colour=discord.Colour.red()
                )
                await ctx.send(embed=embed)

    @rule.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def full(self, ctx):
        embed = discord.Embed(
            title='Rules',
            colour=discord.Colour.red()
        )
        embed.add_field(name="Rule #1", value="No NSFW - This is a simple and basic rule that everyone needs to "
                                              "follow. If you post any kind of NSFW it will result in a mute. "
                                              "Continuing will result in a ban. (THIS INCLUDES BORDERLINE NSFW).",
                        inline=False)

        embed.add_field(name="Rule #2", value="No bullying - Being a jerk to others is not allowed. Bullying will "
                                              "result in a warn. Continuing will result in a kick.", inline=False)

        embed.add_field(name="Rule #3", value="No harassment - If you are here just to harass others because of what "
                                              "they are, you need to leave. We do not accept this. Will result in a "
                                              "mute. Continuation will result in a ban.", inline=False)

        embed.add_field(name="Rule #4", value="NO DRAMA - Arguments that happens in any chat will result in a mute. "
                                              "Continuation will result in a kick and so on. Just bring it to DM's "
                                              "please.", inline=False)

        embed.add_field(name="Rule #5", value="No Advertising - This includes DM advertising. The only place you are "
                                              "allowed to advertise is in #deleted-channel. We only allow YouTube "
                                              "links here.", inline=False)

        embed.add_field(name="Rule #6", value="No Impersonation - Impersonating others will result in a nickname "
                                              "change.", inline=False)

        embed.add_field(name="Rule #7", value="No illegal Activity of any kind. - Any illegal activity that follows "
                                              "under US Laws or other countries will result in a permanent ban and we"
                                              " will contact Discord support.", inline=False)

        embed.add_field(name="Rule #8", value="Follow the Discord Terms of Service. - Example: Being underage will "
                                              "result in a ban. No raiding either.", inline=False)

        embed.add_field(name="Rule #9", value="HAVE COMMON SENSE. - Think before you post or ask something. Do not "
                                              "post any memes about tragic events like 9/11 or animal abuse. That "
                                              "will result in a mute. Continuation will result in a Ban. This does "
                                              "include keeping stuff in the correct channel.", inline=False)

        embed.add_field(name="Rule #10", value="No ghost pinging. - Ghost pinging is pinging someone and then "
                                               "deleting the ping. Will result in a warn. Spam pinging will result in"
                                               " a mute.", inline=False)

        embed.add_field(name="Rule #11", value="No loophooling. - Loopholing is basically breaking a rule and saying "
                                               "how something isn't a rule even though it is. This will result in a "
                                               "warn or ban.", inline=True)
        await ctx.send(embed=embed)

    @rule.command(name='1')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _1(self, ctx):
        embed = discord.Embed(
            title='Rule #1',
            description='No NSFW - This is a simple and basic rule that everyone needs to follow. If you post any '
                        'kind of NSFW it will result in a mute. Continuing will result in a ban. (THIS INCLUDES '
                        'BORDERLINE NSFW).',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
        
    @rule.command(name='69')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _69(self, ctx):
        embed = discord.Embed(
            title='Rule #69',
            colour=discord.Colour.red()
        )
        embed.set_image(url='https://media.discordapp.net/attachments/842450788998578236/851014341276598302/unknown.png')
        
        await ctx.send(embed=embed)

    @rule.command(name='63')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _63(self, ctx):
        embed = discord.Embed(
            title='Rule #63',
            description='No.',
            colour=discord.Colour.red()
        )

        await ctx.send(embed=embed)


    @rule.command(name='2')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _2(self, ctx):
        embed = discord.Embed(
            title='Rule #2',
            description='No bullying - Being a jerk to others is not allowed. Bullying will result in a warn. '
                        'Continuing will result in a kick.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='3')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _3(self, ctx):
        embed = discord.Embed(
            title='Rule #3',
            description='No harassment - If you are here just to harass others because of what they are, you need to '
                        'leave. We do not accept this. Will result in a mute. Continuation will result in a ban.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='4')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _4(self, ctx):
        embed = discord.Embed(
            title='Rule #4',
            description='NO DRAMA - Arguments that happens in any chat will result in a mute. Continuation will '
                        'result in a kick and so on. Just bring it to DM\'s please.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='5')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _5(self, ctx):
        embed = discord.Embed(
            title='Rule #5',
            description='No Advertising - This includes DM advertising. The only place you are allowed to advertise '
                        'is in #deleted-channel. We only allow YouTube links here.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='6')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _6(self, ctx):
        embed = discord.Embed(
            title='Rule #6',
            description='No Impersonation - Impersonating others will result in a nickname change.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='7')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _7(self, ctx):
        embed = discord.Embed(
            title='Rule #7',
            description='No illegal Activity of any kind. - Any illegal activity that follows under US Laws or other '
                        'countries will result in a permanent ban and we will contact Discord support.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='8')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _8(self, ctx):
        embed = discord.Embed(
            title='Rule #8',
            description='Follow the Discord Terms of Service. - Example: Being underage will result in a ban. No '
                        'raiding either.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='9')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _9(self, ctx):
        embed = discord.Embed(
            title='Rule #9',
            description='HAVE COMMON SENSE. - Think before you post or ask something. Do not post any memes about '
                        'tragic events like 9/11 or animal abuse. That will result in a mute. Continuation will '
                        'result in a Ban. This does include keeping stuff in the correct channel.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='10')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _10(self, ctx):
        embed = discord.Embed(
            title='Rule #10',
            description='No ghost pinging. - Ghost pinging is pinging someone and then deleting the ping. Will result '
                        'in a warn. Spam pinging will result in a mute.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='11')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _11(self, ctx):
        embed = discord.Embed(
            title='Rule #11',
            description='No loophooling. - Loopholing is basically breaking a rule and saying how something isn\'t a '
                        'rule even though it is. This will result in a warn or ban.',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='34')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _34(self, ctx):
        embed = discord.Embed(
            title='Rule #34',
            description='no',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def html2(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851877985199980624/bruhhhh.gif')

def setup(client):
    client.add_cog(Tags(client))
