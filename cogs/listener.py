from discord.ext import commands


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('AOUUtils is ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        if "mobile" in message.content.lower() and "aou" in message.content.lower():
            await message.reply(
                'The AOU Mod is not for mobile.\n**However, the 100 Player Battle Royale mode works on any device if '
                'you can connect to the server!**'
            )

            await self.client.process_commands(message)


def setup(client):
    client.add_cog(Listener(client))
