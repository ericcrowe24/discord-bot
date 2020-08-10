import enum


class Rarity(enum.Enum):
    COMMON = enum.auto()
    UNCOMMON = enum.auto()
    RARE = enum.auto()
    LEGENDARY = enum.auto()
    UNIQUE = enum.auto()


class Item:
    def __init__(self, id: int, iid: int, gid: int, name: str, desc: str, rarity: Rarity):
        self.ID = id
        self.ItemID = iid
        self.GuildID = gid
        self.Name = name
        self.Description = desc
        self.Rarity = rarity
