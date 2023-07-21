"""Use Python 3.11"""

import sqlite3

name_base: str = 'data_base.base'

create_tables: str = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    id_user INTEGER,
    name TEXT,
    date_registration TEXT
    );

CREATE TABLE IF NOT EXISTS user_lang (
    id_user INTEGER PRIMARY KEY,
    lang TEXT,
    FOREIGN KEY (id_user) REFERENCES users (id_user)
    )
'''


def create_table():
    db = sqlite3.connect(name_base)
    cursor = db.cursor()
    cursor.executescript(create_tables)
    db.close()


create_table()
