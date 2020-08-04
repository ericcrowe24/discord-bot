from discord.ext import commands
from discord.message import Message
from RGUE.Cogs.Economy import AccountAccess
from RGUE import Utilities


# noinspection PyMethodMayBeStatic
class EconomyCog(commands.Cog):
    _last_members = {}

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        account = AccountAccess.get_account_by_did(message.author.id)

        if account is None:
            AccountAccess.add_account(message.author)
        else:
            account.Balance += 1
            AccountAccess.update_account(account)

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        member = ctx.author
        account = AccountAccess.get_account_by_did(member.id)

        if account is None:
            AccountAccess.add_account(member)
            account = AccountAccess.get_account_by_did(member.id)

        if member.dm_channel is None:
            dm = await member.create_dm()
            await dm.send("Your balance is: " + str(account.Balance))
        else:
            await member.dm_channel.send("Your balance is: " + str(account.Balance))

    @commands.command()
    async def give(self, ctx):
        raise NotImplementedError

    @commands.group()
    async def grant(self, ctx):
        split = ctx.message.content.split()
        amount = split[3]
        did, prefix, target = Utilities.get_target_data(split[1])

        if prefix == '!':
            self._grant_user(ctx, did, amount)
            await ctx.message.channel.send("Granted" + target + " " + amount + " points!")
        elif prefix == '&':
            self._grant_role(ctx, did, amount)
            await ctx.message.channel.send("Granted all " + target + " members " + amount + " points!")

    def _grant_user(self, ctx, did, amount):
        account = AccountAccess.get_account_by_did(did)

        if account is None:
            member = Utilities.find_member_by_id(ctx.message, did)
            AccountAccess.add_account(member)
            account = AccountAccess.get_account_by_did(did)
            account.Balance += int(amount) - 1
        else:
            account.Balance += int(amount)

        AccountAccess.update_account(account)

    def _grant_role(self, ctx, did, amount):
        members = Utilities.find_members_by_role(ctx.message, Utilities.find_role(ctx.message, did))

        for member in members:
            self._grant_user(ctx, member.id, amount)

    @grant.command(name="all")
    async def grant_all(self, ctx):
        amount = ctx.message.content.split()[2]

        for member in ctx.message.channel.guild.members:
            self._grant_user(ctx, member.id, amount)

        await ctx.message.channel.send("Granted all users " + amount + " points!")
