# Overview of directories

1. `clean`

	Contains scripts for detecting language and annotating lyrics. Direct feedback from and to database. Check `main.py` for implementation.

	**Note: functions here default to parallel computation unless stated**

2. `db`

	Database-related files

3. `freq`

	Contains scripts to process lyrics and produce most frequent wordss

4. `scrape`

	Data-scraping related functions

5. `split`

	Contains scripts to split data into training/test/validation sets

6. `unpack`

	Contains scripts to unpack string data from the database and conver to python-readable formats. Check `main.py` for implementation.

	**Note: functions here default to parallel computation unless stated**

7. `tmp`

	Directory to store old or temporary scripts
