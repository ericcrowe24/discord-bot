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
