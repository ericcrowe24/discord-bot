from RGUE.DataAcces import BaseConnection
from RGUE.Cogs.Shame import Counter


class ShameConnection(BaseConnection.BaseConnection):
    _Counters = "Counters"
    _ShameLog = "ShameLog"
    _TimesCalled = "TimesCalled"

    def create_tables(self):
        cursor = self._db.cursor()

        sql = "CREATE TABLE " + self._Counters + " (" \
              + self._ID + " int(11) NOT NULL AUTO_INCREMENT," \
              + self._GuildID + " BIGINT(20) NOT NULL," \
              + self._DiscordID + " bigint(20) NOT NULL," \
              + self._DiscordUserName + " TEXT NULL," \
              + self._Date + " datetime NOT NULL," \
              + self._TimesCalled + " int(11) NOT NULL," \
                                    " PRIMARY KEY (" + self._ID + "));"

        cursor.execute(sql)

        sql = "CREATE TABLE " + self._ShameLog + " (" \
              + self._ID + " INT(11) NOT NULL AUTO_INCREMENT," \
              + self._GuildID + " BIGINT(20) NOT NULL," \
              + self._DiscordID + " BIGINT(20) NOT NULL," \
              + self._DiscordUserName + " VARCHAR(50) NOT NULL," \
              + self._Message + " VARCHAR(100) NOT NULL," \
              + self._Date + " DATE NOT NULL," \
                             "PRIMARY KEY (" + self._ID + "));"

        cursor.execute(sql)

        self._db.commit()

        cursor.close()

    def get_counter_by_discord_id(self, gid, did):
        cursor = self._db.cursor()

        sql = "SELECT * FROM " + self._Counters \
              + " WHERE " + self._GuildID + " = " + str(gid) \
              + " AND " + self._DiscordID + " = " + str(did) + ";"

        cursor.execute(sql)

        fetched = cursor.fetchone()

        cursor.close()

        if fetched is None:
            return None
        else:
            return Counter.Counter(fetched[1], fetched[2], fetched[3], fetched[4], fetched[5], fetched[0])

    def get_all_counters(self, gid):
        cursor = self._db.cursor()

        sql = "SELECT * FROM " + self._Counters + " WHERE " + self._GuildID + " = " + str(gid) + ";"

        cursor.execute(sql)

        fetched = cursor.fetchall()

        counters = []

        for counter in fetched:
            counters.append(Counter.Counter(counter[1], counter[2], counter[3], counter[4], counter[5], counter[0]))

        cursor.close()

        return counters

    def add_counter(self, counter):
        cursor = self._db.cursor()

        sql = "INSERT INTO " + self._Counters + " (" \
              + self._GuildID + ", " \
              + self._DiscordID + ", " \
              + self._DiscordUserName + ", " \
              + self._Date + ", " \
              + self._TimesCalled \
              + ") VALUES (%s, %s, %s, %s, %s);"

        values = (str(counter.GuildID), counter.DiscordID, counter.DiscordUsername, counter.Date, counter.Count)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def update_counter(self, counter):
        cursor = self._db.cursor()

        sql = "UPDATE " + self._Counters + " SET " + self._TimesCalled + " = " + str(counter.Count) \
              + " WHERE " + self._GuildID + " = " + str(counter.GuildID) \
              + " AND " + self._DiscordID + " = " + str(counter.DiscordID) + ";"

        cursor.execute(sql)

        sql = "UPDATE " + self._Counters + " SET " + self._Date + " = '" + str(counter.Date) \
              + "' WHERE " + self._GuildID + " = " + str(counter.GuildID) \
              + " AND " + self._DiscordID + " = " + str(counter.DiscordID) + ";"
        print(sql)

        cursor.execute(sql)

        self._db.commit()

        cursor.close()

    def add_shame_log(self, target, message, date):
        cursor = self._db.cursor()

        sql = "INSERT INTO " + self._ShameLog + " (" \
              + self._GuildID + ", " \
              + self._DiscordID + ", " \
              + self._DiscordUserName + ", " \
              + self._Message + ", " \
              + self._Date \
              + ") VALUES (%s, %s, %s, %s, %s);"

        values = (str(target.guild.id), str(target.id), target.name, message, date)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_shame_logs(self, gid):
        cursor = self._db.cursor()

        sql = "SELECT * FROM " + self._ShameLog + " WHERE " + self._GuildID + " = " + str(gid) + ";"

        cursor.execute(sql)

        logs = cursor.fetchall()

        cursor.close()

        return logs
