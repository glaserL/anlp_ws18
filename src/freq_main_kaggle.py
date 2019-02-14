#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports and data structures
import os
import re
from db import database
from freq.freqAnalysis import freqAnalyzer
from freq.freqAnalysis import freqVisual
# from collections import Counter

#####################################################################
# query all lyrics from specified genres into bulk list 
#####################################################################

# initiliaze db in repo
os.system("python3 db/init_database.py \
          -c ../data/lyrics.csv \
          -d ./db/db_kaggle.db \
          -s ./db/schema_Kaggle.sql")

# connect to derived database
dbi = database.Database(path_to_db = os.getcwd()+"/db/db_kaggle.db",
                        path_to_schema = os.getcwd()+"/db/schemaKaggle.sql")
cur = dbi.get_connection().cursor()

# define data structures
genres = ["hip-hop", "rock", "country"]
genresLyrics = []

for i in genres:
    # query databases and fill genresLyrics
    query = "SELECT lyrics, year FROM songs WHERE genre LIKE ?"
    cur.execute(query, ('%'+i+'%',))
    genresLyrics.append(cur.fetchall())

# this process will tokenize lyrics and save their corresponding files as csvs
# assembles into correct structure and removes song related annotations such as
# (chorus), (verse), etc.
genresLyrics = [[re.sub(r'\([^)]*\)|\[[^)]*\]', '', l[0]) for l in item] for item in genresLyrics]  
w = freqAnalyzer.tokenizeLyrics(genresLyrics, genres)

# call out freq class and clean lyrics
w.cleanLyrics()
    
# redefine file and find unique words, using variable from above chunk
s = freqVisual(w.filesClean)
words = s.uniqueWords(limit = 200)
# words = [dict(Counter(thing).most_common()[0:100]) for thing in words]
i = 0

# process WordClouds
for g in genres:
    s.makeCloud(words[i], "cloud" + g + "Plain", None, width = 800, height = 600)
    i += 1
    
#####################################################################
# extra example for beyonce WordCloud
#####################################################################

# connect to derived database
dbi = database.Database(path_to_db = os.getcwd()+"/db/db_kaggle.db",
                        path_to_schema = os.getcwd()+"/db/schemaKaggle.sql")
cur = dbi.get_connection().cursor()

test = []
query = "SELECT lyrics FROM songs WHERE LOWER(artist) LIKE '%beyonce%';"
cur.execute(query)
test.append(cur.fetchall())
# assembles into correct structure and removes song related annotations such as
# (chorus), (verse), etc.
test = [[re.sub(r'\([^)]*\)|\[[^)]*\]', '', l[0]) for l in item] for item in test]

w = freqAnalyzer.tokenizeLyrics(test, ["beyonce"])
w.cleanLyrics()
s = freqVisual(w.filesClean)
words = s.uniqueWords(limit = 50)
s.makeCloud(words[0], "cloudbeyoncePlain", None, width = 800, height = 600)

#####################################################################
# see if we can get significant data from the 1900s
#####################################################################

# connect to derived database
dbi = database.Database(path_to_db = os.getcwd()+"/db/db_kaggle.db",
                        path_to_schema = os.getcwd()+"/db/schemaKaggle.sql")
cur = dbi.get_connection().cursor()

# define data structures
genres = ["hip-hop", "rock", "country"]
genresLyrics = []

for i in genres:
    # query databases and fill genresLyrics
    query = "SELECT lyrics FROM songs WHERE (year LIKE '%19%' and genre LIKE ?);"
    cur.execute(query, ('%'+i+'%',))
    genresLyrics.append(cur.fetchall())

# assembles into correct structure and removes song related annotations such as
# (chorus), (verse), etc.
genresLyrics = [[re.sub(r'\([^)]*\)|\[[^)]*\]', '', l[0]) for l in item] for item in genresLyrics]
w = freqAnalyzer.tokenizeLyrics(genresLyrics, ["hip19", "rock19", "country19"])
w.cleanLyrics()

genres = ["hip19", "rock19", "country19"]
# redefine file and find unique words, using variable from above chunk
s = freqVisual(w.filesClean)
words = s.uniqueWords(limit = 200)
i = 0

# process WordClouds
for g in genres:
    s.makeCloud(words[i], "cloud" + g + "Plain", None, width = 800, height = 600)
    i += 1