#Script for initial database setup

import sqlite3
from sqlite3 import Error

db = 'sensor.db'

def open_database(db):
    con = None
    try:
        con = sqlite3.connect(db)
        return con
    except Error as e:
        print(e)
    return con


def create_table(con, sql):
    try:
        c = con.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def main():

    # create settings table
    create_settings_sql = (' CREATE TABLE IF NOT EXISTS settings ('
           'userid text,'
           'low_temp integer,'
           'high_temp integer,'
           'low_humidity integer,'
           'high_humidity integer,'
           'low_pressure integer,'
           'high_pressure integer,'
           'polling_frequency integer);')

    con = open_database(db)

    if con is not None:
        create_table(con, create_settings_sql)

    else:
        print("Can't open database")


if __name__ == '__main__':
    main()
