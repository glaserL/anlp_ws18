#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import nltk
import multiprocessing
from tqdm import tqdm
from multiprocessing import Pool
from db import database

select_statement = ("SELECT id, lyrics FROM songs WHERE language IS 'en' AND postagged IS NULL;")
update_statement = ("UPDATE songs SET postagged = ? WHERE id = ?;")

def _anno(do):
    sql_id, lyrics = do
    test = lyrics.splitlines()
    test = [re.sub(r'\([^)]*\)|\[[^)]*\]', '', l) for l in test]
    test = [nltk.pos_tag(nltk.word_tokenize(b)) for el in test for b in nltk.sent_tokenize(el) if el != ""]    
    return (str(test), sql_id)

def annotate(nocores=None, chunksize = 100):
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(select_statement)
    if nocores == 1 or multiprocessing.cpu_count() == 1:
        statements = []    
        iterator = tqdm(cur.fetchall())
        for el in iterator:
            res = _anno(el)
            statements.append(res)
            if len(statements) >= 5000:
                conn.executemany(update_statement, statements)
                conn.commit()
                statements.clear()
        conn.executemany(update_statement, statements)
        conn.commit()
        conn.close()
    else:
        if nocores == None:
            nocores =  multiprocessing.cpu_count()-1
        iterator = cur.fetchall()
        with Pool(nocores) as p:
           statements = list(tqdm(p.imap_unordered(_anno, iterator, chunksize), total=len(iterator)))
        conn.executemany(update_statement, statements)
        conn.commit()
        conn.close()