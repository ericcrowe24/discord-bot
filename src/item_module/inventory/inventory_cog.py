from typing import List

from discord.ext import commands

from item_module.data_access.inventory_connection import InventoryConnection

from item_module.inventory.inventory import Inventory


class InventoryCog(commands.Cog):
    def inventory(self, ctx):
        inv = get_inventory_by_discord_id(ctx.guild.id, ctx.author.id)

        if inv is None:
            await ctx.send("You have no items")


def add_inventory(gid: int, did: int):
    db = InventoryConnection()
    db.add_inventory(gid, did)
    db.close()


def get_inventory_by_discord_id(gid: int, did: int) -> Inventory:
    db = InventoryConnection()
    inv = db.get_inventory_by_discord_id(gid, did)
    db.close()

    return inv


def get_guild_inventories(gid: int) -> List[Inventory]:
    db = InventoryConnection()
    invs = db.get_guild_inventories(gid)
    db.close()

    return invs


def delete_inventory(gid: int, did: int):
    db = InventoryConnection()
    db.delete_inventory(gid, did)
    db.close()

