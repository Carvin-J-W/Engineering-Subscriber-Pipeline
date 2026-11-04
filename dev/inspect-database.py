#!/usr/bin/env python
# coding: utf-8

import sqlite3

# Reads each database and prints their table structures. Then reads each column in each table for each database.

for database in ["cademycode.db", "cademycode_updated.db"]:
    print(f"\nDatabase: {database}")

    with sqlite3.connect(database) as con:
        cursor = con.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tables = cursor.fetchall()

        for (table,) in tables:
            print(f"\nTable: {table}")

            cursor.execute(f'PRAGMA table_info("{table}")')
            columns = cursor.fetchall()

            print("Columns:", [column[1] for column in columns])

