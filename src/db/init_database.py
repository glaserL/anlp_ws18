import database as db
import csv
import sys
BATCHSIZE = 1000
def loadIntoDatabaseCSV(path_to_csv):
    database = db.Database()
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

def init(datapath = "../trainData/lyrics.csv"):
    loadIntoDatabaseCSV(datapath)

if __name__ == "__main__":
    if len(sys.argv)>1:
        init(sys.argv[1])
    else:
        init()
