class Account:
    def __init__(self, gid, did, user, balance, shame, aid=0):
        self.ID = aid
        self.GuildID = gid
        self.DiscordID = did
        self.DiscordUsername = user
        self.Balance = balance
        self.ShameReducedCount = shame
