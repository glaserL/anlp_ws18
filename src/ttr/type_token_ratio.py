import ast
from db import database
from collections import defaultdict

def ttr_update():
    """
    Fetches all PoS-tagged lyrics without assigned type-token radio from the database.
    Then calls the ttr-calculation function and updates the database with
    the resulting values for each song
    """
    # get all english songs without ttr from the data base
    db = database.Database()
    conn = db.get_connection()
    select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en' AND ttr IS NULL;")
    update_statement = ("UPDATE songs SET ttr = ? WHERE id = ?;")
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = cur.fetchall()
    work = [(sqlid, ast.literal_eval(el)) for sqlid, el in iterator]
    statements = type_token_ratio(work)
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()
    return 0

def type_token_ratio(work):
    """
    Calculates the type token ratio of the songs from the database
    Type token ratio = (number_of_types/number_of_tokens)*100
    The higher the number, the greater the lexical variety
    :param work: PoS tagged song lyrics from the database
    :return: list of tuples (song id, type_token_ratio)
    """
    ttr_db = []
    for elem in work:
        ttr_dict = defaultdict(int)
        lyrics = [item for sublist in elem[1] for item in sublist]
        lyrics = [i for i in lyrics if i[0] not in [',', '.', "'", '?', '!', '’', '&', '#', ':']]
        for tuples in lyrics:
            word = tuples[0]
            ttr_dict[word] += 1
        try:
            ttr = (len(ttr_dict) / sum(ttr_dict.values()))*100
        except:
            ttr = -1
        ttr_db.append((ttr, elem[0]))
    return ttr_db
