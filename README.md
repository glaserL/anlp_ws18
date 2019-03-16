# ANLP :fire: Haxxors 2018

## Table of Contents
* [Overview](#Overview)
* [Usage](#Usage)
* [Authors](#Authors)

## Overview
For this project, we analyzed lyrics we collected from genius.com. We performed various cleaning, annotation and analytical methods on the collected data. To view the results of our analysis, check [Data Summarization](/docs/summary/README.md).

## Usage
### Overview of directories

```shell
$ tree -d -L 1
.
├── data # storage of large data
├── docs # documentation on project
├── src # source code, classes/functions
└── tmp # temporary or old scripts

4 directories
```

### Data Scraping

Under development :cloud:

### Data Processing and Visualization

To process the scraped database and conduct visualization, run the following:

```shell
$ cd ./src

$ python3 main_dbproc.py

$ python3 main_stats.py
```

### Guidelines for Pull Requests

For guidelines on submitting pull requests, feel free to refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## Authors

Atreya Shankar (:snail:), Jules Hanel (:snake:), Luis Glaser (:chipmunk:)

Cognitive Systems 2018, Advanced Natural Language Processing (ANLP)
