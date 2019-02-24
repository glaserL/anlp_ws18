# Overview of directories

```shell
$ tree -d -L 1
.
├── avg_word_length # word length calculation
├── clean # detect language and POS tag
├── db # database management
├── egocentrism # egocentric analysis
├── freq # word frequency
├── non_std_words # non standard word frequency
├── scrape # data scraping
├── sentiment # vader sentiment analysis
├── split # splitting data into train/test
├── tmp # temporary scripts
├── ttr # type-token-ratio
├── unpack # unpack from string to pythonic
└── vis # visualize data

13 directories
```

## Pruning heuristics

After crawling we had 399,342 songs, steming from different genres.

| Genre | Count |
| ------- | ------ |
| Pop | 81928 |
| Rock | 38864 |
| Hip Hop | 269761 |
| Country | 8789 |

However, they included many duplicates, non-english songs, unusable metadata and even errors like a "song" from Slavoj Žižek and crossword puzzles from the New York Times. This section will describe how and we removed entries of our data.

* Removing non english songs using the python package `langdetect`
* Removed meta annotations in the lyrics e.g. [chorus]
* Merge the smallest genres, since they are similar anyhow (Rock'n'Roll & Pop)
* Remove non sensical entries like "In Progress" or tracklists of albums. We found these were songs with TTR > 85.
* Remove non-english songs that weren't recognized by `langdetect`. We found these were songs with non-standard-words-ratio >= 0.4.
