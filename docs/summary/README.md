# Frequency Analysis

Using kaggle data as preliminary data, we had performed most frequent word analysis on music genres using all the data we had.

To do this, we firstly tokenized lyrics and then removed non-alphanumeric characters. Next, we removed lyrics-specific tokens such as "chorus" and "verse". Finally, we removed common stop-words such as "i" and "he".

With the resulting tokens, we then extracted tokens that were unique to each genre in order to display key differences between the genres.

The corresponding WordClouds can be seen below:

**1. Hip-Hop**

<img src = "/data/img/cloudhipPlain.png" width = "500">

**2. Country**

<img src = "/data/img/cloudcountryPlain.png" width = "500">

We also experimented using more exciting masks for word-clouds.

**1. Hip-Hop (Biggie)**

<img src = "/data/img/cloudHipMask.png" width = "500">

**2. Rock (Guitar)**

<img src = "/data/img/cloudRock.png" width = "500">


## most frequent words per genre:
We grouped our data in three by year. T1 = <1990, T2 = 2001-2010, T3 = 2011-2019.

<img src = "/data/img/freqbarExtend.png" width = "800">

## Annotations

As already mentioned, we performed a range of analysis on our data. Below shows a normalized spider plot for each of these metrics. The spider plot belows gives an overview of these for each unit. One inference we can draw from that is for example, that Hip-Hop is significantly more negative as other genres.

Legend:

| abbrev | metric |
|---|---|
|SEN|Sentiment value |
|TTR| Type- Token-Ratio |
|EGO| measure for egocentrism |
|NSW| non-standard words |
|AWL| average word length |

<img src = "/data/img/spider.png" width = "800">

### Mean change between intervals
<img src = "/data/img/all_pvals.png" width = "800">

### Collection Bias

We also were successful in mitigating the temporal bias the original kaggle data had.

<img src = "/data/img/genius_histogram_line.png" width = 400><img src = "/data/img/kaggle_histogram_line.png" width = 400>
