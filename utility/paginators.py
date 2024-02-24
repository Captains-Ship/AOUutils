import asyncio
from functools import partial
from typing import Union, Optional

from discord import InteractionResponded
from discord.ext import commands
import discord


class ButtonType:
    left2 = "<<"
    left1 = "<"
    stop = "[]"
    right1 = ">"
    right2 = ">>"


class BPV(discord.ui.View):
    def __init__(self, owner_id, buttons, paginator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner_id: int = owner_id
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
    async def left2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            self.paginator._set_view_interaction(interaction)
            await self.paginator._decrease(2) # noqa

    @discord.ui.button(emoji="", custom_id=ButtonType.left1, style=discord.ButtonStyle.success)
    async def left1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            self.paginator._set_view_interaction(interaction)
            await self.paginator._decrease(1)  # noqa

    @discord.ui.button(emoji="Capstop:928210625677656074", custom_id=ButtonType.stop, style=discord.ButtonStyle.danger)
    async def _stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            await self.paginator.stop()

    @discord.ui.button(emoji="Capright:928210625669238794", custom_id=ButtonType.right1, style=discord.ButtonStyle.success)
    async def right1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            self.paginator._set_view_interaction(interaction)
            await self.paginator._increase(1)  # noqa

    @discord.ui.button(emoji="Capright2:928210625652482048", custom_id=ButtonType.right2, style=discord.ButtonStyle.gray)
    async def right2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            self.paginator._set_view_interaction(interaction)
            await self.paginator._increase(2)  # noqa

    async def on_timeout(self) -> None:
        await self.paginator.stop()


class ButtonPaginator:
    def __init__(self,
                 ctx: commands.Context = None,
                 interaction: discord.Interaction = None,
                 *,
                 pages: list,
                 timeout: int = 180,
                 color: discord.Color = discord.Color.og_blurple(),
                 prefix: str = "",
                 suffix: str = "",
                 title: str = "",
                 force_embed=False,
                 loop: bool = False,
                 buttons: dict = None
                 ):
        if ctx is None and interaction is None:
            raise ValueError("You must provide either a context or an interaction.")
        if ctx is not None and interaction is not None:
            raise ValueError("You must provide either a context or an interaction, not both.")
        self.owner_id: int = interaction.user.id if interaction is not None else ctx.author.id
        self.ctx: Optional[commands.Context] = ctx
        self.interaction: Optional[discord.Interaction] = interaction
        self.pages: list = pages
        self.timeout: int = timeout
        self.color: discord.Color = color
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.title: str = title
        self.force_embed: bool = force_embed
        self.index: int = 0
        self.loop = loop
        self.buttons: dict = buttons or {  # ⬅️◀️⏹️▶️➡️
            "\U00002b05": ButtonType.left2,
            "\U000025c0": ButtonType.left1,
            "\U000023f9": ButtonType.stop,
            "\U000025b6": ButtonType.right1,
            "\U000027a1": ButtonType.right2
        }
        self._stopped: bool = False
        self.__view_interaction: Optional[discord.Interaction] = None
        self.view: BPV = BPV(owner_id=self.owner_id, buttons=self.buttons, paginator=self, timeout=self.timeout)

    @staticmethod
    def entries_to_pages(entries: list, joiner: str = "\n", embed: bool = True):
        """
        Splits entries into pages.
        Set `embed` to True if you want to split the entries to use in embeds. Default is True.

        Why doesn't the paginator accept entries and split it on it's own? Because I don't want to.

        """
        pages = []
        temp = ""
        for entry in entries:
            if len(temp + entry + joiner) < (4096 if embed else 2000):
                temp += entry + joiner
            else:
                pages.append(temp)
                temp = ""
        if temp != "":
            pages.append(temp)
        return pages


    async def start(self):
        """Starts the paginator,
        ctx is only needed if you want to use a different context than the one the paginator was created with"""
        await self._handle_sending()
        self.view.owner_id = self.owner_id

    def _set_view_interaction(self, interaction: discord.Interaction):
        """Set the view interaction for response handling"""
        self.__view_interaction = interaction

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
            await self.__view_interaction.response.edit_message(content="", embed=x)
        else:
            if self.force_embed:
                x = discord.Embed(title=self.title, description=self.prefix + self.pages[self.index] + self.suffix, color=self.color)
                await self.__view_interaction.response.edit_message(content="", embed=x)
            else:
                await self.__view_interaction.response.edit_message(content=self.prefix + self.pages[self.index] + self.suffix, embed=None)

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
            self.index = (len(self.pages) - 1) if self.loop and self.index <= 0 else 0
        else:
            self.index -= amount
            if self.index < 0:
                self.index = (len(self.pages) - 1) if self.loop else 0
        await self._edit_message()

    async def _increase(self, amount: int):
        """
        increases the index of the paginator by amount
        internal function. dont call unless you know what you are doing.
        """
        if amount == 2:
            self.index = 0 if self.loop and self.index >= (len(self.pages) - 1) else len(self.pages) - 1
        else:
            self.index += amount
            if self.index >= len(self.pages):
                self.index = 0 if self.loop else (len(self.pages) - 1)
        await self._edit_message()

    def _check(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        return user.id == self.owner_id

    async def _handle_sending(self):
        """Handles the sending of the paginator
        internal function. dont call unless you know what you are doing.
        """
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
        if self.interaction is not None:
            try:
                self.msg = await self.interaction.response.send_message(content=tobesent if isinstance(tobesent, str) else None, embed=tobesent if isinstance(tobesent, discord.Embed) else None, view=self.view)
            except InteractionResponded:
                self.msg = await self.interaction.followup.send(
                    content=tobesent if isinstance(tobesent, str) else None,
                    embed=tobesent if isinstance(tobesent, discord.Embed) else None, view=self.view)
            return
        self.msg = await self.ctx.send(content=tobesent if isinstance(tobesent, str) else None, embed=tobesent if isinstance(tobesent, discord.Embed) else None, view=self.view)
        