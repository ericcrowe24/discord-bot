from discord.ext import commands
from RGUE.Cogs.Shame import ShameCog
from RGUE.Cogs.Economy import AccountCog
from RGUE.Cogs.Economy import SpendingCog


class BotClient(commands.Bot):
    def __init__(self, init):
        super(BotClient, self).__init__(command_prefix="!")
        self.add_cog(ShameCog.ShameCog(self))
        self.add_cog(AccountCog.AccountCog(self))
        self.add_cog(SpendingCog.SpendingCog(self))

        if init:
            self._init_database()

    def _init_database(self):
        print("Creating shame tables...")
        self.get_cog("ShameCog").init_tables()
        print("Creating economy tables...")
        self.get_cog("AccountCog").init_tables()
        pass

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
