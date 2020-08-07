from discord.ext import commands
from economy_module.economy import account_access
from ark_bot.bot.data_access.shame_connection import ShameConnection


class SpendingCog(commands.Cog):
    @commands.group()
    async def spend(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify how you would like to spend your points")

    @spend.command(help="Spend points to reduce your shame count by 1.")
    async def shame(self, ctx):
        account = account_access.get_account_by_did(ctx.author.guild.id, ctx.author.id)

        db = ShameConnection()
        counter = db.get_counter_by_discord_id(ctx.author.guild.id, ctx.author.id)

        if counter.Count <= 0:
            await ctx.send("Your shame is 0. I'm disappointed.")
            return

        if account is None:
            await ctx.send("You don't have any points")
            return

        cost = 100 + (int(account.ShameReducedCount) * 100)

        if account.Balance < cost:
            await ctx.send("You don't have enough points to reduce your shame, costs " + str(cost))
            return

        account.Balance -= cost
        account.ShameReducedCount += 1
        counter.Count -= 1

        account_access.update_account(account)
        db.update_counter(counter)
        db.close()

        await ctx.send("Congratulations! You reduced your shame by 1! "
                       "Now stop doing things to get shamed for.")

    @spend.command(help="Spend points to increase your shame count by 1.")
    async def shameless(self, ctx):
        account = account_access.get_account_by_did(ctx.author.guild.id, ctx.author.id)

        db = ShameConnection()
        counter = db.get_counter_by_discord_id(ctx.author.guild.id, ctx.author.id)

        if account is None:
            await ctx.send("You don't have any points")
            return

        cost = 100 + (int(account.ShameReducedCount) * 10)

        if account.Balance < cost:
            await ctx.send("You don't have enough points to... buy shame... costs " + str(cost))
            return

        account.Balance -= cost
        account.ShameReducedCount += 1
        counter.Count += 1

        account_access.update_account(account)
        db.update_counter(counter)
        db.close()

        await ctx.send("Congratulations! You increased your shame count by 1! "
                       "What is *wrong* with you?")
