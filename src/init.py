# -*- coding: utf-8 -*-
import sqlite3
from src.tools.db import DB
from src.tools.path import Path

def init_database():
    if Path.is_file(Path.db_path):
        DB.set_conn(sqlite3.connect(Path.db_path))
    else:
        DB.set_conn(sqlite3.connect(Path.db_path))
        # 没有数据库就新建一个出来
        with open(Path.sql_path) as sql_script:
            DB.cursor.executescript(sql_script.read())
        DB.commit()
