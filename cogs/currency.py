import discord
from discord.ext import commands
import random as r
import json



class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name='start')
    async def start(self, ctx):
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                print(money[str(ctx.author.id)])
                await ctx.reply('You already have an account')
        except KeyError:
            if ctx.author.id not in self.client.curblack:
                with open('cur.json', 'r') as f:
                    money = json.load(f)
                    money[str(ctx.author.id)] = '500'
                with open('cur.json', 'w') as f:
                    json.dump(money, f, indent=4)
                    await ctx.send('You have made an account! :happyAOUutils:')
            else:
                await ctx.send('blacklist moment')

    @commands.command(aliases=['balance'])
    async def bal(self, ctx, user: discord.Member = None):
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                user = user or ctx.author
                damoney = money[str(user.id)]
                embed = discord.Embed(
                    title = f'{user.name}\'s Balance',
                    description = f'{damoney}✧',
                    colour = discord.Colour.red()
                )
                embed.set_footer(text='👁️👄👁️')
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
                usersmoney = usersmoney + inte
                money[str(ctx.author.id)] = usersmoney
                with open('cur.json', 'w') as f:
                    json.dump(money, f, indent=4)
                    replieswin = [
                        f'You made a mod for minecraft and was paid {inte}✧ by Captain',
                        f'You revived AOU for a few seconds and got paid {inte}✧ by Heapons',
                        f'Toasty paid you {inte}✧ for coding in JavaScript',
                        f'Captain paid you {inte}✧ for coding in python',
                        f'You worked at the bank and stole {inte}✧ while you were there',
                        f'Robin ran past you at work and gave you {inte}✧',
                        f'Arawn paid you {inte}✧ for an among us mod',
                        f'You walked home with Arawn Pierer, they paid you {inte}✧ for keeping them safe on their way home',
                        f'You playtested Arawn Pierers game and found {r.randrange(2, 50, 2)} bugs and Arawn Pierer paid you {inte}✧',
                        f'You helped making AOU work on mobile and was paid {inte}✧ by Angxl',
                        f'You invested in Bitro and got {inte}✧ extra',
                        f'You played dimensionsSMP and someone gave you {r.randrange(1, 5, 2)} diamonds and you made that into {inte}✧',
                        f'You hacked AOUutils and gave yourself {inte}✧'
                    ]
                    await ctx.reply(r.choice(replieswin))
        except KeyError:
            await ctx.reply('You do not yet have an account, create one with `aou start`')
    
    @commands.command()
    @commands.is_owner()
    async def debug(self, ctx):
        with open('cur.json', 'r') as f:
            jason = json.load(f)
            await ctx.send(f'```json\n{jason}```')




def setup(client):
    client.add_cog(Currency(client))
