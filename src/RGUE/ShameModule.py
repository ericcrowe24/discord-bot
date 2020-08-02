from discord import Embed
from discord import utils as dutils
from discord import Color
import datetime


async def process_command(context, message, db):
    embed = Embed()

    split = message.content.split()

    if split[1] == "log":
        embed = get_shame_logs(db)
    else:
        if message.content.startswith("!shame"):
            embed = shame(message, db)

    if embed is not None:
        await message.channel.send(embed=embed)


def get_shame_logs(db):
    logs = db.get_shame_logs()

    embed = Embed(title="Shame Log", color=Color.green())

    for log in logs:
        embed.add_field(name=log[0], value=str(log[2] + "\n" + str(log[3])), inline=False)

    return embed


def shame(message, con):
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
        return shame_user(con, did, message, target, reason)

    elif prefix == '&':
        return shame_role(con, did, message, reason)


def shame_user(con, did, message, target, reason):
    counter = get_counter(con, did, message)

    embed = create_shame_embed(counter, target, reason)

    update_counter(con, counter)

    con.add_shame_log(counter.UserName, ("No reason given." if len(reason) == 0 else reason), datetime.datetime.now())

    return embed


def shame_role(con, did, message, reason):
    members = find_members_by_role(message, find_role(message, did))

    counters = []

    for member in members:
        counters.append(get_counter(con, member.id, message))

    desc = "Reason: " + ("No reason given." if len(reason) == 0 else reason) + "\n\n"

    for counter in counters:
        desc += ("<@!" + str(counter.DiscordID)
                 + ">\nCount: " + str(counter.Count)
                 + "\nLast Shame: " + str(counter.Date) + "\n\n")
        update_counter(con, counter)
        con.add_shame_log(counter.UserName, ("No reason given." if len(reason) == 0 else reason),
                          datetime.datetime.now())

    return Embed(title="Users shamed", description=desc, color=Color.green())


def get_counter(con, did, message):
    member = con.get_counter_by_discord_id(did)

    if len(member) == 0:
        mem = dutils.find(lambda m: m.id == int(did), message.channel.guild.members)
        return add_counter(mem, con)
    elif len(member) == 1:
        counter = Counter(member[0][1], member[0][2], member[0][3], member[0][4], member[0][0])

        counter.Count += 1

        return counter


def create_shame_embed(counter, target, reason):
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


def update_counter(con, counter):
    counter.Date = datetime.datetime.now()

    con.update_counter(counter)


def add_counter(member, connection):
    counter = Counter(member.id, member.name, datetime.datetime.now(), 1)
    connection.add_counter(counter)
    return counter


def create_error_embed(message):
    return Embed(title="Error", description=message, color=Color.red())


def find_role(message, target):
    for r in message.channel.guild.roles:
        if r.id == int(target):
            return r


def find_members_by_role(message, role):
    members = list()

    for member in message.channel.guild.members:
        if role in member.roles:
            members.append(member)

    return members


class Counter:
    def __init__(self, did, user, date, count, id=0):
        self.id = id
        self.UserName = user
        self.DiscordID = did
        self.Date = date
        self.Count = count
