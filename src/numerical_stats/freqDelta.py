#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import csv
import operator
import numpy as np
from scipy import stats
from collections import Counter
from db import database

genres = ["Country", "Pop", "Hip-Hop"]
s1 = 'SELECT frequency FROM songs WHERE (year NOT LIKE "2%" OR year IS "2000") AND genre IS ?;'
s2 = 'SELECT frequency FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" AND genre IS ?;'
s3 = 'SELECT frequency  FROM songs WHERE year LIKE "201%" AND year IS NOT "2010" AND genre IS ?;'

for genre in genres:
    t = []
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
    super_list = []
    sorted_list = []
    backup = []
    for d in t:
        small = [Counter(ast.literal_eval(elem[0])) for elem in d]
        backup.append(dict(small[0]))
        super_list.append(dict(sum(small, Counter()).most_common()[:50]))
    keys = {key for d in super_list for key in d.keys()}
    for i in range(len(super_list)):
        d = super_list[i]
        for key in keys:
            if key not in d.keys():
                if key in backup[i].keys():
                    d.update({key:backup[i][key]})
                else:
                    d.update({key:0})
    super_list = [sorted(d.items(), key=operator.itemgetter(0)) for d in super_list]
    sorted_list.append([[tup[1] for tup in d] for d in super_list])

# sample test
test = np.array(sorted_list[0])
stats.chi2_contingency(test)
