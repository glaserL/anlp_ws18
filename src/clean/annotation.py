#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dependencies
import re
import nltk
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool
from db import database

# engineer statements
select_statement = ("SELECT id, lyrics FROM songs WHERE language IS 'en' AND postagged IS NULL;")
update_statement = ("UPDATE songs SET postagged = ? WHERE id = ?;")

def _anno(do):
    res = []
    
    for sql_id, lyrics in do:
        test = lyrics.splitlines()
        test = [re.sub(r'\([^)]*\)|\[[^)]*\]', '', l) for l in test]
        test = [nltk.pos_tag(nltk.word_tokenize(b)) for el in test for b in nltk.sent_tokenize(el) if el != ""]
        res.append((str(test), sql_id))
        
    return res

def annotate(nocores=None, chunksize = 100):

    if nocores == 1 or multiprocessing.cpu_count() == 1:
        # initialize connection
        db = database.Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(select_statement)
        statements = []
        
        # initiliaze progress bar and query
        iterator = tqdm(cur.fetchall())
        
        # start loop for annotation
        for sql_id, lyrics in iterator:
        
            test = lyrics.splitlines()
            test = [re.sub(r'\([^)]*\)|\[[^)]*\]', '', l) for l in test]
            test = [nltk.pos_tag(nltk.word_tokenize(b)) for el in test for b in nltk.sent_tokenize(el) if el != ""]
            statements.append((str(test), sql_id))
        
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
            
        db = database.Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(select_statement)
        iterator = cur.fetchall()

        with Pool(nocores) as p:
           statements = list(tqdm(p.imap_unordered(_anno, [iterator[i:i+chunksize] for i in range(0, len(iterator),chunksize)]), total=len(iterator)/chunksize))
        
        statements = [item for sublist in statements for item in sublist]
        conn.executemany(update_statement, statements)
        conn.commit()
        conn.close()