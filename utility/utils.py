import discord
from discord.ext import commands
import json


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


class Duration(commands.Converter):
    async def convert(self, ctx, argument) -> int:
        try:
            if argument.isdigit():  # Argument is in seconds
                return int(argument)
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
                    return sum(nums)
                else:
                    return -1
        except:
            raise commands.BadArgument(f"{argument} is not a valid duration.")
