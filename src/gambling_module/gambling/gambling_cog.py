from discord.ext import commands
from economy_module.economy import account_cog
import random as rand


class GamblingCog(commands.Cog):
    _gamble_help = "Gamble your points on games of chance!\n" \
                   "Available games:\n" \
                   "random, random20, random50, random100"

    def __init__(self, acc_cog: account_cog.AccountCog):
        super(GamblingCog, self).__init__()
        self._account = acc_cog

    @commands.group(aliases=["gamble"], help=_gamble_help)
    async def bet(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify how you would like to gamble.")

    @bet.command(aliases=["rand", "rand10"])
    async def random10(self, ctx):
        await self._rand_roll(ctx, 10, 1)

    @bet.command(aliases=["rand20"])
    async def random20(self, ctx):
        await self._rand_roll(ctx, 20, 2)

    @bet.command(aliases=["rand50"])
    async def random50(self, ctx):
        await self._rand_roll(ctx, 50, 5)

    @bet.command(aliases=["rand100"])
    async def random100(self, ctx):
        await self._rand_roll(ctx, 100, 19)

    async def _rand_roll(self, ctx, target, multi):
        split = ctx.message.content.split()
        amount = int(split[2])
        withdraw = self._account.withdraw(ctx.author, amount)

        if withdraw != 0:
            await ctx.send("You don't have that many points.")

        rand.seed()
        roll = rand.randint(1, target)

        await ctx.send("Your number is: " + str(roll))

        if roll == target:
            self._account.deposit(ctx.author, amount + amount * multi)

            await ctx.send("You won " + str(amount + amount * multi) + " points!")
        else:
            await ctx.send("You lost...")
