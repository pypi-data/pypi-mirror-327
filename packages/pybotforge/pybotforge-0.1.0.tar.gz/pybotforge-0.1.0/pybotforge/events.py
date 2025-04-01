class EventManager:
    def __init__(self, bot):
        self.bot = bot

    def on_ready(self, callback):
        @self.bot.event
        async def on_ready():
            await callback()

    def on_message(self, callback):
        @self.bot.event
        async def on_message(message):
            await callback(message)