from db import database
import ast


def egocentrism_update():
    """
    Fetches all PoS-tagged lyrics without assigned egocentrism value from the database.
    Then calls the egocentrism function and updates the database with
    the resulting values for each song

    """
    db = database.Database()
    conn = db.get_connection()
    select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en' AND egocentrism IS NULL;")
    update_statement = ("UPDATE songs SET egocentrism = ? WHERE id = ?;")
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = cur.fetchall()
    work = [(sqlid, ast.literal_eval(el)) for sqlid, el in iterator]
    statements = egocentrism(work)
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()

    return


def egocentrism(work):
    """
    Calculates the egocentrism value of the songs from the database
    It is calculated as follows:
    (number of first person singular pronouns)/(number of second person singular pronouns)
    The higher the number, the more egocentric the song.

    :param work: PoS tagged song lyrics from the database
    :return: list of tuples (song id, egocentrism_ratio)
    """
    egocentrism_list = []
    first_person = ['i', 'me', 'my', 'mine', 'myself']
    second_person = ['you', 'your', 'yours', 'yourself']

    for elem in work:
        lyrics = [item for sublist in elem[1] for item in sublist]
        lyrics = [i for i in lyrics if i[0] not in [',', '.', "'", '?', '!', '’', '&', '#', ':']]
        count_ego = 1
        count_you = 1
        for tuples in lyrics:
            if tuples[1] in ['PRP', 'PRP$']:
                if tuples[0].lower() in first_person:
                    count_ego += 1
                if tuples[0].lower() in second_person:
                    count_you += 1
        egocentrism_list.append((count_ego / count_you, elem[0]))

    return egocentrism_list


