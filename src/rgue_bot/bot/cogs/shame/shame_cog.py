from discord import Embed
from discord import Color
from discord.ext import commands
from rgue_bot.bot import utilities
from rgue_bot.bot.cogs.shame.counter import Counter
from rgue_bot.bot.data_access.shame_connection import ShameConnection
import datetime


class Shame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="shame", help="Shame a user or all users under a role")
    async def shame(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = self._do_shame(ctx)

            if embed is not None:
                await ctx.send(embed=embed)

    @shame.command(name="log", help="Show all of the same logs.")
    async def get_shame_logs(self, ctx):
        logs = get_all_shame_logs(ctx.guild.id)

        embed = Embed(title="shame Log", color=Color.light_grey())

        for log in logs:
            member = utilities.find_member_by_id(ctx.guild.members, log[2])
            embed.add_field(name=member.name, value=str(log[3] + "\n" + str(log[4])), inline=False)

        await ctx.send(embed=embed)

    @shame.command(aliases=["score"], help="Show all users' shame counters.")
    async def scoreboard(self, ctx):
        counters = get_all_counters(ctx.guild.id)

        desc = ""

        for counter in counters:
            desc += str(counter.DiscordUsername) + ": " + str(counter.Count) + "\n"

        await ctx.send(embed=Embed(title="shame Scoreboard", description=desc, colour=Color.blue()))

    def init_tables(self):
        db = ShameConnection()
        db.create_tables()
        db.close()

    def _do_shame(self, ctx):
        split = ctx.message.content.split()
        target = split[1]
        prefix = target[2]

        reason = " ".join(split[2:])

        if prefix == '!' or '0' <= prefix <= '9':
            return self._shame_user(ctx, target, target[3 if prefix == '!' else 2:-1], reason)
        elif prefix == '&':
            return self._shame_role(ctx, target[3:-1], reason)

    def _shame_user(self, ctx, target, did, reason):
        counter = get_counter(ctx.guild.id, did)
        member = utilities.find_member_by_id(ctx.guild.members, did)

        if counter is None:
            add_counter(member)
            counter = get_counter(ctx.guild.id, member.id)

        counter.Count += 1

        embed = self._create_shame_embed(member.name, counter, target, reason)

        update_counter(counter)

        add_shame_log(member,
                      ("N/A" if len(reason) == 0 else reason), datetime.datetime.now())

        return embed

    def _shame_role(self, ctx, did, reason):
        members = utilities.find_members_by_role(ctx.guild.members, utilities.find_role(ctx.guild.roles, did))

        desc = "Reason: " + ("No reason given." if len(reason) == 0 else reason) + "\n\n"

        for member in members:
            counter = get_counter(ctx.guild.id, member.id)

            if counter is None:
                add_counter(member)
                counter = get_counter(ctx.guild.id, member.id)

            counter.Count += 1

            desc += ("<@!" + str(counter.DiscordID)
                     + ">\nCount: " + str(counter.Count)
                     + "\nLast shame: " + str(counter.Date) + "\n\n")
            update_counter(counter)
            add_shame_log(member, ("N/A" if len(reason) == 0 else reason),
                          datetime.datetime.now())

        return Embed(title="Users shamed", description=desc, color=Color.green())

    def _create_shame_embed(self, name, counter, target, reason):
        diff = datetime.datetime.now() - counter.Date

        weeks, days = divmod(diff.days, 7)
        minutes, sec = divmod(diff.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return Embed(title=name + "'s shame",
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


def get_counter(gid, did):
    db = ShameConnection()
    counter = db.get_counter_by_discord_id(gid, did)
    db.close()

    return counter


def get_all_counters(gid):
    db = ShameConnection()
    counters = db.get_all_counters(gid)
    db.close()

    return counters


def update_counter(counter):
    counter.Date = datetime.datetime.now()

    db = ShameConnection()
    db.update_counter(counter)
    db.close()


def add_counter(member):
    counter = Counter(member.guild.id, member.id, datetime.datetime.now(), 1)

    db = ShameConnection()
    db.add_counter(counter)
    db.close()

    return counter


def get_all_shame_logs(gid):
    db = ShameConnection()
    logs = db.get_shame_logs(gid)
    return logs


def add_shame_log(user, reason, date):
    db = ShameConnection()
    db.add_shame_log(user, reason, date)
    db.close()
