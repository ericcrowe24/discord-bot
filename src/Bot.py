from RGUE.BotClient import BotClient
from RGUE import DataAccess
import sys


def main(key):
    bot = BotClient()
    bot.run(str(key))


if __name__ == '__main__':
    if sys.argv[2] == "-init" or sys.argv[2] == "-i":
        DataAccess.host = sys.argv[3]
        DataAccess.user = sys.argv[4]
        DataAccess.password = sys.argv[5]
        DataAccess.database = sys.argv[6]

        db = DataAccess.Connection()
        db.create_databases()
        db.close()
    else:
        DataAccess.host = sys.argv[2]
        DataAccess.user = sys.argv[3]
        DataAccess.password = sys.argv[4]
        DataAccess.database = sys.argv[5]

    main(sys.argv[1])
