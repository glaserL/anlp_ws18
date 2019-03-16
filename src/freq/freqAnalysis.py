#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import multiprocessing
from db import database
from tqdm import tqdm
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter

select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en' AND frequency IS NULL")
update_statement = ("UPDATE songs SET frequency = ? WHERE id = ?;")
lemmatizer = WordNetLemmatizer()

# modified, source https://stackoverflow.com/a/15590384
def _get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return "a"
    elif treebank_tag.startswith('V'):
        return "v"
    elif treebank_tag.startswith('N'):
        return "n"
    elif treebank_tag.startswith('R'):
        return "r"
    else:
        return "n"

def _freq(do):
    sql_id, tokens = do
    ls = ast.literal_eval(tokens)
    ls = [item for sublist in ls for item in sublist]
    freq = []
    for tups in ls:
        if tups[0].lower().isalpha() and tups[0].lower() not in stopwords.words('english'):
            freq.append(lemmatizer.lemmatize(tups[0].lower(), _get_wordnet_pos(tups[1])))
    return (str(dict(Counter(freq))), sql_id)

def frequency(nocores=None, chunksize = 100):
    if nocores == None:
        nocores =  multiprocessing.cpu_count()-1
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = cur.fetchall()
    with Pool(nocores) as p:
       statements = list(tqdm(p.imap_unordered(_freq,iterator,chunksize), total=len(iterator)))
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()
    return 0
