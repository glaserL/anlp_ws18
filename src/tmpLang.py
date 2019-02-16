from langdetect import detect
from db import database
import csv
import os
from ast import literal_eval as make_tuple

db = database.Database()
conn = db.get_connection()

select_statement = ("SELECT "
                    "id, artist, title, lyrics "
                    "FROM songs "
                    ";")

cur = conn.cursor()
cur.execute(select_statement)

iterator = cur.fetchall()

path = os.path.dirname(os.getcwd()) + "/tmp/lang.csv"

# write list to clear memory
with open(path, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for sql_id, artist, title, lyrics in iterator:
        statements = []
        try:
            language = detect(lyrics[:1000])
        except:
            language = "NA"
        statements.append((sql_id, artist, title, language))
        writer.writerows([statements])

with open(path, 'r') as f:
    reader = csv.reader(f)
    ls = list(reader)

ls = [make_tuple(el[0]) for el in ls]