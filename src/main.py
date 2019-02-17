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