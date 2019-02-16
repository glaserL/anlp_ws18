"""This script will remove any non english lyrics from our database, in order to make our
analysis more feasable. Also, it serves as a template for any other annotation scripts
that we might employ.
"""
__author__ = "Luis Glaser"
__email__ = "Luis.Glaser@uni-potsdam.de"

from langdetect import detect
from db import database # necessary to access our database

db = database.Database()
conn = db.get_connection() # Connect to the database, CLOSE this object after you're done

"""below the SELECT sql statement. Note, CAPS words are SQL keywords, 
lower case are column names or other things
"""
select_statement = ("SELECT " # keyword for selecting some data
                    "id, lyrics " # which columns to select, see schema.sql for options
                    "FROM songs " # the table to get stuff from
                    "WHERE " # key word for conditions, followed by conditions seperated with AND
                    "language IS NULL" # only where we didnt fill out anything yet
                    ";") # THE HOLY SEMICOLON WELCOME TO THE EIGHTIES 

""" Then, we prepare an update statement. We leave wildcard "?" which are filled up with data
when hitting the database. This also prevents bad things as SQL Injection and broken escape 
characters.
"""
update_statement = ("UPDATE " #keyword for updating one or more existing rows
                    "songs " # the table to update
                    "SET " # following the values to update
                    "language = ? " # replaced by the first tuple element of data
                    "WHERE " # criteria where to replace above values
                    "id = ?"
                    ";")

cur = conn.cursor() # cursor are basically pointers to the database that operates on it
cur.execute(select_statement) # now the cursor is the link to what we queried for

statements = [] # This will contain the values for the wildcards above
try:
    from tqdm import tqdm # I love myself some progressbar, dont worry if you dont have it ...
    iterator = tqdm(cur.fetchall())
except ModuleNotFoundError: # ... I'll catch you. *badum tiss*
    iterator = cur.fetchall()
for sql_id, lyrics in iterator: # remember, we only selected two values in the statement above!
    
    # CHANGE BELOW TO DO STUFF
    language = detect(lyrics[:1000]) # only get the first 1000 characters to save time
    # CHANGE ABOVE TO DO STUFF

    statements.append((language, sql_id)) # and add a tuple, containing all ? you had above
    # Once in a while we want to push results to the database:
    if statements >= 5000: 
        # combine the query with the values and push them to the database in a batch
        conn.executemany(update_statement, statements)
        conn.commit() # commit to the temporary changes we just made
        statements.clear() # and remove the ones we have already comitted
conn.executemany(update_statement, statements) # write the leftovers
conn.commit()
conn.close() # close the connection so other connections can start comitting/writing