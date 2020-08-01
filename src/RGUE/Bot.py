import discord
from src.RGUE import Commands
from src.RGUE import DataAccess


class Bot(discord.Client):
    def __init__(self, host, user, password, db):
        super(Bot, self).__init__()
        self.DB = DataAccess.Connection(host, user, password, db)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not message.author.bot and len(message.attachments) == 0 and message.content[0] == '!':
            await Commands.process_command(self, message, self.DB)


def main(key, host, user, password, bd):
    bot = Bot(host, user, password, bd)
    bot.run(str(key))
