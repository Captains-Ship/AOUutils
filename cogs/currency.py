import discord
from discord.ext import commands
import random as r
import json
global ci

ci = '✧'


class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client

    def dev():
        async def predicate(ctx):
            devs = [742976057761726514, 347366054806159360]
            return ctx.author.id in devs
        return commands.check(predicate)

    @commands.command()
    @dev()
    async def bal(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                user = money[str(member.id)]
                wallet = user['wallet']
                bank = user['bank']
                embed = discord.Embed(
                    title=f'{member.name}\'s Balance',
                    description=f'Wallet: {wallet}{ci}\nBank: {bank}{ci}',
                    colour=discord.Colour.red()
                )
                embed.set_footer(text='👁️👄👁️')
                await ctx.send(embed=embed)
        except KeyError:
            if member == ctx.author:
                await ctx.send('You do not have an account yet. Create one with `aou start`.')
            else:
                await ctx.send(f'{member.name} does not have an account yet.')


    @commands.command()
    @dev()
    async def start(self, ctx):
        with open('cur.json', 'r') as f:
            money = json.load(f)
            try:
                print(money[str(ctx.author.id)])
                await ctx.send('You already have an account.')
                return
            except KeyError:
                money[str(ctx.author.id)] = {}
                user = money[str(ctx.author.id)]
                user['bank'] = 500
                user['wallet'] = 500
                user['inventory'] = {}
                inv = user['inventory']
        with open('cur.json', 'w') as f:
            json.dump(money, f, indent=4)
            await ctx.send('You have made an account, and got some sweet starter money!')

    @commands.command()
    @dev()
    async def inv(self, ctx):
        with open('cur.json', 'r') as f:
            money = json.load(f)
            user = money[str(ctx.author.id)]
            inv = user['inventory']
            inventory = ""
            for key in inv:
                amount = inv[key]
                theitem = f'**{key}**: {amount}\n'
                inventory = inventory + theitem
        embed = discord.Embed(
            title = 'Inventory',
            description = inventory,
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'{ctx.author}\'s Inventory')
        await ctx.send(embed=embed)    

    @commands.command()
    @dev()
    async def shop(self, ctx, *, item=None):
        if item == None:
            afford = ", "
            affordnt = ", "
            with open('shop.json', 'r') as f:
                shop = json.load(f)
                with open('cur.json', 'r') as f:
                    users = json.load(f)
                    user = users[str(ctx.author.id)]
                    for key in shop:
                        price = shop[key]['price']
                        if price > user['wallet']:
                            affordnt = affordnt + f", **{key}** ({price}{ci})"
                        else:
                            afford = afford + f", **{key}** ({price}{ci})"
            embed = discord.Embed(
                title='The Shop',
                colour = discord.Colour.red()
            )
            afford = afford.replace(', , ', '')
            affordnt = affordnt.replace(', , ', '')
            if afford == ", ":
                embed.add_field(name='Shit you can afford', value='None lmao broke ass', inline=False)
            else:
                embed.add_field(name='Shit you can afford', value=afford, inline=False)
            if affordnt == ", ":
                embed.add_field(name='Shit you cant afford', value='None lmao rich ass', inline=False)
            else:
                embed.add_field(name='Shit you cant afford', value=affordnt, inline=False)
            await ctx.send(embed=embed)
        else:
            try:
                with open('shop.json', 'r') as f:
                    shop = json.load(f)
                    for key in shop:
                        if str(key).lower().startswith(str(item).lower()):
                            item = shop[key]
                            price = item['price']
                            desc = item['description']
                            embed = discord.Embed(
                                title = 'The Shop',
                                description = f'**{key}**',
                                colour = discord.Colour.red()
                            ).add_field(
                                name='Price',
                                value=f'{price}{ci}'
                            ).add_field(
                                name='Description',
                                value=f'{desc}'
                            )
                            await ctx.send(embed=embed)
                            return
                        elif str(item).lower() in str(key).lower():
                            item = shop[key]
                            price = item['price']
                            desc = item['description']
                            embed = discord.Embed(
                                title = 'The Shop',
                                description = f'**{key}**',
                                colour = discord.Colour.red()
                            ).add_field(
                                name='Price',
                                value=f'{price}{ci}'
                            ).add_field(
                                name='Description',
                                value=f'{desc}'
                            )
                            await ctx.send(embed=embed)
                            return
            except KeyError:
                await ctx.send('Not a valid shop item.')
            await ctx.send('Not a valid shop item.')
                





    @commands.command()
    @commands.cooldown(1, 3600, type=discord.ext.commands.BucketType.user)
    @dev()
    async def work(self, ctx):
        try:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                usersmoneye = money[str(ctx.author.id)]
                usersmoneyee = usersmoneye['wallet']
                usersmoney = int(usersmoneyee)
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
                    money[str(ctx.author.id)]['wallet'] = usersmoney
                elif fail == True:
                    inte = r.randrange(3000, 6000, 2)
                    usersmoney = usersmoney + inte
                    money[str(ctx.author.id)]['wallet'] = usersmoney

                with open('cur.json', 'w') as f:
                    json.dump(money, f, indent=4)
                    replieswin = [
                        f'You made a mod for minecraft and was paid {inte}{ci} by Captain',
                        f'You revived AOU for a few seconds and got paid {inte}{ci} by Heapons',
                        f'Toasty paid you {inte}{ci} for coding in JavaScript',
                        f'Captain paid you {inte}{ci} for coding in python',
                        f'You worked at the bank and stole {inte}{ci} while you were there',
                        f'Robin ran past you at work and gave you {inte}{ci}',
                        f'Arawn paid you {inte}{ci} for an among us mod',
                        f'You walked home with Arawn Pierer, they paid you {inte}{ci} for keeping them safe on their way home',
                        f'You playtested Arawn Pierers game and found {r.randrange(2, 50, 2)} bugs and Arawn Pierer paid you {inte}{ci}',
                        f'You helped making AOU work on mobile and was paid {inte}{ci} by Angxl',
                        f'You invested in Bitro and got {inte}{ci} extra',
                        f'You played dimensionsSMP and someone gave you {r.randrange(1, 5, 2)} diamonds and you made that into {inte}{ci}',
                        f'You hacked AOUutils and gave yourself {inte}{ci}',
                        f'You said piss and Amaan gave you {inte}{ci}'
                    ]
                    repliesloss = [
                        f'You tried to steal money while working at the bank but never got an opportunity to. you were paid {inte}{ci} for an hour of work',
                        f'You were going to work but was beat up on the way there, you got {inte}{ci} for working an hour.',
                        f':) {inte}{ci}',
                        f'You burnt the toast at work and was sent home early. You gained {inte}{ci}',
                        f'You tried to training a pikachu in the Hidden Leaf Village but it didn\'t learn a thing. Paid {inte}{ci} for poor work',
                        f'You got lost while sailing a cruise ship, and was paid {inte}{ci} for a bad 6 days of work',
                        f'You dropped a spoon and was sent home. You got {inte}{ci}',
                        f'I Agree disagreed with you. You got {inte}{ci} for a bad day of work',
                        f'XtraCube banned you with XtraCute and you were paid {inte}{ci} for a bad day of work.'
                    ]
                    if fail == True:
                        await ctx.send(r.choice(repliesloss))
                    else:
                        await ctx.reply(r.choice(replieswin))
        except KeyError:
            await ctx.reply('You do not yet have an account, create one with `aou start`')
    

    @commands.command(aliases=['dep'])
    @dev()
    async def deposit(self, ctx, *, amount: int=0):
        if amount > 0:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                wallet = money[str(ctx.author.id)]['wallet']
                bank = money[str(ctx.author.id)]['bank']
                if amount - 1 < int(wallet):
                    money[str(ctx.author.id)]['wallet'] = wallet - amount
                    money[str(ctx.author.id)]['bank'] = int(bank) + amount
                    await ctx.send('Transaction Complete!')
                else:
                    await ctx.send('not enough money to do this transaction')
            with open('cur.json', 'w') as f:
                json.dump(money, f, indent=4)
        else:
            await ctx.send('Dont try to break me!')

    @commands.command(aliases=['with'])
    @dev()
    async def withdraw(self, ctx, *, amount: int=0):
        if amount > 0:
            with open('cur.json', 'r') as f:
                money = json.load(f)
                wallet = money[str(ctx.author.id)]['wallet']
                bank = money[str(ctx.author.id)]['bank']
                if amount - 1 < int(bank):
                    money[str(ctx.author.id)]['bank'] = bank - amount
                    money[str(ctx.author.id)]['wallet'] = int(wallet) + amount
                    await ctx.send('Transaction Complete!')
                else:
                    await ctx.send('not enough money to do this transaction')
            with open('cur.json', 'w') as f:
                json.dump(money, f, indent=4)
        else:
            await ctx.send('Dont try to break me!')

#1️⃣2️⃣3️⃣4️⃣5️⃣
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                'its not done yet have some patience please.'
                '\nits about 56% done'
            )

def setup(client):
    client.add_cog(Currency(client))
