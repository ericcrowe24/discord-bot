import mysql.connector as mysql

host, user, password, database = "", "", "", ""


class Connection:
    def __init__(self):
        self._db = mysql.connect(host=host, user=user, password=password, database=database)

    def close(self):
        self._db.close()

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

        self._db.commit()

        cursor.close()

    def get_counter_by_discord_id(self, did):
        cursor = self._db.cursor()

        sql = "SELECT * FROM Counters WHERE DiscordID = " + str(did)
        cursor.execute(sql)

        counters = cursor.fetchall()

        cursor.close()

        return counters

    def add_counter(self, counter):
        cursor = self._db.cursor()

        sql = "INSERT INTO Counters (DiscordID, DiscordUserName, Date, TimesCalled) VALUES (%s, %s, %s, %s)"

        values = (counter.DiscordID, counter.UserName, counter.Date, counter.Count)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def update_counter(self, counter):
        cursor = self._db.cursor()

        sql = "UPDATE Counters SET TimesCalled = '" + str(counter.Count) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"

        cursor.execute(sql)

        sql = "UPDATE Counters SET Date = '" + str(counter.Date) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"

        cursor.execute(sql)

        self._db.commit()

        cursor.close()

    def add_shame_log(self, username, message, date):
        cursor = self._db.cursor()

        sql = "INSERT INTO ShameLog (User, Message, Date) VALUES (%s, %s, %s)"

        values = (username, message, date)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_shame_logs(self):
        cursor = self._db.cursor()

        sql = "SELECT * FROM ShameLog"

        cursor.execute(sql)

        logs = cursor.fetchall()

        cursor.close()

        return logs
