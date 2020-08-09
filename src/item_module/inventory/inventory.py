from typing import List
from item_module.item.item import Item


class Inventory:
    def __init__(self, iid: int, gid: int, did: int, items: List[Item],):
        self.InventoryID = iid
        self.GuildID = gid
        self.DiscordID = did
        self.Items = items
