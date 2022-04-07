import asyncio
from functools import partial
from typing import Union, Optional

from discord.ext import commands
import discord


class ButtonType:
    left2 = "<<"
    left1 = "<"
    stop = "[]"
    right1 = ">"
    right2 = ">>"


class BPV(discord.ui.View):
    def __init__(self, ctx, buttons, paginator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx: commands.Context = ctx
        self.btns = buttons
        self.paginator: ButtonPaginator = paginator
        for button in self.btns.keys():
            if self.btns[button] == ButtonType.left2:
                x = self.left2
                x.emoji = button
            elif self.btns[button] == ButtonType.left1:
                x = self.left1
                x.emoji = button
            elif self.btns[button] == ButtonType.stop:
                x = self._stop
                x.emoji = button
            elif self.btns[button] == ButtonType.right1:
                x = self.right1
                x.emoji = button
            elif self.btns[button] == ButtonType.right2:
                x = self.right2
                x.emoji = button

    @discord.ui.button(emoji="", custom_id=ButtonType.left2, style=discord.ButtonStyle.gray)
    async def left2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.paginator._decrease(2)  # noqa

    @discord.ui.button(emoji="", custom_id=ButtonType.left1, style=discord.ButtonStyle.success)
    async def left1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.paginator._decrease(1)  # noqa

    @discord.ui.button(emoji="Capstop:928210625677656074", custom_id=ButtonType.stop, style=discord.ButtonStyle.danger)
    async def _stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.paginator.stop()

    @discord.ui.button(emoji="Capright:928210625669238794", custom_id=ButtonType.right1, style=discord.ButtonStyle.success)
    async def right1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.paginator._increase(1)  # noqa

    @discord.ui.button(emoji="Capright2:928210625652482048", custom_id=ButtonType.right2, style=discord.ButtonStyle.gray)
    async def right2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.paginator._increase(2)  # noqa

    async def on_timeout(self) -> None:
        await self.paginator.stop()


class ButtonPaginator:
    def __init__(self,
                 ctx: commands.Context = None,
                 *,
                 pages: list[Union[discord.Embed, str]],
                 timeout: int = 180,
                 color: discord.Color = discord.Color.og_blurple(),
                 prefix: str = "",
                 suffix: str = "",
                 title: str = "",
                 force_embed=False,
                 buttons: dict = None
                 ):
        self.ctx: commands.Context = ctx
        self.pages: list = pages
        self.timeout: int = timeout
        self.color: discord.Color = color
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.title: str = title
        self.msg: Optional[discord.Message] = None
        self.force_embed: bool = force_embed
        self.index: int = 0
        self.buttons: dict = buttons or {  # ⬅️◀️⏹️▶️➡️
            "\U00002b05": ButtonType.left2,
            "\U000025c0": ButtonType.left1,
            "\U000023f9": ButtonType.stop,
            "\U000025b6": ButtonType.right1,
            "\U000027a1": ButtonType.right2
        }
        self._stopped: bool = False
        self.view: BPV = BPV(ctx=self.ctx, buttons=self.buttons, paginator=self, timeout=self.timeout)

    async def start(self, ctx: Optional[commands.Context] = None):
        """Starts the paginator,
        ctx is only needed if you want to use a different context than the one the paginator was created with"""
        self.ctx = ctx or self.ctx
        await self._handle_sending()
        self.view.ctx = self.ctx

    async def _edit_message(self):
        """
        Edits the message of the paginator
        internal function. dont call unless you know what you are doing.
        """
        if self.msg is None:
            return
        if self.index >= len(self.pages):
            return
        if isinstance(self.pages[self.index], discord.Embed):
            x = self.pages[self.index]
            x.description = self.prefix + x.description or x.title + self.suffix
            x.title = self.title
            await self.msg.edit(content="", embed=x)
        else:
            if self.force_embed:
                x = discord.Embed(title=self.title, description=self.prefix + self.pages[self.index] + self.suffix, color=self.color)
                await self.msg.edit(content="", embed=x)
            else:
                await self.msg.edit(content=self.prefix + self.pages[self.index] + self.suffix, embed=None)

    async def stop(self):
        """Stops the internal paginator."""
        if self._stopped:
            raise RuntimeError("Paginator is already stopped.")
        self._stopped = True
        try:
            self.view.stop()
            await self.msg.edit(view=None)
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def _decrease(self, amount: int):
        """
        decreases the index of the paginator by amount
        internal function. dont call unless you know what you are doing.
        """
        if amount == 2:
            self.index = 0
        else:
            self.index -= amount
            if self.index < 0:
                self.index = 0
        await self._edit_message()

    async def _increase(self, amount: int):
        """
        increases the index of the paginator by amount
        internal function. dont call unless you know what you are doing.
        """
        if amount == 2:
            self.index = len(self.pages) - 1
        else:
            self.index += amount
            if self.index >= len(self.pages):
                self.index = len(self.pages) - 1
        await self._edit_message()

    def _check(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        return user.id == self.ctx.author.id

    async def _handle_sending(self):
        """Handles the sending of the paginator
        internal function. dont call unless you know what you are doing.
        """
        if self.ctx is None:
            raise ValueError(
                "You need to provide a context to start the paginator, do this either in class init or in start()")
        if len(self.pages) == 0:
            raise ValueError("You need to provide at least one page")
        if self.force_embed:
            tobesent = discord.Embed(color=self.color, title=self.title, description=self.pages[self.index] if isinstance(self.pages[self.index], str) else self.pages[self.index].description)
            tobesent.description = self.prefix + tobesent.description + self.suffix
        else:
            if isinstance(self.pages[self.index], str):
                tobesent = self.prefix + self.pages[self.index] + self.suffix
            else:
                tobesent = self.pages[self.index]
                tobesent.description = self.prefix + tobesent.description + self.suffix
        self.msg = await self.ctx.send(content=tobesent if isinstance(tobesent, str) else None, embed=tobesent if isinstance(tobesent, discord.Embed) else None, view=self.view)