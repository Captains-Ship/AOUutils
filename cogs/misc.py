import discord
from discord.ext import commands
import datetime
from utility.utils import *


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, *, text=" "):
        if text != ' ':
            await ctx.send(text)
        else:
            await ctx.reply('I cannot send nothing')
    
    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title='Info About All Of Us',
            description=f'Owner={ctx.guild.Owner}',
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
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Info about the bot.',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Devs', value='Captain, GingerGigiCat, EnderB0YHD')
        embed.add_field(name='Main Linecount', value=lineCount())




def setup(client):
    client.add_cog(Misc(client))