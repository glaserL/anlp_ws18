#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import nltk
import numpy as np
from db import database
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

select_statement = "SELECT id, lyrics FROM songs WHERE sentiment IS NULL;"
update_statement = "UPDATE songs SET sentiment = ? WHERE id = ?;"
analyzer = SentimentIntensityAnalyzer()

def _senti(do):
    sql_id, lyrics = do
    test = lyrics.splitlines()
    test = [re.sub(r'\([^)]*\)|\[[^]]*\]|\{[^}]*\}', '', l) for l in test]
    test = [nltk.sent_tokenize(el) for el in test if el != ""]
    test = [item for el in test for item in el]
    test = [analyzer.polarity_scores(sentence)["compound"] for sentence in test]
    test = np.mean(test)
    return (test, sql_id)

def senti():
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(select_statement)
    iterator = tqdm(cur.fetchall())
    statements = []
    for el in iterator:
        res = _senti(el)
        statements.append(res)
        if len(statements) >= 1000:
            conn.executemany(update_statement, statements)
            conn.commit()
            statements.clear()
    conn.executemany(update_statement, statements)
    conn.commit()
    conn.close()