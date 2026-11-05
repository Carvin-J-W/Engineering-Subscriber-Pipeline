#!/usr/bin/env python
# coding: utf-8

# Please note that Jupyter Notebook was used for to view outputs and you will not be able to see those outputs. I will also upload the jupyter notebook in the repository.

import pandas as pd
import sqlite3


# Inspecting local SQL Database

con = sqlite3.connect('cademycode.db')
curs = con.cursor()

curs.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""").fetchall()
# Output contained three tables: cademycode_courses, cademycode_student_jobs, cademycode_students

curs.execute("""SELECT * FROM cademycode_courses""").fetchmany(5)

curs.execute("""SELECT * FROM cademycode_student_jobs""").fetchmany(5)

curs.execute("""SELECT * FROM cademycode_students""").fetchmany(5)



# Transforming SQL Databases into Pandas Dataframes

cmc_courses = pd.read_sql_query("""SELECT * FROM cademycode_courses""", con)

cmc_student_jobs = pd.read_sql_query("""SELECT * FROM cademycode_student_jobs""", con)

cmc_students = pd.read_sql_query("""SELECT * FROM cademycode_students""", con)


# Inspecting and Cleaning Data


print(cmc_courses.head())
print("------------------------------")
print(cmc_student_jobs.head())
print("------------------------------")
print(cmc_students.head()) 

cmc_students = cmc_students.rename(columns={"uuid": "student_id"})

cmc_students.head()


print(cmc_courses.describe()) #Data makes sense as in doesn't need to be cleaned
print(cmc_courses.info())


print(cmc_student_jobs.describe()) # Same here
print(cmc_student_jobs.info())


#Why is there 10 career paths but 13 job ids? Will investigate below.
print(cmc_courses.career_path_name)
print("-------------------------------")
print(cmc_student_jobs.job_category)
# The column "job_category" in the student_jobs dataframe literally means where students are currently employed. Not related to courses dataframe, so all is clear. 


print(cmc_students.describe())
print(cmc_students.info()) # Definetly will change the data types to proper ints and floats respectively.

cmc_students.isna().sum() # 5 unemployed, 251 yet to complete a course, 471 with no career path, 471 with no hours studying.



cmc_students["time_spent_hrs"] = pd.to_numeric(cmc_students["time_spent_hrs"], errors="coerce").astype("float")

column_list = ["job_id", "num_course_taken", "current_career_path_id"]

for col in column_list:
    cmc_students[col] = pd.to_numeric(cmc_students[col], errors="coerce").astype("Int64")

cmc_students.info()
print(cmc_students.head())


# Creating a CSV & a Cleaned SQLite Database

merged_df = pd.merge(cmc_students, cmc_courses, left_on="current_career_path_id", right_on="career_path_id", how="left", validate="many_to_one") # Using validate to hunt down why I have dulicated in my merged dataframe
print("pre: merged_df Shape:", merged_df.shape) #12 columns indicates the lack of presence of job dataframe

merged_df = pd.merge(merged_df, cmc_student_jobs, left_on="job_id", right_on="job_id", how="left", validate="many_to_many") #Same as above, trying to figure out the source of duplication

print("merged_df Shape:", merged_df.shape)

merged_df = merged_df.drop_duplicates() #Had to drop redundant rows. Manually inspected CSV to ensure I wasn't dropping valuable information.

print("post-drop merged_df Shape:", merged_df.shape)


# Creating a full-stocked analytics CSV file

merged_df.to_csv("revised-subscriber-data.csv", index=False)


# Creating a clean SQL database

out_con = sqlite3.connect("cleaned-cademycode-GitHub.db")

cmc_courses.to_sql("cademycode_courses", out_con, if_exists="replace", index=False)

cmc_student_jobs.to_sql("cademycode_student_jobs", out_con, if_exists="replace", index=False)

cmc_students.to_sql("cademycode_students", out_con, if_exists="replace", index=False)




