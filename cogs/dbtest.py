import discord
from discord.ext import commands
import sqlite3
from sqlite3 import Error
from logger import logger


def connect(path='config.db'):
    try:
        if connection:
            logger.error('There is already an active database connection.')
            return
        connection = sqlite3.connect(path)
        return connection
    except Error as e:
        logger.error(f'Database failed to load due to the following error:')
        logger.error(str(e))


class Dbtest(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Dbtest(client))
