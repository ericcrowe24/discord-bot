from typing import List

from rgue_bot.bot.data_access.base_connection import BaseConnection
from item_module.item.user_item import UserItem


class UserItemConnection(BaseConnection):
    _UserItems = "UserItems"
    _InventoryID = "InventoryID"
    _ItemID = "ItemID"
    _Amount = "Amount"

    def create_tables(self):
        raise NotImplementedError

    def add_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "INSERT INTO %s (%s, %s, %s) VALUES (%s, %s, %s);"
        values = (self._UserItems,
                  self._ItemID, self._ItemID, self._Amount,
                  item.InventoryID, item.ItemID, item.Amount)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def get_user_items(self, iid: int) -> List[UserItem]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM %s WHERE %s = %s;"
        values = (self._UserItems, self._InventoryID, str(iid))

        cursor.execute(sql, values)

        fetched = cursor.fetchall()

        cursor.close()

        items = []

        for item in fetched:
            items.append(self._create_user_item(item))

        return items

    def update_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "UPDATE %s SET %s = %s " \
              "WHERE %s = %s " \
              "AND %s = %s;"
        values = (self._UserItems, self._Amount, item.Amount,
                  self._InventoryID, item.InventoryID,
                  self._ItemID, item.ItemID)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def remove_user_item(self, item: UserItem):
        cursor = self._db.cursor()

        sql = "DELETE FROM %s " \
              "WHERE %s = %s " \
              "AND %s = %s;"
        values = (self._UserItems,
                  self._InventoryID, item.InventoryID,
                  self._ItemID, item.ItemID)

        cursor.execute(sql, values)

        self._db.commit()

        cursor.close()

    def _create_user_item(self, item):
        raise NotImplementedError
