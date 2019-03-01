#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import csv
import os
from tqdm import tqdm
from collections import Counter
from db import database

genres = ["Country", "Pop", "Hip-Hop"]
s1 = 'SELECT frequency FROM songs WHERE (year NOT LIKE "2%" OR year IS "2000") AND genre IS ?;'
s2 = 'SELECT frequency FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" AND genre IS ?;'
s3 = 'SELECT frequency  FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" AND genre IS ?;'

def getFreqRefined(m):
    for genre in genres:
        print("\nWorking on "+genre+"\n")
        t = []
        super_list = []
        db = database.Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(s1, (genre,))
        t.append(cur.fetchall())
        cur.execute(s2, (genre,))
        t.append(cur.fetchall())
        cur.execute(s3, (genre,))
        t.append(cur.fetchall())
        conn.commit()
        conn.close()
        for d in t:
            small = [Counter(ast.literal_eval(elem[0])) for elem in tqdm(d)]
            super_list.append(dict(sum(small, Counter()).most_common()))
        keys = set(super_list[0].keys()).intersection(set(super_list[1].keys())).intersection(set(super_list[2].keys()))
        common_list = [{key:d[key] for key in keys} for d in super_list]
        common_list = [Counter(d) for d in common_list]
        max_keys = dict(sum(common_list, Counter()).most_common()[:m]).keys()
        common_list = [{key:d[key] for key in max_keys} for d in super_list]
        if genre == "Country":
            string = 'w'
        else:
            string = 'a'
        with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), "../data/freqRefined.csv"), string) as o:
            writer = csv.writer(o)
            writer.writerow([key for key, value in common_list[0].items()])
            for i in range(len(common_list)):
                writer.writerow([value for key, value in common_list[i].items()])

def getFreq(m):
    for genre in genres:
        print("\nWorking on "+genre+"\n")
        t = []
        super_list = []
        db = database.Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(s1, (genre,))
        t.append(cur.fetchall())
        cur.execute(s2, (genre,))
        t.append(cur.fetchall())
        cur.execute(s3, (genre,))
        t.append(cur.fetchall())
        conn.commit()
        conn.close()
        for d in t:
            small = [Counter(ast.literal_eval(elem[0])) for elem in tqdm(d)]
            super_list.append(dict(sum(small, Counter()).most_common()[:m]))
        if genre == "Country":
            string = 'w'
        else:
            string = 'a'
        with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), "../data/freq.csv"), string) as o:
            writer = csv.writer(o)
            for i in range(len(super_list)):
                writer.writerow([key for key, value in super_list[i].items()])
                writer.writerow([value for key, value in super_list[i].items()])