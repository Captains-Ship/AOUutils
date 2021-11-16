import json
import datetime
import discord
from discord.ext import commands


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
def lineCount():
    with open('AOUUtils.py', 'r') as file:
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
        try:
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
                        multiple = values.get(char, 1)
                        num = int("".join(tempnums))
                        tempnums.clear()
                        nums.append(num * multiple)
                if len(nums) > 0:
                    return Duration(sum(nums))
                else:
                    return -1  # Idk what to put here so I might as well put -1
        except:
            raise commands.BadArgument(f"{argument} is not a valid duration.")


class Duration:
    def __init__(self, seconds):
        self.total_seconds = seconds
        self.weeks, seconds = divmod(seconds, 604800)
        self.days, seconds = divmod(seconds, 86400)
        self.hours, seconds = divmod(seconds, 3600)
        self.minutes, self.seconds = divmod(seconds, 60)
        self.epoch = self.total_seconds + int(datetime.datetime.now().timestamp())  # In case you need to make timestamps, here ya go.

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
