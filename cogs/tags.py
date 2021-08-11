import discord
from discord.ext import commands
import urllib.request, json
from logger import logger
class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def beta(self, ctx):
        await ctx.send('http://bit.ly/AOUutilsBETA')

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



    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def timezones(self, ctx):
        await ctx.reply('```UTC+5: Vedant (🔰Moderator), Toasty (👨‍💻Developer)\n\nUTC+2: Captain (🔰Head Staff), Heapons (Manager)\n\nUTC+1: Wulfstrex (👥Community Manager), EnderBoyHD (🔰Admin)\n\nUTC0: Ariana Pierer (🔰Moderator), Shadows (🔰Moderator)\n\nUTC-3: funnynumber (👨‍💻Main-Dev), XtraCube (👨‍💻Main-Dev), Ruthless (🔰Moderator), Neil (🔰Moderator)\n\nUTC-4: Doggo (🔰Moderator), TheDreamChicken (🔰Admin)\n\nUTC-5: Pure (🔰Owner), angxl wtf (🔰Owner), Joshua TDM (👥Community Manager), Skylario (🔰Head Staff), Jameyiscool (🔰Moderator), Pikanaruto (🔰Admin)\n\nUTC-7: Popcat (🔰Moderator)```')

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
        await ctx.send('we are NOT town of us. this is all of us.')

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
                with urllib.request.urlopen(f"http://127.0.0.1:22023/api/v1/{endpoint}") as url:
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
