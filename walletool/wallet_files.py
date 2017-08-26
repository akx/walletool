# -- encoding: UTF-8 --
import collections
import os


def read_wallet_dat(filename):
    from bsddb3 import db
    filename = os.path.realpath(filename)
    env = db.DBEnv()
    env.set_lk_detect(db.DB_LOCK_DEFAULT)
    env.open(
        os.path.dirname(filename),
        db.DB_PRIVATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL | db.DB_CREATE,
    )
    d = db.DB(env)
    d.open(filename, 'main', db.DB_BTREE, db.DB_THREAD | db.DB_RDONLY)
    return collections.OrderedDict((k, d[k]) for k in d.keys())
