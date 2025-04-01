import discord
from .commands import CommandManager
from .events import EventManager

class PyBotForgeClient:
    def __init__(self, token, prefix, intents=None):
        self.token = token
        self.prefix = prefix
        self.intents = intents or discord.Intents.default()
        self.bot = discord.Client(intents=self.intents)
        self.commands = CommandManager(self.bot, prefix)
        self.events = EventManager(self.bot)

    def run(self):
        self.bot.run(self.token)