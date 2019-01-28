import database as db
import csv
import os
import argparse
BATCHSIZE = 1000

def loadIntoDatabaseCSV(path_to_csv, path_to_db, path_to_schema):
    database = db.Database(path_to_db, path_to_schema)
    connection = database.get_connection()
    with open(path_to_csv, encoding='utf-8', mode='r') as f:
        try:
            from tqdm import tqdm
            iterator = tqdm(csv.DictReader(f))
        except ModuleNotFoundError:
            iterator = csv.DictReader(f)
        c = 0
        try:
            statements = []
            for line in iterator:
                c += 1
                # [print(type(line[key])) for key in ['song','artist','year','genre','lyrics']]
                statement = {key : line[key] for key in
                            ['song','artist','year','genre','lyrics']}
                statement['title'] = statement['song']
                del statement['song'] # stupid quick fix
                statements.append(statement)
                # connection.execute("INSERT INTO songs VALUES(NULL, :song, :artist, :year, :genre, :lyrics)", statement)

                if c % BATCHSIZE == 0:
                    connection.executemany("INSERT INTO songs VALUES(NULL, :title, :artist, :year, :genre, :lyrics)", statements)
                    connection.commit()
                    statements.clear()
        except csv.Error:
            # TODO: Research what causes RuntimeError from tqdm when
            # this exception is thrown
            connection.close()

# leave defaults as such in case we call this from another main
def init(datapath = "../data/lyrics.csv", 
         path_to_db = os.path.dirname(os.path.abspath(__file__))+"/database.db",
         path_to_schema = os.path.dirname(os.path.abspath(__file__))+"/schema.sql"):
    loadIntoDatabaseCSV(datapath, path_to_db, path_to_schema)

if __name__ == "__main__":
    
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--textPath', dest = "text", action="store", default="../data/lyrics.csv")
    parser.add_argument('-d', '--dbPath', dest = "database", action="store", default=os.path.dirname(os.path.abspath(__file__))+"/database.db")
    parser.add_argument('-s', '--schemaPath', dest = "schema", action="store", default= os.path.dirname(os.path.abspath(__file__))+"/schema.sql")
    args = parser.parse_args()
    
    # initialize based on defaults
    init(args.text, args.database, args.schema)