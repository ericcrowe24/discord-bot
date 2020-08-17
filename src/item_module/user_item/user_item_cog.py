from typing import List

from discord.ext import commands

from item_module.user_item.user_item import UserItem
from item_module.data_access.user_item_connection import UserItemConnection


class UserItemCog(commands.Cog):
    def get_user_items(self, inv: int) -> List[UserItem]:
        return get_user_items(inv)

    def update_user_item(self, item: UserItem):
        update_user_item(item)

    def withdraw_item(self, inv: int, item: int):
        return get_user_item(inv, item)

    def deposit_item(self, item: UserItem):
        add_user_item(item)

    def transfer_item(self, inv_from: int, inv_to: int, item: int, amount: int):
        raise NotImplementedError


def add_user_item(item: UserItem):
    db = UserItemConnection()
    db.add_user_item(item)
    db.close()


def get_user_item(inv: int, item: int) -> UserItem:
    db = UserItemConnection()
    item = db.get_user_item(inv, item)
    db.close()

    return item


def get_user_items(iid: int) -> List[UserItem]:
    db = UserItemConnection()
    items = db.get_user_items(iid)
    db.close()

    return items


def update_user_item(item: UserItem):
    db = UserItemConnection()
    db.update_user_item(item)
    db.close()
