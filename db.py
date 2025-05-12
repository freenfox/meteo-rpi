import sqlite3
from contextlib import contextmanager

DB = "/home/admin/meteo-rpi/db.db"  # TODO: À compléter

@contextmanager
def connect_db():
    conn = sqlite3.connect(DB)
    try:
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute('PRAGMA encoding = "UTF-8"')
        yield cur
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()

def exec_dict(cur, query, params=None):
    if params is None:
        cur.execute(query)
    else:
        cur.execute(query, params)
    columns = [col[0] for col in cur.description]
    return [dict(zip(columns, row)) for row in cur.fetchall()]

if __name__ == '__main__':
    print("Initialisation de la base de données...")
    with connect_db() as cur:
        with open('create_db.sql') as f:
            cur.executescript(f.read())
    print("Base de données initialisée.")