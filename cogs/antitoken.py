from github import Github
from discord.ext import commands
from utility.utils import getconfig
from regex import regex

global g
g = Github(getconfig()['tokens']['github'])


class Antitoken(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.github = g

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 850668209148395520: return
        for word in message.content.split(' '):
            a = regex.match(r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})', message.content)
            if a is not None:
                try:
                    await message.reply('```py\nToken detected.\nSending to github for invalidation...```')
                except:
                    pass
                # If you need write access, contact captian.
                repo = g.get_repo("Captains-Ship/anti-token")
                repo.create_file("token.txt", "antitoken", word)
                contents = repo.get_contents("token.txt")
                repo.delete_file(contents.path, "cleaning up", contents.sha)
                return


def setup(client):
    client.add_cog(Antitoken(client))
