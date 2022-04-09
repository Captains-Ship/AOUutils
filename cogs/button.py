import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
import string
import random

import config
from logger import logger


class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.

    @discord.ui.button(emoji='<a:Yes:850974892366757930>', label='Confirm', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        if str(self.ctx.author.id) != str(interaction.user.id):
            return await interaction.response.send_message('not yours dumdum', ephemeral=True)
        await interaction.response.send_message('The end is near...', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(emoji='<a:X_:850974940282748978>', label='Cancel', style=discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(self.ctx.author.id) != str(interaction.user.id):
            return await interaction.response.send_message('not yours dumdum', ephemeral=True)
        await interaction.response.send_message('Cancelling, your account is safe!', ephemeral=True)
        self.value = False
        self.stop()


class Poll(discord.ui.View):
    def __init__(self, ctx, question):
        super().__init__()
        self.ctx = ctx
        self.yes = []
        self.no = []
        self.question = question
        self.timeout = None

    @discord.ui.button(emoji='\U0001f44d', style=discord.ButtonStyle.green)
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) == (str(self.ctx.user.id) if isinstance(self.ctx, discord.Interaction) else str(self.ctx.author.id)):
            return await interaction.response.send_message('You cant vote on your own polls!', ephemeral=True)
        if interaction.user in self.no:
            self.no.remove(interaction.user.id)
        if interaction.user in self.yes:
            self.yes.remove(interaction.user.id)
            del interaction.message.embeds[0]
            embed = discord.Embed(
                title='Poll',
                description=self.question
            )
            embed.add_field(name="People agreeing:", value=f"{len(self.yes)}", inline=True)
            embed.add_field(name="People disagreeing:", value=f"{len(self.no)}", inline=True)
            await interaction.message.edit(embed=embed)
            return await interaction.response.send_message('Revoked!', ephemeral=True)
        self.yes.append(interaction.user.id)
        del interaction.message.embeds[0]
        embed = discord.Embed(
            title='Poll',
            description=self.question
        )
        embed.add_field(name="People agreeing:", value=f"{len(self.yes)}", inline=True)
        embed.add_field(name="People disagreeing:", value=f"{len(self.no)}", inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message('Vote has been registered', ephemeral=True)

    @discord.ui.button(emoji='\U0001f44e', style=discord.ButtonStyle.red)
    async def disagree(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) == (str(self.ctx.user.id) if isinstance(self.ctx, discord.Interaction) else str(self.ctx.author.id)):
            return await interaction.response.send_message('You cant vote on your own polls!', ephemeral=True)
        if interaction.user in self.yes:
            self.yes.remove(interaction.user.id)
        if interaction.user in self.no:
            self.no.remove(interaction.user.id)
            del interaction.message.embeds[0]
            embed = discord.Embed(
                title='Poll',
                description=self.question
            )
            embed.add_field(name="People agreeing:", value=f"{len(self.yes)}", inline=True)
            embed.add_field(name="People disagreeing:", value=f"{len(self.no)}", inline=True)
            await interaction.message.edit(embed=embed)
            return await interaction.response.send_message('Revoked!', ephemeral=True)
        self.no.append(interaction.user)
        del interaction.message.embeds[0]
        embed = discord.Embed(
            title='Poll',
            description=self.question
        )
        embed.add_field(name="People agreeing:", value=f"{len(self.yes)}", inline=True)
        embed.add_field(name="People disagreeing:", value=f"{len(self.no)}", inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message('Vote has been registered', ephemeral=True)

    @discord.ui.button(label="END", style=discord.ButtonStyle.red)
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != (str(self.ctx.user.id) if isinstance(self.ctx, discord.Interaction) else str(self.ctx.author.id)):
            return await interaction.response.send_message('You arent the creator of this poll!', ephemeral=True)
        embed = discord.Embed(
            title='Results'
        )
        embed.add_field(name=f'People agreeing: {len(self.yes)}', value="\n".join([str(m) for m in self.yes]) or "None", inline=True)
        embed.add_field(name=f'People disagreeing: {len(self.no)}', value="\n".join([str(m) for m in self.no]) or "None", inline=True)
        self.stop()
        await interaction.message.edit(view=None, content='Poll Ended!')
        await self.ctx.channel.send(embed=embed)


class Nitro(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.green)
    async def accept(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('https://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825',
                                                ephemeral=True)
        print(f'lmao {interaction.user} got trolled')


class Button(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poll(self, ctx, *, question=None):
        if not question:
            return await ctx.reply('nice question!')
        poller = Poll(ctx, question)
        embed = discord.Embed(
            title='Poll',
            description=question
        )
        await ctx.send(embed=embed, view=poller)

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.describe(question="The question that you want to ask.")
    @app_commands.guilds(config.slash_guild)
    async def poll_slash(self, interaction: discord.Interaction, question: str) -> None:
        poller = Poll(interaction, question)
        embed = discord.Embed(
            title='Poll',
            description=question
        )
        await interaction.response.send_message(embed=embed, view=poller)

    @commands.command()
    async def nitro(self, ctx):
        embed = discord.Embed(
            title='A WILD GIFT APPEARS!',
            description='**Nitro**\nExpires in 47 hours',
        )
        embed.set_thumbnail(url='https://i.imgur.com/w9aiD6F.png')
        nitro = Nitro()

        def id_generator(size=8, chars=string.ascii_letters + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        a = id_generator(chars=string.ascii_letters)
        await ctx.send(f'discord.com/gifts\/{a}', embed=embed, view=nitro)
        await ctx.message.delete()

    @commands.command()
    async def delete_account(self, ctx: commands.Context):

        view = Confirm(ctx)
        view.author = str(ctx.author.id)
        embed = discord.Embed(
            title='Are You Sure?!?!?',
            description='Deleting your account is **PERMANENT**. ARE YOU ABSOLUTELY SURE?!??!?!',
            colour=discord.Colour.from_rgb(255, 0, 0)

        )
        embed.set_footer(text="Captain will NOT revert this.")
        msg = await ctx.reply('Are you sure you want to delete your AOU account?\n**THIS CANNOT BE UNDONE!**',
                              embed=embed, view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            await msg.edit('Timed Out! Cancelling.', embed=None, view=None)
        elif view.value:
            print('Confirmed...')
            await msg.edit('Confirmed! Delete Started!.', embed=None, view=None)
            with open('cur.json', 'r') as f:
                cur = json.load(f)
                try:
                    del cur[str(ctx.author.id)]
                except KeyError:
                    return await ctx.reply('you do not have an account.')
            with open('cur.json', 'w') as f:
                json.dump(cur, f, indent=4)
            await asyncio.sleep(1)
            await msg.edit('Deleted. :(', embed=None, view=None)
        else:
            print('Cancelled...')
            await msg.edit('Cancelled! Stopping.', embed=None, view=None)


async def setup(client):
    await client.add_cog(Button(client))
