from ark_bot.bot.bot_client import BotClient
from ark_bot.bot.data_access import base_connection


def start(key, init=False, *, host, user, password, database):
    base_connection.host = host
    base_connection.user = user
    base_connection.password = password
    base_connection.database = database
    bot = BotClient(init)
    bot.run(str(key))
