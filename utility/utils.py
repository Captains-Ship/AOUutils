import discord


# Members online
def countOnlineMember(guild):
    memberList = []
    for member in guild.members:
        if member.status != discord.Status.offline:
            memberList.append(member)
    return len(memberList)

#lines in main file
def lineCount():
    with open('AOUUtils.py', 'r') as file:
        for i, l in enumerate(file):
            pass

    return i + 1
#membercount
def memcount(guild):
    memlist = []
    for m in guild.members:
        memlist.append(m)
    return len(memlist)
#bot count
def botcount(guild):
    botlist = []
    for m in guild.members:
        if m.bot:
            botlist.append(m)
    return len(botlist)
