from discord.ext import commands
import discord


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print('AOUUtils is ready')
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.client.get_guild(794950428756410429)
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'AOU | {guild.member_count} members'))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply('The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if you can connect to the server!**')
            blacklist = []
            if message.author.id not in blacklist:
                await self.client.process_commands(message)


def setup(client):
    client.add_cog(Listener(client))
