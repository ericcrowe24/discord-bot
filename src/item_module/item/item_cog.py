from typing import List

from discord.ext import commands
from discord import Embed

from item_module.data_access.item_connection import ItemConnection
from item_module.item.item import Item, Rarity


class ItemCog(commands.Cog):
    def __init__(self):
        self._create_tables()

    @commands.group()
    async def item(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        await ctx.send("Please specify what you would like to do, !help item for a list of commands")

    @item.command()
    async def add(self, ctx, *args):
        if args[2].lower() not in (Rarity.Common.name.lower(), Rarity.Uncommon.name.lower(), Rarity.Rare.name.lower(),
                                   Rarity.Legendary.name.lower(), Rarity.Unique.name.lower()):
            await ctx.send("Rarity must be one of:\n"
                           + Rarity.Common.name.lower() + "\n"
                           + Rarity.Uncommon.name.lower() + "\n"
                           + Rarity.Rare.name.lower() + "\n"
                           + Rarity.Legendary.name.lower() + "\n"
                           + Rarity.Unique.name.lower())
            return

        rarity = self._get_rarity(args[2])

        item = Item(0, 0, ctx.guild.id, args[0], args[1], rarity)

        add_item(item)

        await ctx.send("Item added!")

    @item.command()
    async def remove(self, ctx, *, iid):
        item = get_item_by_id(ctx.guild.id, int(iid))

        delete_item(item)

        await ctx.send("Item deleted.")

    @commands.group()
    async def items(self, ctx, *, rarity=None):
        if ctx.invoked_subcommand is not None:
            return

        if rarity is None:
            items = get_all_guild_items(ctx.guild.id)
        else:
            items = get_items_by_rarity(ctx.guild.id, self._get_rarity(rarity))

        desc = ""

        for item in items:
            desc += item.Name + ", " + str(item.ItemID) + ", " + item.Rarity.name + ": " + item.Description + "\n"

        await ctx.send(embed=Embed(title="Items", description=desc))

    def _get_rarity(self, rarity: str):
        rarities = {Rarity.Common.name.lower(): Rarity.Common,
                    Rarity.Uncommon.name.lower(): Rarity.Uncommon,
                    Rarity.Rare.name.lower(): Rarity.Rare,
                    Rarity.Legendary.name.lower(): Rarity.Legendary,
                    Rarity.Unique.name.lower(): Rarity.Unique}

        return rarities[rarity.lower()]

    def _create_tables(self):
        create_tables()


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


