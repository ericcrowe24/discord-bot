from discord.ext import commands
from RGUE.Cogs.Economy import AccountAccess
from RGUE.DataAcces.ShameConnection import ShameConnection


class SpendingCog(commands.Cog):
    @commands.group()
    async def spend(self, ctx):
        await ctx.message.channel.send("Please specific how you would like to spend your points")
    
    @spend.command()
    async def shame(self, ctx):
        account = AccountAccess.get_account_by_did(ctx.author.id)

        db = ShameConnection()
        counter = db.get_counter_by_discord_id(ctx.author.id)

        if counter.Count <= 0:
            await ctx.message.channel.send("Your shame is 0. I'm disappointed.")
            return

        if account is None:
            await ctx.message.channel.send("You don't have any points")
            return

        cost = account.ShameReducedCount * 10 + 100

        if account.Balance < cost:
            await ctx.message.channel.send("You don't have enough points to reduce your shame, costs " + str(cost))
            return

        account.Balance -= cost
        account.ShameReducedCount += 1
        counter.Count -= 1

        AccountAccess.update_account(account)
        db.update_counter(counter)
        db.close()

        await ctx.message.channel.send("Congratulations! You reduced your shame by 1! "
                                       "Now stop doing things to get shamed for")