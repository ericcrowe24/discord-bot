from ark_bot.bot.data_access.base_connection import BaseConnection
from economy_module.economy.account import Account


class AccountConnection(BaseConnection):
    _Accounts = "Accounts"
    _Balance = "Balance"
    _ShameReducedCount = "ShameReducedCount"

    def create_tables(self):
        cursor = self._db.cursor()

        sql = "CREATE TABLE " + self._Accounts + " (" \
              + self._ID + " INT NOT NULL AUTO_INCREMENT," \
              + self._GuildID + " BIGINT(20) NOT NULL," \
              + self._DiscordID + " BIGINT(20) NOT NULL," \
              + self._Balance + " INT NOT NULL DEFAULT 1," \
              + self._ShameReducedCount + " INT DEFAULT 0," \
              + "PRIMARY KEY (" + self._ID + "));" \

        cursor.execute(sql)

        self._db.commit()

        cursor.close()

    def add_account(self, member):
        cursor = self._db.cursor()

        sql = "INSERT INTO " + self._Accounts + "(" \
              + self._GuildID + ", " \
              + self._DiscordID \
              + ") VALUES (%s, %s);"

        values = (member.guild.id, member.id)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_all_accounts(self, gid):
        cursor = self._db.cursor()

        sql = "SELECT * FROM " + self._Accounts + " WHERE " + self._GuildID + " = " + str(gid) + ";"

        cursor.execute(sql)
        fetched = cursor.fetchall()
        cursor.close()

        accounts = []

        if len(fetched) == 0 or fetched is None:
            return None

        for a in fetched:
            accounts.append(self._create_account_object(a))

        return accounts

    def get_account_by_did(self, gid, did):
        cursor = self._db.cursor()

        sql = "SELECT * FROM " + self._Accounts \
              + " WHERE " + self._GuildID + " = " + str(gid) \
              + " AND " + self._DiscordID + " = " + str(did) + ";"

        cursor.execute(sql)
        fetched = cursor.fetchone()
        cursor.close()

        if fetched is None:
            return None

        return self._create_account_object(fetched)

    def update_account(self, account):
        cursor = self._db.cursor()

        sql = "UPDATE " + self._Accounts + " SET " + self._Balance + " = " + str(account.Balance) \
              + " WHERE " + self._GuildID + " = " + str(account.GuildID)\
              + " AND " + self._DiscordID + " = " + str(account.DiscordID) + ";"

        cursor.execute(sql)

        sql = "UPDATE " + self._Accounts + " SET " + self._ShameReducedCount + " = " \
              + str(account.ShameReducedCount) \
              + " WHERE " + self._GuildID + " = " + str(account.GuildID)\
              + " AND " + self._DiscordID + " = " + str(account.DiscordID) + ";"

        cursor.execute(sql)

        self._db.commit()

        cursor.close()

    # noinspection PyMethodMayBeStatic
    def _create_account_object(self, acc) -> Account:
        account = Account(acc[1], acc[2], acc[3], acc[4], acc[0])
        return account
