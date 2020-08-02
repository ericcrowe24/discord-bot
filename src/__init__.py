from RGUE import Bot
import sys


if __name__ == '__main__':
    if sys.argv[1] == "start":
        Bot.main(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], True)
    else:
        Bot.main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
