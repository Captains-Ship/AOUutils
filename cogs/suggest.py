from discord.ext import commands
import discord
import urllib
from logger import logger


class Suggest(commands.Cog, name="Suggest"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggest', help="A command to Suggest things!", aliases=['request'])
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    async def h(self, ctx, *, suggestion=None):
        if suggestion:
            blacklist = [
                             328661975250894850,
                             841330839685431336,
                             675474604533219360,
                             721745855207571627,
                             476549192362229791,
                             468134163493421076
                         ]
            if ctx.author.id not in blacklist:
                guild = self.bot.get_guild(850668209148395520)
                chandler = guild.get_channel(851880033428570113)
                if suggestion is not None:
                    e = discord.Embed(
                        title = 'Suggestion Sent!',
                        description = suggestion,
                        colour = discord.Colour.red()
                        )
                    e.set_footer(icon_url=ctx.author.display_avatar.url, text=f'Suggested by {ctx.message.author.name}')
                    msg = await chandler.send(embed=e)
                    await msg.add_reaction('<a:Yes:850974892366757930>')
                    await msg.add_reaction('<a:X_:850974940282748978>')
                await ctx.reply('Suggestion Sent!')
            else:
                await ctx.reply('blacklist moment')
        else:
            await ctx.send('actually give me a suggestion -_-')

    @h.error
    async def h_error(self, ctx, error):
        await ctx.send(error)




def setup(bot):
    bot.add_cog(Suggest(bot))
