# dependencies
import re
import nltk
from db import database

# initialize connection
db = database.Database()
conn = db.get_connection()

# engineer statements
select_statement = ("SELECT id, lyrics FROM songs WHERE language IS 'en' AND postagged IS NULL;")
update_statement = ("UPDATE songs SET postagged = ? WHERE id = ?;")
cur = conn.cursor()
cur.execute(select_statement)
statements = []

# initiliaze progress bar and query
try:
    from tqdm import tqdm
    iterator = tqdm(cur.fetchall())
except ModuleNotFoundError:
    iterator = cur.fetchall()

# start loop for annotation
for sql_id, lyrics in iterator:

    test = re.sub(r'\([^)]*\)|\[[^)]*\]', '', lyrics)
    test = test.splitlines()
    test = [nltk.pos_tag(nltk.word_tokenize(b)) for el in test for b in nltk.sent_tokenize(el) if el != ""]
    statements.append((str(test), sql_id))

    if len(statements) >= 5000:
        conn.executemany(update_statement, statements)
        conn.commit()
        statements.clear()

conn.executemany(update_statement, statements)
conn.commit()
conn.close()