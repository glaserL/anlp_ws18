from db import database
import csv
import sys
db = database.Database()
connection = db.get_connection()
# connection.execute("SELECT *;")
BATCHSIZE = 1000
delimiter = ';'
if len(sys.argv)>2:
    delimiter = sys.argv[2]
with open(sys.argv[1], encoding='utf-8', mode='r') as f:
    try:
        from tqdm import tqdm
        iterator = tqdm(csv.DictReader(f, delimiter = delimiter))
    except ModuleNotFoundError:
        iterator = csv.DictReader(f, delimiter = delimiter)
    c = 0
    try:
        statements = []
        for line in iterator:
            c += 1
            # [print(type(line[key])) for key in ['song','artist','year','genre','lyrics']]
            statement = {key : line[key] for key in
                        ['song','artist','year','genre','lyrics']}
            statements.append(statement)
            # connection.execute("INSERT INTO songs VALUES(NULL, :song, :artist, :year, :genre, :lyrics)", statement)

            if c % BATCHSIZE == 0:
                connection.executemany("INSERT INTO songs VALUES(NULL, :song, :artist, :year, :genre, :lyrics)", statements)
                statements.clear()
    except csv.Error:
            print('csv choked on line %s' % (c+1))
            connection.close()
    connection.close()
