from rgue_bot.bot.bot_client import BotClient
from rgue_bot.bot.data_access import base_connection
import sys


def start(key, init=False, *, host, user, password, database):
    base_connection.host = host
    base_connection.user = user
    base_connection.password = password
    base_connection.database = database
    bot = BotClient(init)
    bot.run(str(key))


if __name__ == "__main__":
    if sys.argv[1] == "-init" or sys.argv[1] == "-i":
        start(sys.argv[2], True, host=sys.argv[3], user=sys.argv[4], password=sys.argv[5], database=sys.argv[6])
    else:
        start(sys.argv[1], host=sys.argv[2], user=sys.argv[3], password=sys.argv[4], database=sys.argv[5])