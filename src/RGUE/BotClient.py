from discord.ext import commands
from RGUE import ShameCog


class BotClient(commands.Bot):
    def __init__(self):
        super(BotClient, self).__init__(command_prefix="!")
        self.add_cog(ShameCog.ShameCog(self))

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
