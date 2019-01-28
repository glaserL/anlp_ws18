#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################################
# query all lyrics from specified genres into bulk list 
#####################################################################

# imports and data structures
import os
from freq.freqAnalysis import freqAnalyzer as fa
from freq.freqAnalysis import freqVisual as fv
from db import database

# initiliaze db in repo
os.system("python3 db/init_database.py")

# connect to derived database
dbi = database.Database()
cur = dbi.get_connection().cursor()

# define data structures
genres = ["hip-hop", "rock", "country"]
genresLyrics = []

for i in genres:
    # query databases and fill genresLyrics
    query = "SELECT lyrics, year FROM songs WHERE genre LIKE ?"
    cur.execute(query, ('%'+i+'%',))
    genresLyrics.append(cur.fetchall())

#####################################################################
# pass bulk list to freqAnalyzer to generate tokens and clean lyrics
####################################################################

# this process will tokenize lyrics and save their corresponding files as csvs
w = fa.freqAnalyzer.tokenizeLyrics(genresLyrics, genres)

# call out freq class and clean lyrics
w.cleanLyrics()

#####################################################################
# find top frequency unique words and make WordClouds
#####################################################################
    
# redefine file and find unique words, using variable from above chunk
s = fv.freqVisual(w.filesClean())
words = s.uniqueWords(limit = 200)
i = 0

# process WordClouds
for g in genres:
    s.makeCloud(words[i], "cloud" + g + "Plain", None, width = 800, height = 600)
    i += 1

#####################################################################
# extra example for beyonce WordCloud
#####################################################################

# connect to derived database
dbi = database.Database()
cur = dbi.get_connection().cursor()

test = []
query = "SELECT lyrics FROM songs WHERE artist LIKE '%beyonce%'"
cur.execute(query)
test.append(cur.fetchall())
test = [[l[0] for l in item] for item in test]

w = fa.freqAnalyzer.tokenizeLyrics(test, ["beyonce"])
w.cleanLyrics()
s = fv.freqVisual(w.filesClean)
words = s.uniqueWords(limit = 50)
s.makeCloud(words[0], "cloudbeyoncePlain", None, width = 800, height = 600)

# TODO Development:
# remove dependency on reading paths, instead read directly list and output to sqlite db
# re-run on newer data once available
# read article and see other comparisons that can be made
# think of how to share db between us, git lfs