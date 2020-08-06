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
        if ctx.invoked_subcommand is None:
            embed = self._do_shame(ctx)

            if embed is not None:
                await ctx.send(embed=embed)

    @shame.command(name="log")
    async def get_shame_logs(self, ctx):
        logs = ShameLogAccess.get_all_shame_logs(ctx.guild.id)

        embed = Embed(title="Shame Log", color=Color.light_grey())

        for log in logs:
            embed.add_field(name=log[3], value=str(log[4] + "\n" + str(log[5])), inline=False)

        await ctx.send(embed=embed)

    @shame.command(aliases=["score"])
    async def scoreboard(self, ctx):
        counters = ShameCounterAccess.get_all_counters(ctx.guild.id)

        desc = ""

        for counter in counters:
            desc += str(counter.DiscordUsername) + ": " + str(counter.Count) + "\n"

        await ctx.send(embed=Embed(title="Shame Scoreboard", description=desc, colour=Color.blue()))

    def init_tables(self):
        db = ShameConnection()
        db.create_tables()
        db.close()

    def _do_shame(self, ctx):
        split = ctx.message.content.split()
        target = split[1]
        prefix = target[2]

        reason = " ".join(split[2:-1])

        if prefix == '!' or '0' <= prefix <= '9':
            return self._shame_user(ctx, target, target[3 if prefix == '!' else 2:-1], reason)
        elif prefix == '&':
            return self._shame_role(ctx, target[3:-1], reason)

    def _shame_user(self, ctx, target, did, reason):
        counter = ShameCounterAccess.get_counter(ctx.guild.id, did)
        member = Utilities.find_member_by_id(ctx.guild.members, did)

        if counter is None:
            ShameCounterAccess.add_counter(member)
            counter = ShameCounterAccess.get_counter(ctx.guild.id, member.id)

        counter.Count += 1

        embed = self._create_shame_embed(counter, target, reason)

        ShameCounterAccess.update_counter(counter)

        ShameLogAccess.add_shame_log(member,
                                     ("N/A" if len(reason) == 0 else reason), datetime.datetime.now())

        return embed

    def _shame_role(self, ctx, did, reason):
        members = Utilities.find_members_by_role(ctx.guild.members, Utilities.find_role(ctx.guild.roles, did))

        desc = "Reason: " + ("No reason given." if len(reason) == 0 else reason) + "\n\n"

        for member in members:
            counter = ShameCounterAccess.get_counter(ctx.guild.id, member.id)

            if counter is None:
                ShameCounterAccess.add_counter(member)
                counter = ShameCounterAccess.get_counter(ctx.guild.id, member.id)

            counter.Count += 1

            desc += ("<@!" + str(counter.DiscordID)
                     + ">\nCount: " + str(counter.Count)
                     + "\nLast Shame: " + str(counter.Date) + "\n\n")
            ShameCounterAccess.update_counter(counter)
            ShameLogAccess.add_shame_log(member, ("N/A" if len(reason) == 0 else reason),
                                         datetime.datetime.now())

        return Embed(title="Users shamed", description=desc, color=Color.green())

    def _create_shame_embed(self, counter, target, reason):
        print(counter)
        diff = datetime.datetime.now() - counter.Date

        weeks, days = divmod(diff.days, 7)
        minutes, sec = divmod(diff.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return Embed(title=counter.DiscordUsername + "'s Shame",
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
