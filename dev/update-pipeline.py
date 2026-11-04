#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd
import logging


# Change loggger (sends to changelog.log)
logger = logging.getLogger("changelog")
logger.setLevel(logging.INFO)

logger_handler = logging.FileHandler("changelog.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger_handler.setFormatter(formatter)

logger.addHandler(logger_handler)



def read_data(database): #("{database}.db")

    with sqlite3.connect(database) as con:

        courses_table = pd.read_sql_query("SELECT * FROM cademycode_courses", con)
        jobs_table = pd.read_sql_query("SELECT * FROM cademycode_student_jobs", con)
        student_table = pd.read_sql_query("SELECT * FROM cademycode_students", con)

    logger.info("Read database %s: %s courses, %s jobs, %s students", database, len(courses_table), len(jobs_table), len(student_table))

    return courses_table, jobs_table, student_table



def clean_students(student_df):
    student_df = student_df.rename(columns={"uuid": "student_id"})

    # changed data types for if any pandas dataframe operations took place
    student_df["time_spent_hrs"] = (pd.to_numeric(student_df["time_spent_hrs"], errors="coerce").astype("float"))

    column_list = ["job_id", "num_course_taken", "current_career_path_id"]
    for col in column_list:
        student_df[col] = (pd.to_numeric(student_df[col], errors="coerce").astype("Int64"))

    logger.info("Student data successfully cleaned: %s rows cleaned.", len(student_df))

    return student_df



def find_new_students(new_students, cleaned_database): #(cleaned new students dataframe, older but clean database)    
    
    _, _, existing_students = read_data(cleaned_database)

    existing_ids = set(existing_students["student_id"])
    
    new_rows = new_students[~new_students["student_id"].isin(existing_ids)].copy()

    logger.info("New student identification complete. %s new student(s) found.", len(new_rows))

    return new_rows



def validate_students(student_df): # new students dataframe

    required_columns = ["student_id", "name", "dob", "sex", "contact_info", "job_id", "num_course_taken", "current_career_path_id", "time_spent_hrs"]

    if not all(col in student_df.columns for col in required_columns):
        raise ValueError("Missing required columns.")

    if student_df["student_id"].isna().any():
        raise ValueError("Student ID missing.")

    if student_df["student_id"].duplicated().any():
        raise ValueError("Duplicated Student ID found.")

    logger.info("Student validation passed. %s rows validated", len(student_df))

    return True 



def save_students(students_df, database): #new_data (cleaned/new students), "cleaned-cademycode.db" (pre-existing clean database, not updated database)
    if students_df.empty:
        print("New students already inserted.")
        logger.info("Database already up-to-date.")
        return 0

    try:
        with sqlite3.connect(database) as con: 
            students_df.to_sql("cademycode_students", con, if_exists="append", index=False)
    except Exception:
        logger.exception("Failed to insert new rows into %s.", database)
        raise

    print(f"Successfully inserted {len(students_df)} students.")

    logger.info("Database updated. %s new rows added to %s.", len(students_df), database)

    return len(students_df)


# Calling the functions
courses_df, jobs_df, student_df = read_data("cademycode_updated.db")

new_clean_students = clean_students(student_df)

new_data = find_new_students(new_clean_students, "cleaned-cademycode-GitHub.db")

validate_students(new_data)
save_students(new_data, "cleaned-cademycode-GitHub.db")

#Ran it once and Output:
#Successfully inserted 1000 students.
#1000






#Below are just some quality checks that you can optionally run: 

#Quality assurance checks. Making sure that the proper amount of student ids present after transformations.
#_,_,student_df = read_data("cleaned-cademycode.db")
#print(len(student_df))
#print(student_df["student_id"].isna().sum())
#print(student_df["student_id"].duplicated().sum())

#with sqlite3.connect("cleaned-cademycode.db") as con:
#    result = con.execute("PRAGMA integrity_check").fetchone()
#print(result)

# Quality assurance checks. Making sure proper amount of rows after save_students transformation.
#courses_df, jobs_df, student_df = read_data("cleaned-cademycode.db")
#print("Courses rows:", len(courses_df))
#print("Jobs rows:", len(jobs_df))
#print("Student rows:", len(student_df))

