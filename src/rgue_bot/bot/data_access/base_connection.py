import mysql.connector as mysql

host, user, password, database = "", "", "", ""


class BaseConnection:
    _ID = "ID"
    _GuildID = "GuildID"
    _DiscordID = "DiscordID"
    _Date = "Date"
    _Message = "Message"

    def __init__(self):
        self._db = mysql.connect(host=host, user=user, password=password, database=database)

    def close(self):
        self._db.close()

    def create_tables(self):
        raise NotImplementedError()
