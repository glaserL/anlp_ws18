#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
from random import shuffle
from collections import defaultdict
from db import database

########################################################
# ttr mod function
########################################################

def type_token_ratio(elem):
    """
    Calculates the type token ratio of the songs from the database
    Type token ratio = (number_of_types/number_of_tokens)*100
    The higher the number, the greater the lexical variety

    :param work: PoS tagged song lyrics from the database
    :return: list of tuples (song id, type_token_ratio)
    """
    ttr_dict = defaultdict(int)
    lyrics = [item for sublist in elem[2] for item in sublist]
    lyrics = [i for i in lyrics if i[0] not in [',', '.', "'", '?', '!', '’', '&', '#', ':']]
    for tuples in lyrics:
        word = tuples[0]
        ttr_dict[word] += 1
    try:
        ttr = (len(ttr_dict) / sum(ttr_dict.values()))*100
    except:
        ttr = -1
    if ttr != -1:
        return (ttr, elem[0])
    else:
        return None

########################################################
# pipeline for pruning
########################################################

select = []
update = []
select.append("SELECT id, year, postagged FROM songs WHERE language IS 'en' AND ttr IS NULL AND genre IS 'Country';")
select.append("SELECT id, year, postagged FROM songs WHERE language IS 'en' AND ttr IS NULL " +
              "AND (genre IS 'Dance_Pop' OR genre IS 'Rock_n_Roll');")
select.append("SELECT id, year, postagged FROM songs WHERE language IS 'en' AND ttr IS NULL " +
              "AND (genre IS 'HipHop_Groups' OR genre IS 'HipHop_Musicians');")
update.append("UPDATE songs SET ttr = ?, genre = 'Country' WHERE id = ?;")
update.append("UPDATE songs SET ttr = ?, genre = 'Pop' WHERE id = ?;")
update.append("UPDATE songs SET ttr = ?, genre = 'Hip-Hop' WHERE id = ?;")

for i in range(len(select)):
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(select[i])
    iterator = cur.fetchall()
    g1 = []
    g2 = []
    g3 = []
    statements = []    
    for el in iterator:
        if 2011 <= int(el[1]) <= 2020:
            g1.append(el)
        elif 2001 <= int(el[1]) <= 2010:
            g2.append(el)
        elif int(el[1]) <= 2000:
            g3.append(el)
    del iterator
    test1 = [g1, g2, g3]
    test2 = [len(g1), len(g2), len(g3)]
    mini = min(test2)
    where = test2.index(mini)    
    # perform ttr completely on smallest group and commit directly
    for el in test1[where]:
        sqlid, year, postag = el
        postag = ast.literal_eval(postag)
        el = (sqlid, year, postag)
        run = type_token_ratio(el)
        if run != None:
            statements.append(run)
    bottom = len(statements)
    conn.executemany(update[i], statements)
    conn.commit()
    statements.clear()    
    # now perform ttr on remaining sets randomly
    for j in range(len(test1)):
        if j != where:
            shuffle(test1[j])
            k = 0
            while(len(statements) != bottom):
                el = test1[j][k]
                sqlid, year, postag = el
                postag = ast.literal_eval(postag)
                el = (sqlid, year, postag)
                run = type_token_ratio(el)
                if run != None:
                    statements.append(run)
                k += 1
            conn.executemany(update[i], statements)
            conn.commit()
            statements.clear()
    conn.close()

########################################################
# vacuum empty spaces
########################################################

db = database.Database()
conn = db.get_connection()
cur = conn.cursor()
cur.execute("DELETE FROM songs WHERE ttr IS NULL;")
cur.execute("VACUUM;")
conn.commit()
conn.close()
