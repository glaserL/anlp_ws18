# Data summarization

Our data was grouped into the three following groups based on the year of publishing: T1 = <1990, T2 = 2001-2010, T3 = 2011-2019.

## Data collection bias

We were successful in mitigating the temporal bias the original kaggle data had. These plots show the differences between our database and kaggle respectively:

<img src = "/data/img/genius_histogram_line.png" width = 400><img src = "/data/img/kaggle_histogram_line.png" width = 400>

## Frequency analysis

1. Below are word-clouds of the top 50 most frequent words:

<img src = "/data/img/wordclouds.png" width = "800">

2. Below we visualized the frequency of the top 20 most frequent common-words across the time steps:

<img src = "/data/img/freqbarExtend.png" width = "800">

## Data processing

We performed a range of analysis on our data. Below shows a normalized/projected spider plot for each of these metrics. The spider plot belows gives an overview of these for each unit. One inference we can draw from that is for example, that Hip-Hop is significantly more negative as other genres.

Legend:

| abbrev | metric |
|---|---|
| SEN |Sentiment value |
| SEN† |Sentiment value (negative) |
| TTR | Type- Token-Ratio |
| EGO | Measure for egocentrism |
| NSW | Non-standard words |
| AWL | Average word length |

<img src = "/data/img/spider.png" width = "800">

## Temporal changes in processed data

<img src = "/data/img/all_pvals.png" width = "800">

| abbrev | metric |
|---|---|
| * | p <= 0.05 |
| ** | p <= 0.01 |
| *** | P <= 0.001 |
| † | Significant effect size |
