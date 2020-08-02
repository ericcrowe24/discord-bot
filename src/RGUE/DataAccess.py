import mysql.connector as mysql


class Connection:
    _db = None
    _instance = None

    def __init__(self):
        raise RuntimeError("must use initialize()")

    @classmethod
    def initialize(cls, host, user, password, db):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._db = mysql.connect(host=host, user=user, password=password, database=db)
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("connection hasn't been initialized")

        return cls._instance

    def create_databases(self):
        cursor = self._db.cursor()

        sql = "CREATE TABLE `Counters` (" \
              "`ID` int(11) NOT NULL AUTO_INCREMENT," \
              "`DiscordID` bigint(20) NOT NULL," \
              "`DiscordUserName` TEXT NULL," \
              "`Date` datetime NOT NULL," \
              "`TimesCalled` int(11) NOT NULL," \
              "PRIMARY KEY (`ID`)" \
              ");"

        cursor.execute(sql)

        sql = "CREATE TABLE `ShameLog` (" \
              "`ID` INT(11) NOT NULL AUTO_INCREMENT," \
              "`User` VARCHAR(50) NOT NULL," \
              "`Message` VARCHAR(100) NOT NULL," \
              "`Date` DATE NOT NULL," \
              "PRIMARY KEY (`ID`)" \
              ");"

        cursor.execute(sql)
        cursor.close()

    def get_counter_by_discord_id(self, did):
        cursor = self._db.cursor()

        sql = "SELECT * FROM Counters WHERE DiscordID = " + str(did)
        cursor.execute(sql)

        return cursor.fetchall()

    def add_counter(self, counter):
        cursor = self._db.cursor()

        sql = "INSERT INTO Counters (DiscordID, DiscordUserName, Date, TimesCalled) VALUES (%s, %s, %s, %s)"
        values = (counter.DiscordID, counter.UserName, counter.Date, counter.Count)
        cursor.execute(sql, values)

        self._db.commit()

    def update_counter(self, counter):
        cursor = self._db.cursor()

        sql = "UPDATE Counters SET TimesCalled = '" + str(counter.Count) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"
        cursor.execute(sql)

        sql = "UPDATE Counters SET Date = '" + str(counter.Date) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"
        cursor.execute(sql)

        self._db.commit()

    def add_shame_log(self, user, message, date):
        cursor = self._db.cursor()

        sql = "INSERT INTO ShameLog (User, Message, Date) VALUES (%s, %s, %s)"
        values = (user, message, date)
        cursor.execute(sql, values)

        self._db.commit()

    def get_shame_logs(self):
        cursor = self._db.cursor()

        sql = "SELECT * FROM ShameLog"
        cursor.execute(sql)

        return cursor.fetchall()
