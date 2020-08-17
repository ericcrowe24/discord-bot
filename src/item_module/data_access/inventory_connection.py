from typing import List
from rgue_bot.bot.data_access import base_connection
from item_module.inventory.inventory import Inventory


class InventoryConnection(base_connection.BaseConnection):
    _Inventories = "Inventories"
    _InventoryID = "InventoryID"

    def create_tables(self):
        if self.check_table_exists(self._Inventories):
            return

        cursor = self._db.cursor()

        sql = "CREATE TABLE %s (" \
              + "%s INT NOT NULL AUTO_INCREMENT, " \
              + "%s BIGINT(20) NOT NULL, " \
              + "%s BIGINT(20) NOT NULL, " \
              + "PRIMARY KEY (%s));"
        formatted = sql.format(self._Inventories,
                               self._InventoryID,
                               self._GuildID,
                               self._DiscordID,
                               self._InventoryID)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def add_inventory(self, gid: int, did: int):
        cursor = self._db.cursor()

        iid = self.get_guild_inventories(gid)[-1].InventoryID

        sql = "INSERT INTO %s (%s, %s, %s) VALUES (%s, %s, %s);"
        formatted = sql.format(self._Inventories,
                               self._InventoryID, self._GuildID, self._DiscordID,
                               str(iid + 1), str(gid), str(did))

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def get_inventory_by_discord_id(self, gid: int, did: int) -> Inventory:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s AND %s = %s;"
        formatted = sql.format(self._Inventories, self._GuildID, self._DiscordID, str(gid), str(did))

        cursor.execute(formatted)

        inv = cursor.fetchone()

        cursor.close()

        return self._create_inventory(inv)

    def get_guild_inventories(self, gid: int) -> List[Inventory]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s;"
        formatted = sql.format(self._Inventories, self._GuildID, str(gid))

        cursor.execute(formatted)

        fetched = cursor.fetchall()

        cursor.close()

        inventories = []

        for inv in fetched:
            inventories.append(self._create_inventory(inv))

        return inventories

    def delete_inventory(self, gid, did):
        cursor = self._db.cursor()

        sql = "DELETE FROM %s WHERE %s = %s AND %s = %s;"
        formatted = sql.format(self._Inventories, self._GuildID, str(gid), self._DiscordID, str(did))

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def _create_inventory(self, inv):
        return Inventory(inv[0], inv[1], inv[2])
