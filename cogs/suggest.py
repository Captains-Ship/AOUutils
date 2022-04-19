import discord
from discord.ext import commands
import urllib
from logger import logger

import config


class Suggest(commands.Cog, name="Suggest"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='suggest', description="A command to Suggest things!", aliases=['request'],
                             usage="<suggestion>\n`suggestion`: The suggestion that you want to give. This is a required argument.")
    @commands.cooldown(1, 5, type=discord.ext.commands.BucketType.user)
    @discord.app_commands.guilds(config.slash_guild)
    @discord.app_commands.describe(suggestion="The suggestion that you want to give.")
    async def h(self, ctx: commands.Context, *, suggestion: str = None) -> None:
        if suggestion:
            blacklist = [
                328661975250894850,
                841330839685431336,
                675474604533219360,
                721745855207571627,
                476549192362229791,
                468134163493421076,
                849939032410030080
            ]
            if ctx.author.id not in blacklist:
                guild = self.bot.get_guild(850668209148395520)
                chandler = guild.get_channel(851880033428570113)
                if suggestion is not None:
                    e = discord.Embed(
                        title='Suggestion Sent!',
                        description=suggestion,
                        colour=discord.Colour.red()
                    )
                    e.set_footer(icon_url=ctx.author.display_avatar.url, text=f'Suggested by {ctx.message.author.name}')
                    msg = await chandler.send(embed=e)
                    await msg.add_reaction('<a:Yes:850974892366757930>')
                    await msg.add_reaction('<a:X_:850974940282748978>')
                await ctx.reply('Suggestion Sent!')
            else:
                await ctx.reply('blacklist moment')
        else:
            if ctx.interaction is not None:
                return await ctx.interaction.response.send_modal(SuggestModal())
            await ctx.send('actually give me a suggestion -_-')

    @h.error
    async def h_error(self, ctx: commands.Context, error: Exception) -> None:
        await ctx.send(error)


class SuggestModal(discord.ui.Modal, title="Suggest a new feature!"):
    suggestion = discord.ui.TextInput(label="Suggestion", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild = interaction.client.get_guild(850668209148395520)
        chandler = guild.get_channel(851880033428570113)
        if self.suggestion.value is not None:
            e = discord.Embed(
                title='Suggestion Sent!',
                description=self.suggestion.value,
                colour=discord.Colour.red()
            )
            e.set_footer(icon_url=interaction.user.display_avatar.url, text=f'Suggested by {interaction.user.name}')
            msg = await chandler.send(embed=e)
            await msg.add_reaction('<a:Yes:850974892366757930>')
            await msg.add_reaction('<a:X_:850974940282748978>')
        await interaction.response.send_message('Suggestion Sent!')


async def setup(bot) -> None:
    await bot.add_cog(Suggest(bot))
