from typing import List

from ark_bot.bot.data_access.base_connection import BaseConnection
from item_module.user_item.user_item import UserItem


class UserItemConnection(BaseConnection):
    _UserItems = "UserItems"
    _InventoryItemID = "InventoryItemID"
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
              "{} INT NOT NULL, " \
              "PRIMARY KEY({}));"
        formatted = sql.format(self._UserItems,
                               self._ID,
                               self._InventoryItemID,
                               self._ItemID,
                               self._InventoryID,
                               self._Amount,
                               self._ID)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def add_user_item(self, item: UserItem):
        items = self.get_user_items(item.InventoryID)

        current_id = self._find_current_inventory_item_id(items)

        cursor = self._db.cursor()

        sql = "INSERT INTO {} " \
              "({}, {}, {}, {}) " \
              "VALUES ({}, {}, {}, {});"
        formatted = sql.format(self._UserItems,
                               self._InventoryItemID, self._InventoryID, self._ItemID, self._Amount,
                               current_id, item.InventoryID, item.ItemID, item.Amount)

        cursor.execute(formatted)

        self._db.commit()

        cursor.close()

    def get_user_items(self, iid: int) -> List[UserItem]:
        cursor = self._db.cursor()

        sql = "SELECT * FROM {} WHERE {} = {} ORDER BY {} ASC;"
        formatted = sql.format(self._UserItems, self._InventoryID, str(iid), self._InventoryItemID)

        cursor.execute(formatted)

        fetched = cursor.fetchall()

        cursor.close()

        items = []

        for item in fetched:
            items.append(self._create_user_item(item))

        return items

    def get_user_items_page(self, iid: int, page=1) -> List[UserItem]:
        items = self.get_user_items(iid)

        if len(items) < 51:
            return items

        paged = []
        start = 1 + 50 * (page - 1)

        if len(items) < start:
            return None

        end = min(50 * page, len(items))

        for x in range(start, end):
            paged.append(items[x - 1])

        return paged

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

    def _find_current_inventory_item_id(self, items: List[UserItem]) -> int:
        if items is not None:
            if len(items) == 0:
                return 0
            elif len(items) == 1:
                if items[0].InventoryItemID != 1:
                    return 1
                else:
                    return 2
            else:
                for x in range(1, len(items)):
                    if items[x].InventoryItemID - 1 != items[x - 1].InventoryItemID:
                        return items[x].InventoryItemID + 1

    def _create_user_item(self, item):
        return UserItem(item[0], item[1], item[2], item[3], item[4])
