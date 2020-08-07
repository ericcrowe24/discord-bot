from economy_module.data_access.account_connection import AccountConnection


def init_tables():
    db = AccountConnection()
    db.create_tables()
    db.close()


def add_account(author):
    db = AccountConnection()
    db.add_account(author)
    db.close()


def get_account_by_did(gid, did):
    db = AccountConnection()
    account = db.get_account_by_did(gid, did)
    db.close()

    return account


def update_account(account):
    db = AccountConnection()
    db.update_account(account)
    db.close()
