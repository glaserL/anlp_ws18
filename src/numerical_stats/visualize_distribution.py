import pandas as pd
import numpy as np
from db import database
from tqdm import tqdm
import matplotlib.pyplot as plt
import os.path


def is_year(x):
    try:
        y = int(x)
        if y < 2018 and y > 1900:
            return y
        else:
            return False
    except ValueError:
        return False


def kaggle_histogram(kaggle_path):
    if os.path.isfile(kaggle_path):
        my_dpi=180
        plt.style.use('ggplot')
        plt.figure(figsize=(2200/my_dpi, 1600/my_dpi), dpi=my_dpi)

        data = pd.read_csv(kaggle_path, sep = ',', error_bad_lines = False)
        data.columns = ['id','title','year','artist','genre','ignore']
        data = data.dropna()
        del data['ignore']
        #data[data.year < data.year.quantile(.05)]

        data.year = data.year.apply(is_year)
        data = data.loc[data['year'] != False]

        for genre in ["Hip-Hop", "Pop", "Country"]:
            year_dist = data.loc[data['genre'] == genre].year.value_counts().sort_index()
            x = year_dist.keys().tolist()
            y = year_dist.tolist()
            plt.subplot(1,1,1)
            plt.plot(x, y, label = genre)
            plt.legend(loc = 'upper left')
            ax = plt.gca()
            ax.set_xlim(1965, 2020)
        plt.savefig("kaggle_histogram_line.png")
    else:
        print("No kaggle data found.")


def genius_histogram():
    my_dpi=180
    plt.style.use('ggplot')
    plt.figure(figsize=(2200/my_dpi, 1600/my_dpi), dpi=my_dpi)

    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()

    # read in data from new database
    select_statement = "SELECT genre, year, COUNT(*) FROM songs WHERE year < 2019 GROUP BY genre, year;"
    cur.execute(select_statement)
    new_counter = {
        "genre" : [],
        "year" : [],
        "count" : []
    }
    for genre, year, count in cur.fetchall():
        new_counter["genre"].append(genre)
        new_counter["year"].append(int(year))
        new_counter["count"].append(count)

    new_counter = pd.DataFrame(new_counter)

    for genre in set(new_counter.genre):
        freqs = new_counter.loc[new_counter["genre"] == genre]
        x, y = zip(*sorted(zip(freqs["year"], freqs["count"])))
        plt.subplot(1,1,1)
        plt.plot(x, y, label = genre)
        plt.legend(loc = 'upper left')
        ax = plt.gca()
        ax.set_xlim(1965, 2020)

    plt.savefig("genius_histogram_line.png")
