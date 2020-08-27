from typing import List

from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color

from item_module.data_access.inventory_connection import InventoryConnection

from item_module.inventory.inventory import Inventory
from item_module.item.item_cog import ItemCog
from item_module.user_item.user_item_cog import UserItemCog


class InventoryCog(commands.Cog):
    def __init__(self, uitems: UserItemCog, items: ItemCog):
        self.UserItem = uitems
        self.Items = items

    def inventory(self, ctx):
        inv = self.get_inventory_by_discord_id(ctx.guild.id, ctx.author.id)

        if inv is None:
            await ctx.send("You have no items")

        uitems = self.UserItem.get_user_items(inv.InventoryID)

        embed = Embed(title="Your items on" + ctx.guild.name, color=Color.magenta())

        for uitem in uitems:
            item = self.Items.get_item_by_id(ctx.guild.id, uitem.ItemID)
            embed.add_field(name=item.Name, value="Amount owned: " + str(uitem.Amount), inline=False)

        if ctx.author.dm_channel is None:
            dm = await ctx.author.create_dmchannel()
            await dm.send(embed=embed)
        else:
            ctx.author.dm_channel.send(embed=embed)

    def add_inventory(self, gid: int, did: int):
        db = InventoryConnection()
        db.add_inventory(gid, did)
        db.close()

    def get_inventory_by_discord_id(self, gid: int, did: int) -> Inventory:
        db = InventoryConnection()
        inv = db.get_inventory_by_discord_id(gid, did)
        db.close()

        return inv

    def get_guild_inventories(self, gid: int) -> List[Inventory]:
        db = InventoryConnection()
        invs = db.get_guild_inventories(gid)
        db.close()

        return invs

    def delete_inventory(self, gid: int, did: int):
        db = InventoryConnection()
        db.delete_inventory(gid, did)
        db.close()
