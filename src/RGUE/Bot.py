from discord.ext import commands
from RGUE import DataAccess
from RGUE import ShameModule


class Bot(commands.Bot):
    def __init__(self, host, user, password, db, init):
        super(Bot, self).__init__(command_prefix="!")
        DataAccess.Connection.initialize(host, user, password, db)
        self.add_command(ShameModule.shame)
        self.add_command(ShameModule.get_shame_logs)

        if init:
            DataAccess.Connection.get_instance().create_databases()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))


def main(key, host, user, password, bd, init=False):
    bot = Bot(host, user, password, bd, init)
    bot.run(str(key))
