# Database Interface

* Short explanation how to interface with our data

## Setup
You should have our 'lyrics.csv' somewhere and unpacked. Then call:
`python3 db/init_database.py`
In case you put the database file anywhere else, hand it as a commandline argument
`python3 db/init_database.py PATH_TO_FILE`


## Querying
In case you're unfamiliar with SQL, you can import the database pseudo interface.
e.g. when your script sits in `src/`:

```
from db import database

dbi = database.Database()
result = dbi.simple_query(columns = ['artist', 'title'], # what columns to select
            artist = 'Rihanna') # criteria to match
```

Unfortunately, with abstraction can lead to feature scarceness. Thus, if the database interface is missing anything, you can directly query the database, however this requires SQL.

```
from db import database

dbi = database.Database()
cur = db.get_connection().cursor()

query = "SELECT artist, title FROM songs WHERE artist = Rihanna;"
cur.execute(query)
result = cur.fetchall()
```

## Splitting data

If you want to create training and test sets from your csv files, you can use the `split_data.py` script. It does feature help message, however a sample call:
`python3 split_data.py --file ../trainData/lyrics.csv --out ..trainData/lyrics_split --train 0.7`
In future this will also support splitting from database directly.
