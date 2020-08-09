from rgue_bot.bot.data_access.shame_connection import ShameConnection


def get_all_shame_logs(gid):
    db = ShameConnection()
    logs = db.get_shame_logs(gid)
    return logs


def add_shame_log(user, reason, date):
    db = ShameConnection()
    db.add_shame_log(user, reason, date)
    db.close()
