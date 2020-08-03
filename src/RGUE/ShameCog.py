from discord import Embed
from discord import utils as dutils
from discord import Color
from discord.ext import commands
from RGUE.DataAccess import Connection
from RGUE.Counter import Counter
import datetime


# noinspection PyMethodMayBeStatic
class ShameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="shame")
    async def shame(self, ctx):
        db = Connection()
        embed = self.do_shame(ctx.message, db)
        db.close()

        if embed is not None:
            await ctx.message.channel.send(embed=embed)

    @shame.command(name="log")
    async def get_shame_logs(self, ctx):
        db = Connection()
        logs = db.get_shame_logs()
        db.close()

        embed = Embed(title="Shame Log", color=Color.green())

        for log in logs:
            embed.add_field(name=log[1], value=str(log[2] + "\n" + str(log[3])), inline=False)

        await ctx.message.channel.send(embed=embed)

    @shame.command(name="scoreboard")
    async def scoreboard(self, ctx):
        db = Connection()
        counters = db.get_all_counters()
        db.close()

        desc = ""

        for counter in counters:
            desc += str(counter.UserName) + ": " + str(counter.Count) + "\n"

        await ctx.message.channel.send(embed=Embed(title="Shame Scoreboard", description=desc))

    def do_shame(self, message, con):
        split = message.content.split()
        target = split[1]
        prefix = target[2]
        did = target[3:-1]

        del split[0:2]

        reason = " ".join(split)

        # if the person invoking the command is on mobile, the exclamation mark is left out in the id for users
        if '0' <= prefix <= '9':
            prefix = '!'
            did = target[2:-1]

        if prefix == '!':
            return self.shame_user(con, did, message, target, reason)

        elif prefix == '&':
            return self.shame_role(con, did, message, reason)

    def shame_user(self, con, did, message, target, reason):
        counter = self.get_counter(con, did, message)

        embed = self.create_shame_embed(counter, target, reason)

        self.update_counter(con, counter)

        con.add_shame_log(counter.UserName,
                          ("No reason given." if len(reason) == 0 else reason), datetime.datetime.now())

        return embed

    def shame_role(self, con, did, message, reason):
        members = self.find_members_by_role(message, self.find_role(message, did))

        counters = []

        for member in members:
            counters.append(self.get_counter(con, member.id, message))

        desc = "Reason: " + ("No reason given." if len(reason) == 0 else reason) + "\n\n"

        for counter in counters:
            desc += ("<@!" + str(counter.DiscordID)
                     + ">\nCount: " + str(counter.Count)
                     + "\nLast Shame: " + str(counter.Date) + "\n\n")
            self.update_counter(con, counter)
            con.add_shame_log(counter.UserName, ("No reason given." if len(reason) == 0 else reason),
                              datetime.datetime.now())

        return Embed(title="Users shamed", description=desc, color=Color.green())

    def get_counter(self, con, did, message):
        counter = con.get_counter_by_discord_id(did)

        if counter is None:
            mem = dutils.find(lambda m: m.id == int(did), message.channel.guild.members)
            return self.add_counter(mem, con)
        else:
            counter.Count += 1

            return counter

    def create_shame_embed(self, counter, target, reason):
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
                     color=Color.green())

    def update_counter(self, con, counter):
        counter.Date = datetime.datetime.now()

        con.update_counter(counter)

    def add_counter(self, member, connection):
        counter = Counter(member.id, member.name, datetime.datetime.now(), 1)
        connection.add_counter(counter)
        return counter

    def create_error_embed(self, message):
        return Embed(title="Error", description=message, color=Color.red())

    def find_role(self, message, target):
        for r in message.channel.guild.roles:
            if r.id == int(target):
                return r

    def find_members_by_role(self, message, role):
        members = list()

        for member in message.channel.guild.members:
            if role in member.roles:
                members.append(member)

        return members
