import discord
def onlinecount(guild):
    memlist = ['']
    for member in guild.members:
        if member.status != discord.Status.offline:
            memlist.append(member)
    return memlist
