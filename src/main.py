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
# work on frequency analysis for words
########################################################

# import functions
from freq import freqAnalysis
# run in parallel manner
freqAnalysis.frequency()

########################################################
# work on average word length for lyrics
########################################################

# import functions
from avg_word_length import avg_word_length
# run
avg_word_length.word_length_update()

########################################################
# work on non standard word ratio for lyrics
########################################################

# import functions
from non_std_words import non_std_words
# run
non_std_words.non_std_update()

########################################################
# work on egocentrism score for lyrics
########################################################

# import function
from egocentrism import egocentrism
#run
egocentrism.egocentrism_update()

########################################################
# work on sentiment analysis
########################################################

# import function
from sentiment import sentiment
#run
sentiment.senti()

########################################################
# prune database by adjusting/adding ttrs
########################################################

import os
os.system("python3 prune.py")