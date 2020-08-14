import enum


class Rarity(enum.Enum):
    Common = enum.auto()
    Uncommon = enum.auto()
    Rare = enum.auto()
    Legendary = enum.auto()
    Unique = enum.auto()


class Item:
    def __init__(self, id: int, iid: int, gid: int, name: str, desc: str, rarity: Rarity):
        self.ID = id
        self.ItemID = iid
        self.GuildID = gid
        self.Name = name
        self.Description = desc
        self.Rarity = rarity
