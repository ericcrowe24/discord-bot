class Counter:
    def __init__(self, gid, did, date, count, cid=0):
        self.id = cid
        self.GuildID = gid
        self.DiscordID = did
        self.Date = date
        self.Count = count
