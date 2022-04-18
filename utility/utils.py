import json
import datetime
from abc import ABC

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import asqlite

class database:
    def __init__(self, conn=None, cursor=None):
        if not conn or not cursor:
            raise Exception("Please instantiate this class by doing 'database.init()' instead")
        self.conn = conn
        self.cur = cursor

    async def execute(self, *args, **kwargs):
        x = await self.cur.execute(*args, **kwargs)
        await self.conn.commit()
        return x

    async def exec(self, *args, **kwargs):
        return await self.execute(*args, **kwargs)

    @classmethod
    async def init(cls, db_name):
        db = await asqlite.connect(db_name + ".sqlite")
        return cls(conn=db, cursor=await db.cursor())


def dev():
        async def predicate(ctx):
            devs = [553677148611936267, 742976057761726514, 347366054806159360, 721745855207571627, 535059139999825922, 813770420758511636]
            return ctx.author.id in devs

        return commands.check(predicate)


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    return (proc, stdout, stderr)


def getconfig(config: str = 'config'):
    if config == 'config':
        with open('config.json', 'r') as config:
            return json.load(config)
    elif config == 'cur':
        with open('cur.json', 'r') as f:
            return json.load(f)
    elif config == 'warn':
        with open('warns.json', 'r') as f:
            return json.load(f)


# Members online
def countOnlineMember(guild):
    memberList = []
    for member in guild.members:
        if member.status != discord.Status.offline:
            memberList.append(member)
    return len(memberList)


# lines in main file
def lineCount(filename: str):
    with open(filename, 'r') as file:
        for i, l in enumerate(file):
            pass

    return i + 1


# membercount
def memcount(guild):
    memlist = []
    for m in guild.members:
        memlist.append(m)
    return len(memlist)


# bot count
def botcount(guild):
    botlist = []
    for m in guild.members:
        if m.bot:
            botlist.append(m)
    return len(botlist)


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():  # Argument is in seconds
            return Duration(int(argument))
        else:
            values = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
            nums = []
            tempnums = []
            for char in argument:
                if char.isdigit():
                    tempnums.append(char)
                else:
                    multiple = values.get(char)
                    if multiple is None:
                        raise commands.BadArgument(f"{argument} is not a valid duration.")
                    num = int("".join(tempnums))
                    tempnums.clear()
                    nums.append(num * multiple)
            if len(nums) > 0:
                return Duration(sum(nums))
            else:
                return -1  # Idk what to put here so I might as well put -1

class Duration:
    def __init__(self, seconds):
        self.total_seconds = seconds
        self.weeks, seconds = divmod(seconds, 604800)
        self.days, seconds = divmod(seconds, 86400)
        self.hours, seconds = divmod(seconds, 3600)
        self.minutes, self.seconds = divmod(seconds, 60)
        self.epoch = self.total_seconds + int(datetime.datetime.now().timestamp())  # In case you need to make timestamps, here ya go.

    def __repr__(self):
        return f"<Duration: {self.total_seconds} seconds; {self.__str__()}>"

    def __add__(self, other):
        return Duration(self.total_seconds + other.total_seconds)

    def __sub__(self, other):
        return Duration(self.total_seconds - other.total_seconds)

    def __gt__(self, other):
        return self.total_seconds > other.total_seconds

    def __lt__(self, other):
        return self.total_seconds < other.total_seconds

    def __le__(self, other):
        return self.total_seconds <= other.total_seconds

    def __ge__(self, other):
        return self.total_seconds >= other.total_seconds

    def __eq__(self, other):
        return self.total_seconds == other.total_seconds

    def __ne__(self, other):
        return self.total_seconds != other.total_seconds

    def __str__(self):
        temp = [
            f"{self.weeks} week" + ("s" if self.weeks != 1 else "") if self.weeks > 0 else "",
            f"{self.days} day" + ("s" if self.days != 1 else "") if self.days > 0 else "",
            f"{self.hours} hour" + ("s" if self.hours != 1 else "") if self.hours > 0 else "",
            f"{self.minutes} minute" + ("s" if self.minutes != 1 else "") if self.minutes > 0 else "",
            f"{self.seconds} second" + ("s" if self.seconds != 1 else "") if self.seconds > 0 else ""
        ]
        temp = list(filter(lambda x: x != "", temp))
        if len(temp) > 1:
            temp[len(temp) - 1] = "and " + temp[len(temp) - 1]
        return ", ".join(temp)

    def __int__(self):
        return self.total_seconds

    def time_left(self) -> int:  # Returns the time left in seconds.
        return self.epoch - int(datetime.datetime.now().timestamp())


class DurationTransformer(app_commands.Transformer):
    @classmethod
    async def transform(cls, interaction: discord.Interaction, value: str):
        if value.isdigit():
            return Duration(int(value))
        else:
            values = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
            nums = []
            tempnums = []
            for char in value:
                if char.isdigit():
                    tempnums.append(char)
                else:
                    multiple = values.get(char)
                    if multiple is None:
                        return -1  # Temporary measure till I figure out which Exception to raise.
                    num = int("".join(tempnums))
                    tempnums.clear()
                    nums.append(num * multiple)
            if len(nums) > 0:
                return Duration(sum(nums))
            else:
                return -1

class ctx(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locale = None
        if self.interaction:
            self.locale = self.interaction.locale
        else:
            self.locale = self.guild.preferred_locale
        if not self.locale:
            self.locale = "en-US"
        self.locale = str(self.locale)

class Response:
    def __init__(self, locale: str):
        self.locale = locale
        self._responses = {
            "en-US": {
                "cant_echo_blank": 'I cannot send nothing',
                "conv_bin_to_ascii": 'Converted Binary to ASCII',
                "req_by": 'Requested by {}',
                "info_title": 'Info About {}',
                "info_owner": 'Owner: {}',
                "channels": 'Channels',
                "roles": 'Roles',
                "member_count": 'MemberCount',
                "members_online": 'Members Online',
                "ping": 'Ping',
                "staff_team_title": 'Staff Team of AOU',
                "staff_team_desc": 'List of all Staff of AOU',
                "wacky_imp": 'Values may or may not be incorrect due to the wacky way i implemented this.',
                "join_date": 'Join Date',
                "creation_date": 'Creation Date',
                "conv_hex_to_ascii": 'Converted Hex to ASCII',
                "purge_cmd": 'Purge Command',
                "purged": 'Purged {} message(s)',
                "purge_none": 'ah yes purge nothing',
                "max_purge": 'Max to purge is `300`',
                "bot_cant_ban": 'above my top role, cant ban',
                "role_hierarchy": '**__Your top role is below their top role.__**',
                "kick_none": 'You need to specify a user to kick.',
                "missing_member": 'You need to specify a member.',
                "member_not_banned": 'Member isn\'t banned!',
                "member_not_warned": 'This member has not been warned before!',
                "missing_id": 'You need to specify an ID.',
                "member_gone": 'Member is not in this server.',
                "invalid_id": 'Invalid ID.',
                "warn_revoked": 'Warning with ID {0} logged against **{1}** has been revoked.',
                "warns_cleared": 'All warnings against **{}** have been revoked.',
                "afk_set": '{0} i set your afk: {1}',
                "toggle": 'Successfully toggled to `{}`!',
                "no_afk_perms": 'You do not have the permission to remove other\'s afk.',
                "afk_removed": '{0} I have removed {1} AFK.',
                "not_afk": '{} are not afk',
                "cooldown_min": 'This command is on cooldown. Please wait {0} minutes and {1} seconds.',
                "cooldown_sec": 'This command is on cooldown. Please wait {} seconds.',
                "unknown_cmd": 'Unknown command "{}"',
                "unknown_cmd_long": 'I do not recognize this command. run `{}help` for a list of commands.',
                "unowner": 'You are not the owner of this bot.',
                "member_not_found": 'The member that you\'ve mentioned isn\'t in this server or does not exist.',
                "not_int": 'You did not provide a valid number.',
                "missing_arg": 'missing argument(s) `{}`',
                "check_fail": 'You are probably not allowed to use this command.',
                "unknown_error": 'Error, This has been reported to the developers!\n{}'
            }
        }
        self._responses["en-GB"] = self._responses["en-US"]

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, item):
        r = self._responses.get(self.locale, None)
        if r is None:
            r = self._responses["en-US"]
        r = r.get(item, None) or self._responses["en-US"].get(item, None)
        if r is None:
            raise AttributeError(f"Response object has no translation for {item}")
        return r