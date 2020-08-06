from ark_bot.bot.Cogs.Shame.Counter import Counter
from ark_bot.bot.data_access.shame_connection import ShameConnection
import datetime


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
    counter = Counter(member.guild.id, member.id, member.name, datetime.datetime.now(), 1)

    db = ShameConnection()
    db.add_counter(counter)
    db.close()

    return counter
