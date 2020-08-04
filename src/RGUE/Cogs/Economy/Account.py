class Account:
    def __init__(self, did, user, balance, shame, aid=0):
        self.ID = aid
        self.DiscordID = did
        self.UserName = user
        self.Balance = balance
        self.ShameReducedCount = shame
