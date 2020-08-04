from discord import Embed
from discord import Color
from discord.ext import commands
from RGUE.DataAcces.ShameConnection import ShameConnection
from RGUE import Utilities
from RGUE.Cogs.Shame import ShameCounterAccess
from RGUE.Cogs.Shame import ShameLogAccess
import datetime


# noinspection PyMethodMayBeStatic
class ShameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="shame")
    async def shame(self, ctx):
        db = ShameConnection()
        embed = self._do_shame(ctx.message)
        db.close()

        if embed is not None:
            await ctx.message.channel.send(embed=embed)

    @shame.command(name="log")
    async def get_shame_logs(self, ctx):
        logs = ShameLogAccess.get_all_shame_logs()

        embed = Embed(title="Shame Log", color=Color.light_grey())

        for log in logs:
            embed.add_field(name=log[1], value=str(log[2] + "\n" + str(log[3])), inline=False)

        await ctx.message.channel.send(embed=embed)

    @shame.command(name="scoreboard")
    async def scoreboard(self, ctx):
        counters = ShameCounterAccess.get_all_counters()

        desc = ""

        for counter in counters:
            desc += str(counter.UserName) + ": " + str(counter.Count) + "\n"

        await ctx.message.channel.send(embed=Embed(title="Shame Scoreboard", description=desc, colour=Color.blue()))

    def init_tables(self):
        db = ShameConnection()
        db.create_tables()
        db.close()

    def _do_shame(self, message):
        split = message.content.split()
        did, prefix, target = Utilities.get_target_data(split[1])

        del split[0:2]

        reason = " ".join(split)

        # if the person invoking the command is on mobile, the exclamation mark is left out in the id for users
        if '0' <= prefix <= '9':
            prefix = '!'
            did = target[2:-1]

        if prefix == '!':
            return self._shame_user(did, message, target, reason)
        elif prefix == '&':
            return self._shame_role(did, message, reason)

    def _shame_user(self, did, message, target, reason):
        counter = ShameCounterAccess.get_counter(did)

        if counter is None:
            member = Utilities.find_member_by_id(message, did)
            ShameCounterAccess.add_counter(member)
            counter = ShameCounterAccess.get_counter(member.id)

        counter.Count += 1

        embed = self._create_shame_embed(counter, target, reason)

        ShameCounterAccess.update_counter(counter)

        ShameLogAccess.add_shame_log(counter.UserName,
                                     ("No reason given." if len(reason) == 0 else reason), datetime.datetime.now())

        return embed

    def _shame_role(self, did, message, reason):
        members = Utilities.find_members_by_role(message, Utilities.find_role(message, did))

        counters = []

        for member in members:
            counter = ShameCounterAccess.get_counter(member.id)
            counters.append(counter)

        desc = "Reason: " + ("No reason given." if len(reason) == 0 else reason) + "\n\n"

        for counter in counters:
            desc += ("<@!" + str(counter.DiscordID)
                     + ">\nCount: " + str(counter.Count)
                     + "\nLast Shame: " + str(counter.Date) + "\n\n")
            ShameCounterAccess.update_counter(counter)
            ShameLogAccess.add_shame_log(counter.UserName, ("No reason given." if len(reason) == 0 else reason),
                                         datetime.datetime.now())

        return Embed(title="Users shamed", description=desc, color=Color.green())

    def _create_shame_embed(self, counter, target, reason):
        diff = datetime.datetime.now() - counter.Date

        weeks, days = divmod(diff.days, 7)
        minutes, sec = divmod(diff.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return Embed(title=counter.UserName + "'s Shame",
                     description="It has been "
                                 + str(weeks) + " week(s), "
                                 + str(days) + " day(s), "
                                 + str(hours) + " hour(s), "
                                 + str(minutes) + " minute(s), and "
                                 + str(sec) + " seconds since "
                                 + str(target) + " was last shamed.\nTimes Shamed: "
                                 + str(counter.Count)
                                 + "\nReason: " + ("No reason given." if len(reason) == 0 else reason),
                     color=Color.red())
