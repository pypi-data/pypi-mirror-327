class CommandManager:
    def __init__(self, bot, prefix):
        self.bot = bot
        self.prefix = prefix
        self.command_list = {}

    def add_command(self, name, code):
        async def command_handler(message):
            if message.content.startswith(f"{self.prefix}{name}"):
                await message.channel.send(code())
        self.command_list[name] = command_handler
        self.bot.event(self._on_message)

    async def _on_message(self, message):
        for name, handler in self.command_list.items():
            if message.content.startswith(f"{self.prefix}{name}"):
                await handler(message)