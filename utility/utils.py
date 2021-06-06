import discord


def countOnlineMember(guild):
    memberList = ['']
    for member in guild.members:
        if member.status != discord.Status.offline:
            memberList.append(member)
    return memberList


def lineCount():
    with open('../AOUUtils.py', 'r') as file:
        for i, l in enumerate(file):
            pass

    return i + 1
