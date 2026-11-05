# Data Engineered Subscriber Pipeline

This repository is one of my portfolio projects from Codecademy. This project is a Data Engineering pipeline that transforms data for a fictional subscription company. 

## What Files Are There?

I have automated most of the processes to a BASH script that will run with files in respective directories. The main directory is called "subscriber-pipeline" which contains a dev directory, a production directory, and the BASH script called "run_pipeline.sh". The dev folder holds all of the python files and logs while the production folder holds the end-state clean database. 

The main files used in the pipeline are inspect_database.py, test-pipeline.py, and update-pipeline.py. In inspect_database.py, the python code checks each databases (original, updated) and sees if there tables schemas and column structures are the same. Next, test-pipeline.py is composed of four unit tests that check for:

1. That the SQL table schemas are that same.
2. Tests if table joins initiate properly from the updated database.
3. Tests to see if new rows are present in the updated database student table.
4. Checks for duplicate uuids (cleaned version = student_id) present in the updated database.

The last file in the pipeline is update-pipeline.py. The update python file reads in new data, the updated database gets cleaned, finds new students, validates new students, then lastly saves new students in a final database.

Please note there are two log files in the dev directory. One is called changelog.log and it writes events that happen in the pipeline process. The second is called error.log and it logs exceptions that happen during unit tests.

If at any time during the BASH script one python file returns an error, then the whole script will stop. If though, the script is successful and uploads new students, the changelog will contain "Database updated." and the cleaned database will be copied into production. 

## How To Run The Code:

### Requirements:

-  Python 3.10 or later
-  pandas library

The project uses Python's standard library modules sqlite3, logging, unittest, and sys, which are included with Python and require no separate installation.

Install the only third-party dependency with:
pip install pandas

### Main Set-Up

To run the code you will need a meta directory that does not need a specific name but needs to house dev, production, and run_pipeline.sh. Inside of dev make sure you have downloaded: cademycode.db, cademycode-updated.db, Initial-Transforming.py (or Jupyter version), inspect-database.py, test-database.py, and update-database.py. The production directory should be made but empty (only after a successful pipeline run will a database appear). Please look at the github directory set up as it mimics what it should look like in your computer. The logs will create themselves once the code is run. In steps run:
1. Initial-Transforming.py (or Jupyter version)
2. Then run_pipeline.sh

If successful both your systems output in Git Bash will tell you:
"New data detected. Deploying database...
Production database updated.
Pipeline completed successfully."
and the last line of your changelog will be "(*Date Ran*) - INFO - Database updated. 1000 new rows added to cleaned-cademycode-GitHub.db.". 

If you have any issues please feel free to email me at carvinjwilson@gmail.com and I will assist you.

