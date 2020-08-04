from discord import utils as dutils
from RGUE.Cogs.Shame.Counter import Counter
from RGUE.DataAcces.ShameConnection import ShameConnection
import datetime


def get_counter(did):
    db = ShameConnection()
    counter = db.get_counter_by_discord_id(did)
    db.close()

    return counter

def get_all_counters():
    db = ShameConnection()
    counters = db.get_all_counters()
    db.close()

    return counters


def update_counter(counter):
    counter.Date = datetime.datetime.now()

    db = ShameConnection()
    db.update_counter(counter)
    db.close()


def add_counter(member):
    counter = Counter(member.id, member.name, datetime.datetime.now(), 1)

    db = ShameConnection()
    db.add_counter(counter)
    db.close()

    return counter
