import discord
from discord.ext import commands
import urllib.request, json
from logger import logger
class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def downgrade(self, ctx):
        embed = discord.Embed(
            title="Uh Oh...",
            description="""
            so you know how launchpad is outdated... ***again***

            well Captain decided to make a simple tool to downgrade among us on steam, the version you want is `2021.6.30s`

            the github repo is [here](https://github.com/Captain8771/easy-among-us-depot-downloader), you will need [python 3.9](https://www.python.org/downloads/release/python-390/)

            if there is any issue open a ticket in <#809192430935080960>
            """, color=discord.Color.red())
        m = ctx.message.reference or ctx.message
        if m != ctx.message:
            m = m.resolved
        await m.reply(embed=embed)
 
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def download(self, ctx):
        embed = discord.Embed(
            title="Downloading Launchpad",
            description="""
		Note: You need to be the desktop client and Among Us should **NOT be updated to v2021.11.9 or higher**

		1) Go to <#896112272399794207> and click "Add to Library"

		2) Go to the library tab (below the friends tab in the homepage) and click "Install" on Launchpad

		The mod should install. (If it fails, don't hesitate to create a ticket and ask about it!)

		3) Now click play!

		Make sure to change the server region to "All Of Us: Launchpad"!
            """, color=discord.Color.red())
        m = ctx.message.reference or ctx.message
        if m != ctx.message:
            m = m.resolved
        await m.reply(embed=embed)
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def beta(self, ctx):
        await ctx.send('http://bit.ly/AOUutilsBETA')

    @commands.command()
    async def light(self, ctx):
        await ctx.send("https://media.discordapp.net/attachments/802743745032355850/897544230774374470/unknown.png")

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def whoasked(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/848185124037460070/870343946910466098/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def man(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851472289542307870/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def iasked(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/848185124037460070/870343552503267368/9dc7ec449dd253e92b676d12e3df882013afe91b4cffa144d21133888a4c5390_3.png')

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
    async def python(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850668209148395524/852622410044669955/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def arch(self, ctx):
        await ctx.send('I use Arch btw <:I_Use_arch_btw:861516766115004426>')

    @commands.command()
    async def vedant(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/802743745032355850/861867163845263391/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def badinternet(self, ctx):
        await ctx.send('https://captain.has-no-bra.in/53twyUx2U')

    """
    UTC+5: Vedant (🔰Moderator), Toasty (👨‍💻Developer)

    UTC+2: Captain (🔰Head Staff), Heapons (Manager)
    
    UTC+1: Wulfstrex (👥Community Manager), EnderBoyHD (🔰Admin)
    
    UTC0: Ariana Pierer (🔰Moderator), Shadows (🔰Moderator)
    
    UTC-3: funnynumber (👨‍💻Main-Dev), XtraCube (👨‍💻Main-Dev), Ruthless (🔰Moderator), Neil (🔰Moderator)
    
    UTC-4: Doggo (🔰Moderator), TheDreamChicken (🔰Admin)
    
    UTC-5: Pure (🔰Owner), angxl wtf (🔰Owner), Joshua TDM (👥Community Manager), Skylario (🔰Head Staff), Jameyiscool (🔰Moderator), Pikanaruto (🔰Admin)
    
    UTC-7: Popcat (🔰Moderator)
    """

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def timezones(self, ctx):
        self.timezonelist = [
                'UTC+2: Captain (manager), Heapons (manager)',
                'UTC+1: EnderB0YHD (Admin)',
                'UTC0: Arawn Pierer (Moderator)',
                'UTC-4: TheDreamChicken (Owner)',
                'UTC-5: Joshua TDM (Owner), Pikanaruto (Developer)',

        ]
        await ctx.reply('```py\n' + "\n\n".join(self.timezonelist) + '```')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def masswarn(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/802743745032355850/855073669835390976/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
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

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def blankmail(self, ctx):
        await ctx.send('In the next **24 hours**, please state your issue, or we will consider it a troll mail and warn you. Thanks!')

    @commands.command(aliases=['modmail'])
    async def mail(self, ctx):
        await ctx.send('Please open a modmail thread')

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


    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def toastydum(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/854416080717348874/854625562722435072/unknown.png')
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def toastydum2(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/842450788998578236/855358370708717578/unknown.png')

    @commands.command()
    async def toastydum3(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/850668209148395524/858965742962737172/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def toasty(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850693035826479114/852964926300881017/unknown.png')

    
    

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def joke(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/854416080717348874/854623492989124608/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def tou(self, ctx):
        await ctx.send('we are NOT Town of Us, this is All Of Us.')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def didntask(self, ctx):
        if ctx.message.reference:
            await ctx.message.reference.resolved.reply('https://cdn.discordapp.com/attachments/844943241878831164/861624113525424129/didntask.mp4')
        else:
            await ctx.send('https://cdn.discordapp.com/attachments/844943241878831164/861624113525424129/didntask.mp4')
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def ari(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/854416080717348874/854629185838645268/unknown.png')


    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def piss(self, ctx):
        await ctx.send('#pisscult\nhttps://cdn.discordapp.com/attachments/854416080717348874/855376400063660052/unknown.png')



    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def scam(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/850693035826479114/854621486853652480/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def skid(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/842450788998578236/854336292652187668/unknown.png')

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def html2(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/842450788998578236/851877985199980624/bruhhhh.gif')
        
    @commands.command()
    async def code(self, ctx):
        await ctx.send("Please **DO NOT** put any other codes beside **AOU MOD** as this the All of Us Discord "
                       "Server. If you want any other mod, please consider joining their Discord Server. Also dont "
                       "spam the code too. Thank you")

    
    @commands.command(name='api')
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def apimembercount(self, ctx, *, endpoint=None):
        if endpoint is not None:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:8080/api/v1/{endpoint}") as url:
                    data = url.read().decode()
                    with open('./templates/404.html') as f:
                        h = f.read()
                        if str(data) == str(h):
                            raise Exception('404 NOT FOUND')
                    await ctx.send(f'```json\n{data}```')

            except Exception as e:
                await ctx.send(e)      
        else:
            await ctx.send('bruh')
    


    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def js(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/850668209148395524/853954282315710484/unknown.png')
def setup(client):
    client.add_cog(Tags(client))
