from db import database
import ast
import enchant

def non_std_update():
    """
    Fetches all PoS-tagged lyrics without assigned non-standard word ratio from the database.
    Then calls the non standard word function and updates the database with
    the resulting ratios for each song.
    """
    db = database.Database()
    conn = db.get_connection()
    select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en' AND non_std_words IS NULL;")
    update_statement = ("UPDATE songs SET non_std_words = ? WHERE id = ?;")
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = cur.fetchall()
    work = [(sqlid, ast.literal_eval(el)) for sqlid, el in iterator]
    statements = non_std_words(work)
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()
    return 0

def non_std_words(work):
    """
    Calculates the non standard word ratio of a song.
    If a word does not exist in the dictionary, it is a non-standard
    word.
    The non-standard word ratio is the ratio of uncommon words to all words
    in a song.
    :param work: PoS tagged song lyrics from the database
    :return: list of tuples (song id, non_standard_word_ratio)
    """
    dictionary = enchant.Dict("en_US")
    non_std_word = []
    for elem in work:
        lyrics = [item for sublist in elem[1] for item in sublist]
        lyrics = [i for i in lyrics if i[0] not in [',', '.', "'", '?', '!', '’', '&', '#', ':']]
        word_count = 1
        not_word_count = 1
        for tuples in lyrics:
            if dictionary.check(tuples[0]):
                word_count += 1
            else:
                not_word_count += 1
        non_std_word.append((not_word_count/(not_word_count+word_count), elem[0]))
    return non_std_word
