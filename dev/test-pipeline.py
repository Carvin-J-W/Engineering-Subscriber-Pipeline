#!/usr/bin/env python
# coding: utf-8


import sqlite3
import unittest
import logging
import sys



# error log
error_logger = logging.getLogger("errors")
error_logger.setLevel(logging.WARNING) 

error_handler = logging.FileHandler("errors.log")
formatter1 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(formatter1)

# Adding the Handler
error_logger.addHandler(error_handler)



# Database filenames
original_db = "cademycode.db"
updated_db = "cademycode_updated.db"


def get_schema(database):

    with sqlite3.connect(database) as con:
        cursor = con.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = cursor.fetchall()

        schema = {}

        for (table_name,) in tables:
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            schema[table_name] = [column[1] for column in cursor.fetchall()]

    return schema



def find_new_students(): # This check looks for any new rows in the updated database and reports changes.

    with sqlite3.connect(original_db) as original_con:
        original_ids = {row[0] for row in original_con.execute("SELECT uuid FROM cademycode_students")}

    with sqlite3.connect(updated_db) as updated_con:
        updated_students = updated_con.execute("SELECT * FROM cademycode_students").fetchall()

        columns = [description[0] for description in updated_con.execute("SELECT * FROM cademycode_students LIMIT 0").description]

    new_students = [dict(zip(columns, row)) for row in updated_students if row[columns.index("uuid")] not in original_ids]

    return new_students


def find_duplicates(column): # This is a data integrity check which looks for duplicated values in either name or uuid (later changed to "student_id")

    if column not in ("uuid", "name"):
        raise ValueError("Column must be 'uuid' or 'name'")

    with sqlite3.connect(updated_db) as con:
        query = f"""
            SELECT "{column}", COUNT(*)
            FROM cademycode_students
            WHERE "{column}" IS NOT NULL
            GROUP BY "{column}"
            HAVING COUNT(*) > 1;
            """

        return con.execute(query).fetchall()



class TestDatabaseUpdates(unittest.TestCase):

    def test_updated_database_has_same_schema(self):
        original_schema = get_schema(original_db)
        updated_schema = get_schema(updated_db)

        self.assertTrue(original_schema, "Original database has no tables")
        self.assertEqual(original_schema, updated_schema, "The original and updated database schemas do not match")

# A new addition to our testClass, checks that our joins for the tables initiate properly

    def test_updated_database_tables_join(self):

        with sqlite3.connect(updated_db) as con:
            con.execute("""
                SELECT
                    s.uuid,
                    c.career_path_name,
                    j.job_category
                FROM cademycode_students AS s
                LEFT JOIN cademycode_courses AS c
                    ON s.current_career_path_id = c.career_path_id
                LEFT JOIN cademycode_student_jobs AS j
                    ON s.job_id = j.job_id
                LIMIT 1;
            """)

# The 3rd test to check if rows have been added or not 

    def test_updated_database_has_new_students(self):

        with sqlite3.connect(original_db) as original_con:
            original_ids = {row[0] for row in original_con.execute("SELECT uuid FROM cademycode_students;")}

        with sqlite3.connect(updated_db) as updated_con:
            updated_ids = {row[0] for row in updated_con.execute("SELECT uuid FROM cademycode_students;")}

        new_students = updated_ids - original_ids

        self.assertGreater(len(new_students), 0, "No new students were found in the updated database")

    def test_updated_database_has_no_duplicate_uuids(self):
        duplicates = find_duplicates("uuid")

        self.assertEqual(duplicates, [], f"Duplicate UUIDs found: {duplicates}")



if __name__ == "__main__":

    print("New student records found:", len(find_new_students()))

    # Check for duplicate student values
    for column in ("uuid", "name"):
        duplicates = find_duplicates(column)

        if duplicates:
            message = (f"Duplicate {column} values found: {duplicates}")

            if column == "uuid":
                error_logger.error(message)
            else:
                error_logger.warning(message)
            print(message)
        else:
            print(f"No duplicate {column} values found.")



     # Run all unit tests
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDatabaseUpdates)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Record any test failures or errors
    if not result.wasSuccessful():
        for test, error in result.failures + result.errors:
            error_logger.error("Test failed: %s\n%s", test, error)

    # Return a failure status if any test failed
    sys.exit(not result.wasSuccessful())  





