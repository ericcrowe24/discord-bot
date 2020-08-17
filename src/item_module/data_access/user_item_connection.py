from typing import List

from rgue_bot.bot.data_access.base_connection import BaseConnection
from item_module.user_item.user_item import UserItem


class UserItemConnection(BaseConnection):
    _UserItems = "UserItems"
    _InventoryID = "InventoryID"
    _ItemID = "ItemID"
    _Amount = "Amount"

    def create_tables(self):
        if self.check_table_exists(self._UserItems):
            return

        cursor = self._db.cursor()

        sql = "CREATE TABLE {} (" \
              "{} INT NOT NULL AUTO INCREMENT, " \
              "{} INT NOT NULL, " \
              "{} INT NOT NULL, " \
              "{} INT NOT NULL, " \
              "PRIMARY KEY({}));"
        formatted = sql.format(self._UserItems,
                               self._ID,
                               self._ItemID,
                               self._InventoryID,
                               self._Amount,
                               self._ID)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def add_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "INSERT INTO {} ({}, {}, {}) VALUES ({}, {}, {});"
        formatted = sql.format(self._UserItems,
                               self._ItemID, self._ItemID, self._Amount,
                               item.InventoryID, item.ItemID, item.Amount)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def get_user_items(self, iid: int) -> List[UserItem]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM {} WHERE {} = {};"
        formatted = sql.format(self._UserItems, self._InventoryID, str(iid))

        cursor.execute(formatted)

        fetched = cursor.fetchall()

        cursor.close()

        items = []

        for item in fetched:
            items.append(self._create_user_item(item))

        return items

    def get_user_item(self, inv: int, item: int):
        cursor = self._db.cursor()

        sql = "SELECT * FROM {} WHERE {} = {} AND {} = {};"
        formatted = sql.format(self._UserItems, str(inv), str(item))

        cursor.execute(formatted)

        fetched = cursor.fetchone()

        cursor.close()

        return self._create_user_item(fetched)

    def update_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "UPDATE {} SET {} = {} " \
              "WHERE {} = {} " \
              "AND {} = {};"
        formatted = sql.format(self._UserItems, self._Amount, item.Amount,
                               self._InventoryID, item.InventoryID,
                               self._ItemID, item.ItemID)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def remove_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "DELETE FROM {} " \
              "WHERE {} = {} " \
              "AND {} = {};"
        formatted = sql.format(self._UserItems,
                               self._InventoryID, item.InventoryID,
                               self._ItemID, item.ItemID)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def _create_user_item(self, item):
        raise NotImplementedError
