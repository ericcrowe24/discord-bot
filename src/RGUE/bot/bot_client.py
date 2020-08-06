from importlib import util as iuitl
from discord.ext import commands
from RGUE.bot.cogs.shame import shame_cog


class BotClient(commands.Bot):
    def __init__(self, init):
        super(BotClient, self).__init__(command_prefix="!")
        self._setup_cogs(init)

    def _setup_cogs(self, init):
        self.add_cog(shame_cog.ShameCog(self))

        economy = iuitl.find_spec("economy_module")
        if economy is not None:
            self._setup_economy_cog(init)

    def _setup_economy_cog(self, init):
        from economy_module.economy import spending_cog
        from economy_module.economy import account_cog

        self.add_cog(account_cog.AccountCog(self))
        self.add_cog(spending_cog.SpendingCog(self))

        if init:
            self.get_cog("AccountCog").init_tables()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
