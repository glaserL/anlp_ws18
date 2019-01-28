# Database Interface

* Short explanation how to interface with our data

## Setup
You should have our 'lyrics.csv' somewhere and unpacked (default path is '/data/lyrics.csv'). Then call:
`python3 db/init_database.py`
In case you put the database file anywhere else, hand it as a commandline argument
`python3 db/init_database.py -c PATH_TO_FILE`

Additionally, you can also specify the path to a desired database and schema: `python3 db/init_database.py -c <path_to_csv> -d <path_to_db> -s <path_to_schema>`

## Querying (Simple, Tight)
In case you're unfamiliar with SQL, you can import the database pseudo interface.
e.g. when your script sits in `src/`:

```
from db import database

dbi = database.Database()
result = dbi.simple_query(columns = ['artist', 'title'], # what columns to select
            artist = 'beyonce') # criteria to match
```

Unfortunately, with abstraction can lead to feature scarceness. Thus, if the database interface is missing anything, you can directly query the database, however this requires SQL.

## Querying (Advanced, Broad)

```
from db import database

dbi = database.Database()
cur = db.get_connection().cursor()

query = "SELECT artist, title FROM songs WHERE LOWER(artist) LIKE '%beyonce%';"
cur.execute(query)
result = cur.fetchall()
```

This allows matching of artist strings containing 'beyonce' substrings, which might be better for collecting more ambiguous artist names containing 'beyonce'. Note, this search is also case-insensitive thereby allowing for more matchings.

## Splitting data

If you want to create training and test sets from your csv files, you can use the `split_data.py` script. It does feature help message, however a sample call:
`python3 split_data.py --file ../trainData/lyrics.csv --out ..trainData/lyrics_split --train 0.7`
In future this will also support splitting from database directly.
