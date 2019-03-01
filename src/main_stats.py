#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################
# create spider plot
########################################

from numerical_stats import vis_spider
vis_spider.run("../data/img/spider.png")

########################################
# create wordclouds
########################################

from numerical_stats import freq_stats
freq_stats.getFreq(50)
from numerical_stats import vis_freq
vis_freq.makeWordCloud("../data/img/wordclouds.png")

########################################
# create barplot
########################################

from numerical_stats import freq_stats
freq_stats.getFreqRefined(20)
from numerical_stats import vis_freq
vis_freq.makeBar("../data/img/freqbar.png")
vis_freq.makeBarExtend("../data/img/freqbarExtend.png")

########################################
# create histogram visualization
########################################
from numerical_stats import visualize_distribution
visualize_distribution.kaggle_histogram("../data/lyrics.csv")
visualize_distribution.genius_histogram()
