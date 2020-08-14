from discord.ext import commands
from discord import Embed
from item_module.item import item_access
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

        item_access.add_item(item)

        await ctx.send("Item added!")

    @item.command()
    async def remove(self, ctx, *, iid):
        item = item_access.get_item_by_id(ctx.guild.id, int(iid))

        item_access.delete_item(item)

        await ctx.send("Item deleted.")

    @commands.group()
    async def items(self, ctx, *, rarity=None):
        if ctx.invoked_subcommand is not None:
            return

        if rarity is None:
            items = item_access.get_all_guild_items(ctx.guild.id)
        else:
            items = item_access.get_items_by_rarity(ctx.guild.id, self._get_rarity(rarity))

        desc = ""

        for item in items:
            desc += item.Name + ", " + str(item.ItemID) + ", " + item.Rarity.name + ": " + item.Description + "\n"

        await ctx.send(embed=Embed(title="Items", description=desc))

    def _get_rarity(self,rarity: str):
        rarities = {Rarity.Common.name.lower(): Rarity.Common,
                    Rarity.Uncommon.name.lower(): Rarity.Uncommon,
                    Rarity.Rare.name.lower(): Rarity.Rare,
                    Rarity.Legendary.name.lower(): Rarity.Legendary,
                    Rarity.Unique.name.lower(): Rarity.Unique}

        return rarities[rarity.lower()]

    def _create_tables(self):
        item_access.create_tables()


