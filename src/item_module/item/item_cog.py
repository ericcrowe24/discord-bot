from discord.ext import commands
from item_module.item import item_access
from item_module.item.item import Item, Rarity


class ItemCog(commands.Cog):

    @commands.group()
    async def item(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        ctx.send("Please specify what you would like to do, !help item for a list of commands")

    @item.command()
    async def add(self, ctx, *args):
        if args[2] not in (Rarity.COMMON.name.lower(), Rarity.UNCOMMON.name.lower(), Rarity.RARE.name.lower(),
                           Rarity.LEGENDARY.name.lower(), Rarity.UNIQUE.name.lower()):
            await ctx.send("Rarity must be one of:\n"
                           + Rarity.COMMON.name.lower() + "\n"
                           + Rarity.UNCOMMON.name.lower() + "\n"
                           + Rarity.RARE.name.lower() + "\n"
                           + Rarity.LEGENDARY.name.lower() + "\n"
                           + Rarity.UNIQUE.name.lower())
            return

        rarity = _get_rarity(args[2])

        item = Item(0, 0, ctx.guild.id, args[0], args[1], rarity)

        item_access.add_item(item)

    @item.group()
    async def remove(self, ctx):
        raise NotImplementedError

    @remove.command()
    async def id(self, ctx, *, id):
        raise NotImplementedError

    @remove.command()
    async def name(self, ctx, *, name):
        raise NotImplementedError

    @commands.group()
    async def items(self, ctx):
        if ctx.invoked_subcommand is None:
            raise NotImplementedError
        raise NotImplementedError

    @items.command()
    async def rarity(self, ctx, *, rarity):
        raise NotImplementedError


def _get_rarity(rarity: str):
    rarities = {Rarity.COMMON.name.lower(): Rarity.COMMON,
                Rarity.UNCOMMON.name.lower(): Rarity.UNCOMMON,
                Rarity.RARE.name.lower(): Rarity.RARE,
                Rarity.LEGENDARY.name.lower(): Rarity.LEGENDARY,
                Rarity.UNIQUE.name.lower(): Rarity.UNIQUE}

    return rarities[rarity.lower()]
