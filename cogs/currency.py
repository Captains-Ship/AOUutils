import json
import random as r
import typing
import discord
from discord.ext import commands

from logger import logger

global ci

ci = '✧'


class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client
    #
    # def dev():
    #     async def predicate(ctx):
    #         devs = [553677148611936267, 742976057761726514, 347366054806159360, 721745855207571627, 535059139999825922]
    #         return ctx.author.id in devs
    #
    #     return commands.check(predicate)
    #
    # @commands.command(description='Shows the current balance in your account or that of the mentioned user.', usage='[user]\n`user`: The user who\'s balance that you want to view, it can be a mention or a user ID.', aliases=['bal'])
    # async def balance(self, ctx, member: discord.Member = None):
    #     member = member or ctx.author
    #     try:
    #         with open('cur.json', 'r') as f:
    #             money = json.load(f)
    #             user = money[str(member.id)]
    #             wallet = user['wallet']
    #             bank = user['bank']
    #             embed = discord.Embed(
    #                 title=f'{member.name}\'s Balance',
    #                 description=f'Wallet: {wallet}{ci}\nBank: {bank}{ci}',
    #                 colour=discord.Colour.red()
    #             )
    #             embed.set_footer(text='👁️👄👁️')
    #             await ctx.send(embed=embed)
    #     except KeyError:
    #         if member == ctx.author:
    #             await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #         else:
    #             await ctx.send(f'{member.name} does not have an account yet.')
    #
    # @commands.command(description='Creates an account in the bot.')
    # async def start(self, ctx):
    #     with open('cur.json', 'r') as f:
    #         money = json.load(f)
    #         try:
    #             print(money[str(ctx.author.id)])
    #             await ctx.send('You already have an account.')
    #             return
    #         except KeyError:
    #             money[str(ctx.author.id)] = {}
    #             user = money[str(ctx.author.id)]
    #             user['bank'] = 500
    #             user['wallet'] = 500
    #             user['inventory'] = {}
    #             inv = user['inventory']
    #     with open('cur.json', 'w') as f:
    #         json.dump(money, f, indent=4)
    #         await ctx.send('You have made an account, and got some sweet starter money!')
    #
    # @commands.command(description='Shows your inventory or that of the mentioned user', aliases=['inv'], usage='[user]\n`user`: The user who\'s inventory that you want to view, it can be a mention or a user ID. This is an optional argument.')
    # async def inventory(self, ctx):
    #     with open('cur.json', 'r') as f:
    #         money = json.load(f)
    #         try:
    #             user = money[str(ctx.author.id)]
    #         except KeyError:
    #             return await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #         inv = user['inventory']
    #         inventory = ""
    #         for key in inv:
    #             amount = inv[key]
    #             theitem = f'**{key}**: {amount}\n'
    #             inventory = inventory + theitem
    #     embed = discord.Embed(
    #         title='Inventory',
    #         description=inventory,
    #         colour=discord.Colour.red()
    #     )
    #     embed.set_footer(text=f'{ctx.author}\'s Inventory')
    #     await ctx.send(embed=embed)
    #
    # @commands.command(description='Opens the shop where you buy goodies!')
    # async def shop(self, ctx, *, item=None):
    #     if item == None:
    #         afford = ""
    #         affordnt = ""
    #         with open('shop.json', 'r') as f:
    #             shop = json.load(f)
    #             with open('cur.json', 'r') as f:
    #                 users = json.load(f)
    #                 try:
    #                     user = users[str(ctx.author.id)]
    #                 except KeyError:
    #                     return await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #                 for key in shop:
    #                     if shop[key]['price'] != -1:
    #                         price = shop[key]['price']
    #                         if price > user['wallet']:
    #                             affordnt = affordnt + f"\n**{key}** ({price}{ci})"
    #                         else:
    #                             afford = afford + f"\n**{key}** ({price}{ci})"
    #         embed = discord.Embed(
    #             title='The Shop',
    #             colour=discord.Colour.red()
    #         )
    #         afford = afford.replace(', , ', '')
    #         affordnt = affordnt.replace(', , ', '')
    #         if afford == ", ":
    #             embed.add_field(name='Shit you can afford', value='None lmao broke ass', inline=False)
    #         else:
    #             embed.add_field(name='Shit you can afford', value=afford, inline=False)
    #         if affordnt == ", ":
    #             embed.add_field(name='Shit you can\'t afford', value='None lmao rich ass', inline=False)
    #         else:
    #             embed.add_field(name='Shit you can\'t afford', value=affordnt, inline=False)
    #         await ctx.send(embed=embed)
    #     else:
    #         try:
    #             with open('shop.json', 'r') as f:
    #                 shop = json.load(f)
    #                 for key in shop:
    #                     if str(key).lower().startswith(str(item).lower()):
    #                         item = shop[key]
    #                         price = item['price']
    #                         desc = item['description']
    #                         embed = discord.Embed(
    #                             title='The Shop',
    #                             description=f'**{key}**',
    #                             colour=discord.Colour.red()
    #                         ).add_field(
    #                             name='Price',
    #                             value=f'{price}{ci}'
    #                         ).add_field(
    #                             name='Description',
    #                             value=f'{desc}'
    #                         )
    #                         await ctx.send(embed=embed)
    #                         return
    #                     elif str(item).lower() in str(key).lower():
    #                         item = shop[key]
    #                         price = item['price']
    #                         desc = item['description']
    #                         embed = discord.Embed(
    #                             title='The Shop',
    #                             description=f'**{key}**',
    #                             colour=discord.Colour.red()
    #                         ).add_field(
    #                             name='Price',
    #                             value=f'{price}{ci}'
    #                         ).add_field(
    #                             name='Description',
    #                             value=f'{desc}'
    #                         )
    #                         await ctx.send(embed=embed)
    #                         return
    #         except KeyError:
    #             await ctx.send('Not a valid shop item.')
    #         await ctx.send('Not a valid shop item.')
    #
    # @commands.command(description='Use this command to work and earn money!')
    # @commands.cooldown(1, 3600, type=discord.ext.commands.BucketType.user)
    # async def work(self, ctx):
    #     try:
    #         with open('cur.json', 'r') as f:
    #             money = json.load(f)
    #             usersmoneye = money[str(ctx.author.id)]
    #             usersmoneyee = usersmoneye['wallet']
    #             usersmoney = int(usersmoneyee)
    #             gained = r.randrange(3000, 6000, 2)
    #             h = ['true', 'false', 'false']
    #             global fail
    #             fail = r.choice(h)
    #             if fail == 'true':
    #                 fail = True
    #             else:
    #                 fail = False
    #             if not fail:
    #                 gained = r.randrange(7000, 12000, 2)
    #                 usersmoney = usersmoney + gained
    #                 money[str(ctx.author.id)]['wallet'] = usersmoney
    #             elif fail:
    #                 gained = r.randrange(3000, 6000, 2)
    #                 usersmoney = usersmoney + gained
    #                 money[str(ctx.author.id)]['wallet'] = usersmoney
    #
    #             with open('cur.json', 'w') as f:
    #                 json.dump(money, f, indent=4)
    #                 replieswin = [
    #                     f'You made a mod for Minecraft and was paid {gained}{ci} by Captain',
    #                     f'You revived AOU for a few seconds and got paid {gained}{ci} by Heapons',
    #                     f'Toasty paid you {gained}{ci} for coding in JavaScript',
    #                     f'Captain paid you {gained}{ci} for coding in Python',
    #                     f'You worked at the bank and stole {gained}{ci} while you were there',
    #                     f'Robin ran past you at work and gave you {gained}{ci}',
    #                     f'Arawn paid you {gained}{ci} for an Among Us mod',
    #                     f'You walked home with Arawn Pierer, they paid you {gained}{ci} for keeping them safe on their way home',
    #                     f'You playtested Arawn Pierer\'s game and found {r.randrange(2, 50, 2)} bugs and Arawn Pierer paid you {gained}{ci}',
    #                     f'You helped AOU work on mobile and was paid {gained}{ci} by Angxl',
    #                     f'You invested in Bitro and got {gained}{ci} extra',
    #                     f'You played dimensionsSMP and someone gave you {r.randrange(1, 5, 2)} diamonds and you made that into {gained}{ci}',
    #                     f'You hacked AOUutils and gave yourself {gained}{ci}',
    #                     f'You said piss and Amaan gave you {gained}{ci}',
    #                     f'You recorded a train and Norway gave you {gained}{ci}'
    #                 ]
    #                 repliesloss = [
    #                     f'You tried to steal money while working at the bank but never got an opportunity to. You were paid {gained}{ci} for an hour of work',
    #                     f'You were going to work but was beat up on the way there, you got {gained}{ci} for working an hour.',
    #                     f':) {gained}{ci}',
    #                     f'You burnt the toast at work and was sent home early. You gained {gained}{ci}',
    #                     f'You tried to training a {r.choice(["Pikachu", "Squirtle", "Bulbasaur", "Charmander"])} in the Hidden Leaf Village but it didn\'t learn a thing. Paid {gained}{ci} for poor work',
    #                     f'You got lost while sailing a cruise ship, and was paid {gained}{ci} for a bad {r.randrange(2, 10, 1)} days of work',
    #                     f'You dropped a spoon and was sent home. You got {gained}{ci}',
    #                     f'I Agree disagreed with you. You got {gained}{ci} for a bad day of work',
    #                     f'XtraCube banned you with XtraCute and you were paid {gained}{ci} for a bad day of work.'
    #                 ]
    #                 if fail:
    #                     await ctx.reply(r.choice(repliesloss))
    #                 else:
    #                     await ctx.reply(r.choice(replieswin))
    #     except KeyError:
    #         await ctx.reply(f'You do not yet have an account, create one with `{ctx.clean_prefix}start`')
    #
    # @commands.command(aliases=['dep'], description='Deposits the specified amount in your bank.', usage='<amount>\n`amount`: The amount of money that you want to deposit. This is a required argument and must be an integer. You may also use "max" or "all".')
    # async def deposit(self, ctx, *, amount: typing.Union[int, str] = 0):
    #     with open('cur.json', 'r') as f:
    #         money = json.load(f)
    #     try:
    #         wallet = money[str(ctx.author.id)]['wallet']
    #         bank = money[str(ctx.author.id)]['bank']
    #     except KeyError:
    #         return await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #     if isinstance(amount, str):
    #         amount = wallet if amount.lower() in ['max', 'all'] else 0
    #     if amount > 0:
    #         if amount - 1 < int(wallet):
    #             money[str(ctx.author.id)]['wallet'] = wallet - amount
    #             money[str(ctx.author.id)]['bank'] = int(bank) + amount
    #             await ctx.send('Transaction Complete!')
    #         else:
    #             await ctx.send('Not enough money to do this transaction.')
    #         with open('cur.json', 'w') as f:
    #             json.dump(money, f, indent=4)
    #     else:
    #         await ctx.send('Don\'t try to break me!')
    #
    # @commands.command(aliases=['with'], description='Withdraws the specified amount from your bank.', usage='<amount>\n`amount`: The amount of money that you want to withdraw. This is a required argument and must be an integer. You may also use "max" or "all".')
    # async def withdraw(self, ctx, *, amount: typing.Union[int, str] = 0):
    #     with open('cur.json', 'r') as f:
    #         money = json.load(f)
    #     try:
    #         wallet = money[str(ctx.author.id)]['wallet']
    #         bank = money[str(ctx.author.id)]['bank']
    #      except KeyError:
    #         return await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #     if isinstance(amount, str):
    #         amount = bank if amount.lower() in ['max', 'all'] else 0
    #     if amount > 0:
    #         if amount - 1 < int(bank):
    #             money[str(ctx.author.id)]['bank'] = bank - amount
    #             money[str(ctx.author.id)]['wallet'] = int(wallet) + amount
    #             await ctx.send('Transaction Complete!')
    #         else:
    #             await ctx.send('Not enough money to do this transaction.')
    #         with open('cur.json', 'w') as f:
    #             json.dump(money, f, indent=4)
    #     else:
    #         await ctx.send('Don\'t try to break me!')
    #
    # @commands.command(description='Sharing is caring! Use this command to give money to others!', usage='<user> <amount>\n`user`: The user that you want to give money to. This is a required argument and must be either a mention or a user ID.\n`amount`: The amount of money that you want to give. This is a required argument and must be an integer.')
    # async def give(self, ctx, user: discord.Member = None, amount: int = 0):
    #     if user != None and user != ctx.author:
    #         if amount > 0:
    #             with open('cur.json', 'r') as f:
    #                 money = json.load(f)
    #                 try:
    #                     author = money[str(ctx.author.id)]
    #                     userlol = money[str(user.id)]
    #                 except KeyError:
    #                     if member == ctx.author:
    #                         return await ctx.send(f'You do not have an account yet. Create one with `{ctx.clean_prefix}start`.')
    #                     return await ctx.send(f'{user.name} does not have an account yet.')
    #                 amon = author['wallet']
    #                 umon = userlol['wallet']
    #                 if int(amon) > amount - 1:
    #                     amon = amon - 1
    #                     umon = umon + amount
    #                     await ctx.send('Transaction Complete!')
    #                 else:
    #                     await ctx.send('Yeah don\'t try to break me please')
    #             with open('cur.json', 'w') as f:
    #                 json.dump(money, f, indent=4)
    #         else:
    #             await ctx.send('Don\'t try to break me!')
    #     else:
    #         await ctx.send('Please enter a user, if you did enter a user make sure it isn\'t you.')
    #
    # @commands.command(description='Use this command to beg for money.\n**NOTE: This is still WIP.**')
    # @dev()
    # async def beg(self, ctx):
    #     await ctx.reply("It's a work in progress mate.")

    @commands.command()
    async def note(self, ctx):
        """
        wondering what happened to currency commands?
        """
        await ctx.send("Currency commands have been deprecated because its useless.\n"
                       "This note will be removed in v1.1.0")  # TODO: remove this in v1.1.0


"""
    #1️⃣2️⃣3️⃣4️⃣5️⃣
"""


async def setup(client):
    await client.add_cog(Currency(client))
