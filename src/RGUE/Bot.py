from discord.ext import commands
from RGUE import ShameModule
from RGUE import DataAccess
import sys


class BotClient(commands.Bot):
    def __init__(self):
        super(BotClient, self).__init__(command_prefix="!")
        self.add_command(ShameModule.shame)
        self.add_command(ShameModule.get_shame_logs)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))


def main(key):
    bot = BotClient()
    bot.run(str(key))


if __name__ == '__main__':
    DataAccess.host = sys.argv[2]
    DataAccess.user = sys.argv[3]
    DataAccess.password = sys.argv[4]
    DataAccess.database = sys.argv[5]

    db = DataAccess.Connection()
    db.create_databases()

    main(sys.argv[1])
