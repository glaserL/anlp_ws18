#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################
# create spider plot
########################################

from numerical_stats import visualize_data
visualize_data.run("../data/img/spider.png")


########################################
# create histogram visualization
########################################
from numerical_stats import visualize_distribution
visualize_distribution.kaggle_histogram("../data/lyrics.csv")
visualize_distribution.genius_histogram()
