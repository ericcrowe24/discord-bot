from typing import List
from rgue_bot.bot.data_access import base_connection
from item_module.inventory.inventory import Inventory


class InventoryConnection(base_connection.BaseConnection):
    _Inventories = "Inventories"
    _ItemID = "ItemID"
    _Quantity = "Quantity"

    def create_tables(self):
        cursor = self._db.cursor()

        sql = "SELECT * " \
              + "FROM information_schema.tables " \
              + "WHERE table_schema = %s " \
              + "AND table_name = %s " \
              + "LIMIT 1;"
        values = (base_connection.database,
                  self._Inventories)

        cursor.execute(sql, values)

        if cursor.fetchone() is not None:
            sql = "CREATE TABLES %s (" \
                  + "%s INT NOT NULL AUTO_INCREMENT, " \
                  + "%s BIGINT(20) NOT NULL, " \
                  + "%s BIGINT(20) NOT NULL, " \
                  + "PRIMARY KEY (%s));"
            values = (self._Inventories,
                      self._ID,
                      self._GuildID,
                      self._DiscordID,
                      self._ID)

            cursor.execute(sql, values)

            self._db.commit()
        else:
            cursor.close()

    def add_inventory(self, gid: int, did: int):
        cursor = self._db.cursor()

        sql = "INSERT INTO %s (%s, %s) VALUES (%s, %s);"
        values = (self._Inventories, self._GuildID, self._DiscordID, str(gid), str(did))

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_inventory_by_discord_id(self, gid: int, did: int) -> Inventory:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s AND %s = %s;"
        values = (self._Inventories, self._GuildID, self._DiscordID, str(gid), str(did))

        cursor.execute(sql, values)

        inv = cursor.fetchone()

        cursor.close()

        return self._create_inventory(inv)

    def get_guild_inventories(self, gid: int) -> List[Inventory]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s;"
        values = (self._Inventories, self._GuildID, str(gid))

        cursor.execute(sql, values)

        fetched = cursor.fetchall()

        cursor.close()

        inventories = []

        for inv in fetched:
            inventories.append(self._create_inventory(inv))

        return inventories

    def delete_inventory(self, gid, did):
        cursor = self._db.cursor()

        sql = "DELETE FROM %s WHERE %s = %s AND %s = %s;"
        values = (self._Inventories, self._GuildID, str(gid), self._DiscordID, str(did))

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def _create_inventory(self, inv):
        raise NotImplementedError
