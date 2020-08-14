from typing import List

from item_module.data_access.item_connection import ItemConnection
from item_module.item.item import Item, Rarity


def create_tables():
    db = ItemConnection()
    db.create_tables()
    db.close()


def add_item(item: Item) -> bool:
    db = ItemConnection()
    success = db.add_item(item)
    db.close()

    if success:
        return True
    else:
        return False


def get_item_by_id(gid: int, iid: int) -> Item:
    db = ItemConnection()
    item = db.get_item_by_id(gid, iid)
    db.close()

    return item


def get_items_by_rarity(gid: int, rarity: Rarity) -> List[Item]:
    db = ItemConnection()
    items = db.get_items_by_rarity(gid, rarity)
    db.close()

    return items


def get_all_guild_items(gid: int) -> List[Item]:
    db = ItemConnection()
    items = db.get_all_guild_items(gid)
    db.close()

    return items


def update_item(item: Item):
    db = ItemConnection()
    db.update_item(item)
    db.close()


def delete_item(item: Item):
    db = ItemConnection()
    db.delete_item(item)
    db.close()
