from RGUE.BotClient import BotClient
from RGUE import DataAccess
import sys


def main(key):
    bot = BotClient()
    bot.run(str(key))


if __name__ == '__main__':
    DataAccess.host = sys.argv[2]
    DataAccess.user = sys.argv[3]
    DataAccess.password = sys.argv[4]
    DataAccess.database = sys.argv[5]

    main(sys.argv[1])