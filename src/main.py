#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################
# detect languages and append back to database
########################################################

# import function
from clean import remove_not_english
# run, no argument implies parallel computation
remove_not_english.langUpdate()

########################################################
# postags lyrics and append back to database
########################################################

# import function
from clean import annotation
# run, no argument implies parallel computation
annotation.annotate()

########################################################
# unpack tokenized sentences and postags
########################################################

# import functions
from unpack import unpack
from db import database

# db-related stuff
select_statement = ("SELECT id, postagged FROM songs WHERE language IS 'en';")
db = database.Database()
conn = db.get_connection()
cur = conn.cursor()
cur.execute(select_statement)
conn.close()
test = cur.fetchall()

# define object to be unpacked, ie postagged lyrics
push = [el[1] for el in test]

# no other input will imply parallel computation
out = unpack.unpack(push)