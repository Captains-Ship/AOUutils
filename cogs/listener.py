from discord.ext import commands


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('AOUUtils is ready')


def setup(client):
    client.add_cog(Listener(client))
