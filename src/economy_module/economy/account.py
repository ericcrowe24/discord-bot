class Account:
    def __init__(self, gid, did, balance, shame, aid=0):
        self.ID = aid
        self.GuildID = gid
        self.DiscordID = did
        self.Balance = balance
        self.ShameReducedCount = shame
