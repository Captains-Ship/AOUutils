import discord
from discord.ext import commands
from utility.rules import rules

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
    async def python(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850668209148395524/852622410044669955/unknown.png')

    @commands.command()
    async def toasty(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850693035826479114/852964926300881017/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def timezones(self, ctx):
        await ctx.reply('```UTC+5: Vedant (🔰Moderator), Toasty (👨‍💻Developer)\n\nUTC+2: Captain (🔰Head Staff)\n\nUTC+1: Wulfstrex (🔰Moderator), EnderBoyHD (🔰Admin), Mathew (🔰Moderator)\n\nUTC0: Ariana Pierer (👥Community Manager), Shadows (🔰Moderator)\n\nUTC-3: funnynumber (👨‍💻Main-Dev), XtraCube (👨‍💻Main-Dev), Ruthless (🔰Moderator), Neil (🔰Moderator)\n\nUTC-4: Doggo (🔰Moderator), TheDreamChicken (🔰Admin)\n\nUTC-5: Pure (🔰Owner), angxl wtf (🔰Owner), Joshua TDM (👥Community Manager), Skylario (🔰Head Staff), Jameyiscool (🔰Moderator), Pikanaruto (🔰Admin)\n\nUTC-7: Popcat (🔰Admin)```')

    @commands.command()
    async def masswarn(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/802743745032355850/855073669835390976/unknown.png')

    @commands.command()
    async def massclearwarn(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/802743745032355850/855073841285562398/unknown.png')


    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def virus(self, ctx):
        await ctx.send('The mod is not a virus. Some antivirus software dont like `dll` files. please disable your antivirus or add an exception.')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def rcg(self, ctx):
        await ctx.send('Yes i know my acc name is `RCG` please shut up about it its the default account name')

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
                for index, rule in enumerate(rules, start=1):
                    embed.add_field(name=f"Rule #{index}", value=rule, inline=False)

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

        for index, rule in enumerate(rules):
            embed.add_field(name=f"Rule #{index}", value=rule, inline=False)

        await ctx.send(embed=embed)

    @rule.command(name='1')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _1(self, ctx):
        embed = discord.Embed(
            title='Rule #1',
            description=rules[0],
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
            description=rules[1],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='3')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _3(self, ctx):
        embed = discord.Embed(
            title='Rule #3',
            description=rules[2],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='4')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _4(self, ctx):
        embed = discord.Embed(
            title='Rule #4',
            description=rules[3],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='5')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _5(self, ctx):
        embed = discord.Embed(
            title='Rule #5',
            description=rules[4],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='6')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _6(self, ctx):
        embed = discord.Embed(
            title='Rule #6',
            description=rules[5],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='7')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _7(self, ctx):
        embed = discord.Embed(
            title='Rule #7',
            description=rules[6],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='8')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _8(self, ctx):
        embed = discord.Embed(
            title='Rule #8',
            description=rules[7],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='9')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _9(self, ctx):
        embed = discord.Embed(
            title='Rule #9',
            description=rules[8],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='10')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _10(self, ctx):
        embed = discord.Embed(
            title='Rule #10',
            description=rules[9],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @rule.command(name='11')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def _11(self, ctx):
        embed = discord.Embed(
            title='Rule #11',
            description=rules[10],
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def toastydum(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/854416080717348874/854625562722435072/unknown.png')
    
    @commands.command()
    async def ari(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/854416080717348874/854629185838645268/unknown.png')

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
    async def piss(self, ctx):
        await ctx.send('#pisscult\nhttps://cdn.discordapp.com/attachments/854416080717348874/855376400063660052/unknown.png')

    @commands.command()
    async def toastydum2(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/842450788998578236/855358370708717578/unknown.png')

    @commands.command()
    async def scam(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/850693035826479114/854621486853652480/unknown.png')

    @commands.command()
    async def skid(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/842450788998578236/854336292652187668/unknown.png')

    @commands.command()
    async def html2(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851877985199980624/bruhhhh.gif')

    @commands.command()
    async def api(self, ctx):
        await ctx.send('https://www.aouutils.com/api/v1/\n(totally real)')
    
    @commands.command()
    async def js(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850668209148395524/853954282315710484/unknown.png')
def setup(client):
    client.add_cog(Tags(client))
