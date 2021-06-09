from discord.ext import commands
import discord
import urllib

class Suggest(commands.Cog, name="Suggest"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggest', help="A command to Suggest things!", aliases=['request'])
    async def h(self, ctx, *, Suggestion=None):
        blacklist = []
        if ctx.author.id not in blacklist:
            guild = self.bot.get_guild(850668209148395520)
            chandler = guild.get_channel(851880033428570113)
            if Suggestion != None :
                e = discord.Embed(
                    title = 'Suggestion Sent!',
                    description = Suggestion,
                    colour = discord.Colour.red()
                    )
                e.set_footer(icon_url=ctx.author.avatar_url, text=f'Suggested by {ctx.message.author.name}')
                await chandler.send(embed=e)
            await ctx.reply('Suggestion Sent!')

    @h.error
    async def h_error(self, ctx, error):
        await ctx.send(error)




def setup(bot):
    bot.add_cog(Suggest(bot))
