import discord
from discord.ext import commands
import datetime
from utility.utils import *


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, *, text=" "):
        if text != ' ':
            await ctx.message.delete()
            await ctx.send(text)
        else:
            await ctx.reply('I cannot send nothing')
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title='Info About All Of Us',
            description=f'Owner={ctx.guild.owner}',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Channels', value=len(ctx.guild.channels))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'requested by {ctx.author}')
        embed.add_field(name='Membercount', value=memcount(ctx.guild))
        embed.add_field(name='Members Online', value=countOnlineMember(ctx.guild))
        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Info about the bot.',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(icon_url=ctx.guild.icon_url, text='Devs: Captain, GingerGigiCat, EnderB0YHD, Toasty')
        embed.add_field(name='Main Linecount', value=lineCount())
        await ctx.reply(embed=embed)
    



    @commands.command()
    @commands.cooldown(1, 15, type=discord.ext.commands.BucketType.user)
    async def staff(self, ctx):
        embed = discord.Embed(
            title = 'Staff Team of AOU',
            description='List of all Staff of AOU',
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )

        android = ctx.guild.get_role(837697914561364008)
        dev = ctx.guild.get_role(794983920848338995)
        adm = ctx.guild.get_role(849669487783444490)
        mod = ctx.guild.get_role(795034661805359134)
        androidteam = []
        devteam = []
        admteam = []
        modteam = []
        rolelist = [837697914561364008, 794983920848338995, 849669487783444490, 795034661805359134]
        teams = ['android team', 'dev team', 'admin team', 'moderator team']
        for m in ctx.guild.members:
            memrol = []
            if m.top_role.id in rolelist:
                if m.top_role == android:
                    androidteam.append(m.name)
                if m.top_role == dev:
                    devteam.append(m.name)
                if m.top_role == adm:
                    admteam.append(m.name)
                if m.top_role == mod:
                    modteam.append(m.name)
            else:
                for role in m.roles:
                    if role.id in rolelist:
                        memrol.append(role)
                memrol.reverse()
                try:
                    if memrol[0] == android:
                        androidteam.append(m.name)
                    if memrol[0] == dev:
                        devteam.append(m.name)
                    if memrol[0] == adm:
                        admteam.append(m.name)
                    if memrol[0] == mod:
                        modteam.append(m.name)
                except:
                    pass
        androidteam = str(androidteam).replace('\', \'', '\n')
        devteam = str(devteam).replace('\', \'', '\n')
        admteam = str(admteam).replace('\', \'', '\n')
        modteam = str(modteam).replace('\', \'', '\n')
        androidteam = str(androidteam).replace('[\'', '\n')
        devteam = str(devteam).replace('[\'', '\n')
        admteam = str(admteam).replace('[\'', '\n')
        modteam = str(modteam).replace('[\'', '\n')
        androidteam = str(androidteam).replace('\']', '\n')
        devteam = str(devteam).replace('\']', '\n')
        admteam = str(admteam).replace('\']', '\n')
        modteam = str(modteam).replace('\']', '\n')
        for team in teams:
            if team == 'android team':
               embed.add_field(name=team, value=androidteam, inline=False)
            if team == 'dev team':
               embed.add_field(name=team, value=devteam, inline=False)
            if team == 'admin team':
               embed.add_field(name=team, value=admteam, inline=False)
            if team == 'moderator team':
               embed.add_field(name=team, value=modteam, inline=False)
                        

        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by {ctx.author}')
        embed.set_author(name='Values may or may not be incorrect due to the wacky way i implemented this.')
        await ctx.reply(embed=embed)



        

def setup(client):
    client.add_cog(Misc(client))