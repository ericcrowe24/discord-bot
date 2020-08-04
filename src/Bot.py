from RGUE.BotClient import BotClient
from RGUE.DataAcces import BaseConnection
import sys


def main(key, init=False):
    bot = BotClient(init)
    bot.run(str(key))


if __name__ == '__main__':
    if sys.argv[1] == "-init" or sys.argv[1] == "-i":
        BaseConnection.host = sys.argv[3]
        BaseConnection.user = sys.argv[4]
        BaseConnection.password = sys.argv[5]
        BaseConnection.database = sys.argv[6]

        main(sys.argv[2], True)
    else:
        BaseConnection.host = sys.argv[2]
        BaseConnection.user = sys.argv[3]
        BaseConnection.password = sys.argv[4]
        BaseConnection.database = sys.argv[5]

        main(sys.argv[1])
