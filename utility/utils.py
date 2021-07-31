import discord
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
