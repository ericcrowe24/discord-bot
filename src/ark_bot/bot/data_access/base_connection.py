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

    def check_table_exists(self, name: str) -> bool:
        cursor = self._db.cursor()

        sql = "SELECT table_name " \
              + "FROM information_schema.tables " \
              + "WHERE table_schema = '{}' " \
              + "AND table_name = '{}' " \
              + "LIMIT 1;"
        formatted = sql.format(database, name)

        cursor.execute(formatted)

        if cursor.fetchone() is not None:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
