#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm
import multiprocessing
from db import database
from langdetect import detect
from multiprocessing import Pool

select_statement = ("SELECT id, lyrics FROM songs WHERE language IS NULL;")
update_statement = ("UPDATE songs SET language = ? WHERE id = ?;")

def _lang(do):
    sql_id,lyrics = do
    try:
       language = detect(lyrics[:1000])
    except:
        language = "NA"
    return (language, sql_id)

def langUpdate(nocores = None, chunksize = 100):
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(select_statement)
    if nocores == 1 or multiprocessing.cpu_count() == 1:
        statements = []
        iterator = tqdm(cur.fetchall())
        for el in iterator:
            res = _lang(el)
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
            statements = list(tqdm(p.imap_unordered(_lang, iterator, chunksize), total=len(iterator)))
        conn.executemany(update_statement, statements)
        conn.commit()
        conn.close()
    return 0
