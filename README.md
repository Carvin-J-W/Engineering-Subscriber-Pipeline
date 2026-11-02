# Data Engineered Subscriber Pipeline

This repository is one of my portfolio projects from Codecademy. This project is a Data Engineering pipeline that transforms data for a fictional subscription company. 

## How It Works:

I have automated most of the processes to a BASH script that will run with files in respective directories. The main directory is called "subscriber-pipeline" which contains a dev directory and a production directory. The dev folder holds all of the python files and logs while the production folder holds the end-state clean database. 

The main files used in the pipeline are inspect_database.py, test-pipeline.py, and update-pipeline.py. In inspect_database.py, the python code checks each databases (original, updated) and sees if there tables schemas and column structures are the same. Next, test-pipeline.py is composed of three unit tests that check for:
1. That the SQL table schemas are that same.
2. Tests if table joins initiate properly from the updated database.
3. Tests to see if new rows are present in the updated database student table.
The last file in the pipeline is update-pipeline.py. The update python file reads in new data, cleans the to be updated database, finds new students, validates new students, then lastly saves new students in a database.

Please note there are two log files in the dev directory. One is called changelog.log and it writes events that happen in the pipeline process. The second is called error.log and it logs exceptions that happen during unit tests.

If at any time during the BASH script one python file returns an error, then the whole script will stop. If though, the script is successful and uploads new students, the changelog will contain "Database updated." and the cleaned database will be copied into production. 


