import discord
from discord.ext import commands
import random as r
import json
global currencyicon
currencyicon = '✧'


class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.command()
    @commands.is_owner()
    async def list(self, ctx, member: discord.Member, type='currency', *, reason='None Provided'):
        if member == ctx.author:
            await ctx.send('no')
        else:
            if True:
    
                with open('blacklist.json', 'r') as f:
                    jason = json.load(f)
                    jason[member.id] = {}
                    jason[member.id]['type'] = type
                    jason[member.id]['reason'] = reason
                with open('blacklist.json', 'w') as f:
                    json.dump(jason, f, indent=4)


    @commands.command(name='start')
    @commands.has_role('Elite')
    async def start(self, ctx):
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                print(money[str(ctx.author.id)])
                await ctx.reply('You already have an account')
        except KeyError:
            with open('blacklist.json', 'r') as fools:

                bl = json.load(fools)

                try:
                    bl2 = bl[str(ctx.author.id)]
                    if bl2['type'] == 'currency':
                        bl3 = bl2['reason']
                        await ctx.send(f'You have been blacklisted for `{bl3}`')
                except KeyError:
                    with open('cur.json', 'r') as f:
                        money = json.load(f)
                        money[str(ctx.author.id)] = '500'
                    with open('cur.json', 'w') as f:
                        json.dump(money, f, indent=4)
                        await ctx.send('You have made an account! :happyAOUutils:')


    @commands.command(aliases=['balance'])
    async def bal(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        if user.bot:
            await ctx.send('no')
        else:
            try:
                with open('cur.json', 'r') as f:
                    money = json.load(f)
                    damoney = money[str(user.id)]
                    embed = discord.Embed(
                        title = f'{user.name}\'s Balance',
                        description = f'{damoney}{currencyicon}',
                        colour = discord.Colour.red()
                    )
                    embed.set_footer(text='AOUutils is still receiving updates relatively quick! no guarantees your things will be saved')
                    await ctx.send(embed=embed)
            except KeyError:
                if user == ctx.author:
                    await ctx.reply('You do not yet have an account, create one with `aou start`')
                else:
                    await ctx.reply(f'{user} Does not have an account yet.')
    
    @commands.command()
    @commands.cooldown(1, 3600, type=discord.ext.commands.BucketType.user)
    async def work(self, ctx):
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                usersmoney = int(money[str(ctx.author.id)])
                inte = r.randrange(3000, 6000, 2)
                h = ['true', 'false', 'false']
                global fail
                fail = r.choice(h)
                if fail == 'true':
                    fail = True
                else:
                    fail = False
                if fail == False:
                    inte = r.randrange(7000, 12000, 2)
                    usersmoney = usersmoney + inte
                    money[str(ctx.author.id)] = usersmoney
                elif fail == True:
                    inte = r.randrange(3000, 6000, 2)
                    usersmoney = usersmoney + inte
                    money[str(ctx.author.id)] = usersmoney

                with open('cur.json', 'w') as f:
                    json.dump(money, f, indent=4)
                    replieswin = [
                        f'You made a mod for minecraft and was paid {inte}{currencyicon} by Captain',
                        f'You revived AOU for a few seconds and got paid {inte}{currencyicon} by Heapons',
                        f'Toasty paid you {inte}{currencyicon} for coding in JavaScript',
                        f'Captain paid you {inte}{currencyicon} for coding in python',
                        f'You worked at the bank and stole {inte}{currencyicon} while you were there',
                        f'Robin ran past you at work and gave you {inte}{currencyicon}',
                        f'Arawn paid you {inte}{currencyicon} for an among us mod',
                        f'You walked home with Arawn Pierer, they paid you {inte}{currencyicon} for keeping them safe on their way home',
                        f'You playtested Arawn Pierers game and found {r.randrange(2, 50, 2)} bugs and Arawn Pierer paid you {inte}{currencyicon}',
                        f'You helped making AOU work on mobile and was paid {inte}{currencyicon} by Angxl',
                        f'You invested in Bitro and got {inte}{currencyicon} extra',
                        f'You played dimensionsSMP and someone gave you {r.randrange(1, 5, 2)} diamonds and you made that into {inte}{currencyicon}',
                        f'You hacked AOUutils and gave yourself {inte}{currencyicon}',
                        f'You said piss and Amaan gave you {inte}{currencyicon}'
                    ]
                    repliesloss = [
                        f'You tried to steal money while working at the bank but never got an opportunity to. you were paid {inte}{currencyicon} for an hour of work'
                    ]
                    if fail == True:
                        await ctx.send(r.choice(repliesloss))
                    else:
                        await ctx.reply(r.choice(replieswin))
        except KeyError:
            await ctx.reply('You do not yet have an account, create one with `aou start`')
    
    @commands.command()
    @cap()
    async def shop(self, ctx):
        try:
            with open('shop.json', 'r') as f:
                shop = json.load(f)
                paginator = commands.Paginator()
                for key in shop:
                    value = shop[key]
                    paginator.add_line(f'{key}: {value}{currencyicon}')


                for page in paginator.pages:
                    await ctx.send(page)
        except KeyError:
            await ctx.reply('You do not yet have an account, create one with `aou start`')




def setup(client):
    client.add_cog(Currency(client))
