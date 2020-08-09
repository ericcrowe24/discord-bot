import enum


class Rarity(enum.Enum):
    COMMON = enum.auto()
    UNCOMMON = enum.auto()
    RARE = enum.auto()
    LEGENDARY = enum.auto()
    UNIQUE = enum.auto()


class Item:
    def __init__(self, gid: int, name: str, desc: str, rarity: Rarity, iid=0):
        self.ItemID = iid
        self.GuildID = gid
        self.Name = name
        self.Description = desc
        self.Rarity = rarity


class UserItem:
    def __init__(self, gid: int, uid: int, amt: int, iid=0):
        self.ItemID = iid
        self.GuildID = gid
        self.UserID = uid
        self.Amount = amt
