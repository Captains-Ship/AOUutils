import discord

# Members online
def countOnlineMember(guild):
    memberList = ['']
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

def memcount(guild):
    memlist = ['']
    for m in guild.members:
        memlist.append(m)
    return len(m) #test commit