from discord.ext import commands
from discord.ext.commands import Context
from . import account_access
from ark_bot.bot import utilities
from economy_module.data_access.AccountConnection import AccountConnection


# noinspection PyMethodMayBeStatic
class AccountCog(commands.Cog):
    def init_tables(self):
        db = AccountConnection()
        db.create_tables()
        db.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        account = account_access.get_account_by_did(message.author.guild.id, message.author.id)

        if account is None:
            account_access.add_account(message.author)
        else:
            account.Balance += 1
            account_access.update_account(account)

    @commands.command(aliases=["bal"], help="Get a dm with your balance for this server.")
    async def balance(self, ctx: Context):
        member = ctx.author
        account = account_access.get_account_by_did(member.guild.id, member.id)

        if account is None:
            account_access.add_account(member)
            account = account_access.get_account_by_did(member.guild.id, member.id)

        if member.dm_channel is None:
            dm = await member.create_dm()
            await dm.send("Your balance on " + ctx.guild.name + " is: " + str(account.Balance))
        else:
            await member.dm_channel.send("Your balance is: " + str(account.Balance))

    @commands.command(help="Give points to another user.")
    async def give(self, ctx: Context):
        split = ctx.message.content.split()

        amount = split[2]

        try:
            if int(amount) < 0:
                await ctx.send("You can't take point from someone like that. Nice try, however.")
                return
        except ValueError:
            await ctx.send("The amount has to be in number format. -_-")
            return

        target = split[1]
        prefix = target[2]

        if str(target[3 if prefix == '!' else 2:-1]) == str(ctx.author.id):
            await ctx.send("Why do you want to give points to yourself?")
            return

        error = self.withdraw(ctx.author, amount)

        if error == 1 or error == 2:
            await ctx.send("You don't have enough points. Better get to typing.")

        if prefix == '!' or '0' <= prefix <= '9':
            member = utilities.find_member_by_id(ctx.guild.members, target[3 if prefix == '!' else 2:-1])
            self.deposit(member, amount)
            await ctx.send("You gave " + target + " " + str(amount) + " points!")
        else:
            await ctx.send("You can only give points to users.")

    @commands.group(help="Grant points to a user or all users under a role. Admin only")
    async def grant(self, ctx: Context):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("Only administrators can invoke that command.")
            return

        split = ctx.message.content.split()

        amount = split[2]

        try:
            if int(amount) < 0:
                await ctx.send("Grant amount has to be a positive number.")
                return
        except ValueError:
            await ctx.send("Grant amount has to be in number format. -_-")
            return

        target = split[1]
        prefix = target[2]

        if prefix == '!' or '0' <= prefix <= '9':
            if self._grant_user(ctx, target[3 if prefix == '!' else 2:-1], amount) == 0:
                await ctx.send("Granted " + target + " " + amount + " points!")
            else:
                await ctx.send("Something went wrong, no points were granted.")
        elif prefix == '&':
            if self._grant_role(ctx, target[3:-1], amount) == 0:
                await ctx.send("Granted all " + target + " members " + amount + " points!")
            else:
                await ctx.send("Something went wrong, one or more users didn't receive any points")

    def _grant_user(self, ctx: Context, did, amount):
        member = utilities.find_member_by_id(ctx.guild.members, did)

        return self.deposit(member, int(amount))

    def _grant_role(self, ctx, did, amount):
        members = utilities.find_members_by_role(ctx.guild.members, utilities.find_role(ctx.guild.roles, did))

        error = 0

        for member in members:
            error += self._grant_user(ctx, member.id, amount)

        return error

    @grant.command(name="all", help="Grant all users points. Admin only")
    async def grant_all(self, ctx):
        amount = ctx.message.content.split()[2]

        for member in ctx.message.channel.guild.members:
            self._grant_user(ctx, member.id, amount)

        await ctx.message.channel.send("Granted all users " + amount + " points!")

    def withdraw(self, target, amount):
        account = account_access.get_account_by_did(target.guild.id, target.id)

        if account is None:
            return 2
        if account.Balance < 0:
            return 1

        account.Balance -= int(amount)

        account_access.update_account(account)

        return 0

    def deposit(self, target, amount):
        account = account_access.get_account_by_did(target.guild.id, target.id)

        if account is None:
            account_access.add_account(target)
            account = account_access.get_account_by_did(target.guild.id, target.id)
            amount -= 1

        account.Balance += int(amount)

        account_access.update_account(account)

        return 0
