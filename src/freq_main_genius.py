#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports and data structures
import os
import re
from freq.freqAnalysis import freqAnalyzer
from freq.freqAnalysis import freqVisual
from db import database

#####################################################################
# query all lyrics from specified genres into bulk list 
#####################################################################

# connect to derived database
dbi = database.Database(path_to_db = os.getcwd()+"/db/db_genius.db",
                        path_to_schema = os.getcwd()+"/db/schema.sql")
cur = dbi.get_connection().cursor()

# define data structures
genres = ["HipHop", "Rock'n'Roll", "Country"]
genresLyrics = []

for i in genres:
    # query databases and fill genresLyrics
    query = "SELECT lyrics FROM songs WHERE genre LIKE ?"
    cur.execute(query, ('%'+i+'%',))
    genresLyrics.append(cur.fetchall())

# this process will tokenize lyrics and save their corresponding files as csvs
genresLyrics = [[re.sub(r'\([^)]*\)|\[[^)]*\]', '', l[0]) for l in item if l[0] != None] for item in genresLyrics]

# tokenize lyrics here
w = freqAnalyzer.tokenizeLyrics(genresLyrics, genres)

# call out freq class and clean lyrics
w.cleanLyrics()

# redefine file and find unique words, using variable from above chunk
s = freqVisual(w.filesClean)
words = s.uniqueWords(limit = 50)
i = 0

# process WordClouds
for g in genres:
    s.makeCloud(words[i], "cloud" + g + "Plain", None, width = 800, height = 600)
    i += 1

#####################################################################
# see if we can get significant data from the 1900s-2000s
#####################################################################

# connect to derived database
dbi = database.Database(path_to_db = os.getcwd()+"/db/db_genius.db",
                        path_to_schema = os.getcwd()+"/db/schema.sql")
cur = dbi.get_connection().cursor()

# define data structures
genresLyrics = []
years = ["19", "20"]

for i in years:
    # query databases and fill genresLyrics
    query = "SELECT lyrics FROM songs WHERE (genre LIKE 'HipHop' and year LIKE ?);"
    cur.execute(query, ('%'+i+'%',))
    genresLyrics.append(cur.fetchall())

# this process will tokenize lyrics and save their corresponding files as csvs
genresLyrics = [[re.sub(r'\([^)]*\)|\[[^)]*\]', '', l[0]) for l in item if l[0] != None] for item in genresLyrics]

genres = ["HipHop19", "HipHop20"]
# tokenize lyrics here
w = freqAnalyzer.tokenizeLyrics(genresLyrics, genres)

# call out freq class and clean lyrics
w.cleanLyrics()

# redefine file and find unique words, using variable from above chunk
s = freqVisual(w.filesClean)
words = s.uniqueWords(limit = 50, findUnique = False)
i = 0

# process WordClouds
for g in genres:
    s.makeCloud(words[i], "cloud" + g + "Plain2", None, width = 800, height = 600)
    i += 1