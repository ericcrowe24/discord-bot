from RGUE.bot.bot_client import BotClient
from RGUE.bot.data_access import base_connection


def main(key, init=False, *, host, user, password, database):
    base_connection.host = host
    base_connection.user = user
    base_connection.password = password
    base_connection.database = database
    bot = BotClient(init)
    bot.run(str(key))
