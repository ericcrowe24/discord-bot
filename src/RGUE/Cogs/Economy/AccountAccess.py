from RGUE.DataAcces.EconomyConnection import EconomyConnection


def init_tables():
    db = EconomyConnection()
    db.create_tables()
    db.close()


def add_account(author):
    db = EconomyConnection()
    db.add_account(author)
    db.close()


def get_account_by_did(did):
    db = EconomyConnection()
    account = db.get_account_by_did(did)
    db.close()

    return account


def update_account(account):
    db = EconomyConnection()
    db.update_account(account)
    db.close()
