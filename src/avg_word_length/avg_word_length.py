from db import database
import ast

"""
Computes the average word length for all songs in the lyrics data base
adds the resulting values
"""

def word_length_update():
    """
    Fetches all PoS-tagged lyrics without assigned average word length from the database.
    Then calls the average word length function and updates the database with
    the resulting values for each song
    """
    # get all english songs without avg_word_length from the data base
    db = database.Database()
    conn = db.get_connection()
    select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en' AND avg_word_length IS NULL;")
    update_statement = ("UPDATE songs SET avg_word_length = ? WHERE id = ?;")
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = cur.fetchall()
    work = [(sqlid, ast.literal_eval(el)) for sqlid, el in iterator]
    statements = avg_word_length(work)
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()
    return 0

def avg_word_length(work):
    """
    Calculates the average word length of the songs from the database

    :param work: PoS tagged song lyrics from the database
    :return: list of tuples (song id, avg_word_length)
    """
    avg_length_db = []
    for elem in work:
        avg_len = 1
        lyrics = [item for sublist in elem[1] for item in sublist]
        lyrics = [i for i in lyrics if i[0] not in [',','.', "'", '?', '!', '’', '&', '#',':']]
        lyr = []
        for tuples in lyrics:
            avg_len += len(tuples[0])
            lyr.append(tuples[0])
        avg_length_db.append(((avg_len / (len(lyrics)+0.0001)), elem[0]))
    return avg_length_db
