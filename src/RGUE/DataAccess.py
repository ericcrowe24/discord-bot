import mysql.connector as mysql


class Connection():
    def __init__(self, host, user, password, db):
        self.db = mysql.connect(host=host, user=user, password=password, database=db)

    def get_counter_by_discord_id(self, id):
        cursor = self.db.cursor()

        sql = "SELECT * FROM Counters WHERE DiscordID = " + str(id)
        cursor.execute(sql)

        return cursor.fetchall()

    def add_counter(self, counter):
        cursor = self.db.cursor()

        sql = "INSERT INTO Counters (DiscordID, DiscordUserName, Date, TimesCalled) VALUES (%s, %s, %s, %s)"
        values = (counter.DiscordID, counter.UserName, counter.Date, counter.Count)
        cursor.execute(sql, values)

        self.db.commit()

    def update_counter(self, counter):
        cursor = self.db.cursor()

        sql = "UPDATE Counters SET TimesCalled = '" + str(counter.Count) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"
        cursor.execute(sql)

        sql = "UPDATE Counters SET Date = '" + str(counter.Date) + "' WHERE DiscordID = '" \
              + str(counter.DiscordID) + "'"
        cursor.execute(sql)

        self.db.commit()

    def add_shame_log(self, user, message, date):
        cursor = self.db.cursor()

        sql = "INSERT INTO ShameLog (User, Message, Date) VALUES (%s, %s, %s)"
        values = (user, message, date)
        cursor.execute(sql, values)

        self.db.commit()

    def get_shame_logs(self):
        cursor = self.db.cursor()

        sql = "SELECT * FROM ShameLog"
        cursor.execute(sql)

        return cursor.fetchall()
