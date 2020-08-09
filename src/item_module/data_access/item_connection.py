from typing import List
from rgue_bot.bot.data_access import base_connection
from item_module.item.item import Item, Rarity


class ItemConnection(base_connection.BaseConnection):
    _Items = "Items"
    _ItemID = "ItemID"
    _Name = "Name"
    _Desc = "Description"
    _Rarity = "Rarity"

    def create_tables(self):
        cursor = self._db.cursor()

        sql = "CREATE TABLE %s (" \
              "%s INT(11) NOT NULL AUTO_INCREMENT," \
              " %s INT(11) NOT NULL," \
              " %s BIGINT(20) NOT NULL," \
              " %s CHAR(255) NOT NULL," \
              " %s CHAR(255) NOT NULL," \
              " %s INT NOT NULL," \
              " PRIMARY KEY(%s));"
        values = (self._Items,
                  self._ID,
                  self._ItemID,
                  self._GuildID,
                  self._Name,
                  self._Desc,
                  self._Rarity,
                  self._ID)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def add_item(self, item: Item):
        cursor = self._db.cursor()

        sql = "INSERT INTO %s (" \
              + "%s, " \
              + "%s, " \
              + "%s, " \
              + "%s, " \
              + "%s, " \
              + "VALUES(%s, %s, %s, %s, %s);"
        values = (self._Items,
                  self._ItemID,
                  self._GuildID,
                  self._Name,
                  self._Desc,
                  self._Rarity,
                  item.ItemID, item.GuildID, item.Name, item.Description, item.Rarity)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_item_by_id(self, gid: int, iid: int) -> Item:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s AND %s = %s;"
        values = (self._Items, self._GuildID, self._ItemID)

        cursor.execute(sql, values)

        item = self._create_item(cursor.fetchone())

        cursor.close()

        return item

    def get_items_by_rarity(self, gid: int, rarity: Rarity) -> List[Item]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s AND %s = %s;"
        values = (self._Items, self._GuildID, str(gid), self._Rarity, str(rarity.value()))

        cursor.execute(sql, values)

        itms = cursor.fetchall()
        cursor.close()

        items = []

        for itm in itms:
            items.append(itm)

        return items

    def get_all_guild_items(self, gid: int) -> List[Item]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s;"
        values = (self._Items, self._GuildID, str(gid))

        cursor.execute(sql, values)

        fetched = cursor.fetchall()
        cursor.close()

        items = []

        for item in fetched:
            items.append(item)

        return items

    def delete_item(self, gid: int, iid: int):
        cursor = self._db.cursor()

        sql = "DELETE FROM %s WHERE %s = %s AND %s = %s;"
        values = (self._Items, self._GuildID, str(gid), self._ItemID, str(iid))

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    # noinspection PyMethodMayBeStatic
    def _create_item(self, item: str) -> Item:
        return Item(int(item[1]), int(item[2]), item[3], item[4], Rarity(int(item[5])))
