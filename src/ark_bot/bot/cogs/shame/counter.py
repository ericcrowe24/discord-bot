class Counter:
    def __init__(self, gid, did, user, date, count, cid=0):
        self.id = cid
        self.GuildID = gid
        self.DiscordID = did
        self.DiscordUsername = user
        self.Date = date
        self.Count = count
