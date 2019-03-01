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


def kaggle_histogram(vis_folder, kaggle_path):
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
        plt.savefig(vis_folder+"/kaggle_histogram_line.png")
    else:
        print("No kaggle data found.")


def genius_histogram(vis_folder):
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

    plt.savefig(vis_folder+"/genius_histogram_line.png")


def is_year(x):
    try:
        y = int(x)
        if y < 2018 and y > 1900:
            return y
        else:
            return False
    except ValueError:
        return False

def kaggle_histogram_binned(vis_folder, kaggle_path):
    my_dpi=180
    plt.style.use('ggplot')
    plt.figure(figsize = (2200/my_dpi, 1600/my_dpi), dpi=my_dpi)

    data = pd.read_csv(kaggle_path, sep = ',', error_bad_lines = False)
    data.columns = ['ignore','ignore','year','ignore','genre','ignore']
    data = data.dropna()
    del data['ignore']
    data["year"] = data.year.apply(is_year).apply(decadify)

    data = data.groupby(by = ["year", "genre"]).size().reset_index().groupby(by = ['year', 'genre'])[0].aggregate('first').unstack().reset_index().set_index('year').reindex(["<2000", "2001-2010", "2011-2019"])
    data.plot(y = ['Country', 'Hip-Hop', 'Pop'], kind = 'bar', ax = plt.gca())

    plt.savefig(vis_folder+"/kaggle_histogram_binned.png")

def decadify(x):
    if x <= 2000:
        return "<2000"
    elif x <= 2010:
        return "2001-2010"
    else:
        return "2011-2019"

def genius_histogram_binned(vis_folder):
    my_dpi=180
    plt.style.use('ggplot')
    plt.figure(figsize = (2200/my_dpi, 1600/my_dpi), dpi=my_dpi)

    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()

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
    new_counter["year"] = new_counter.year.apply(decadify)
    new_counter = new_counter.groupby(by=["genre","year"]).sum().groupby(by = ['year', 'genre'])['count'].aggregate('first').unstack().reset_index().set_index('year').reindex(["<2000", "2001-2010", "2011-2019"])

    new_counter.plot(y = ['Country', 'Hip-Hop', 'Pop'], kind = 'bar')

    plt.savefig(vis_folder+"/genius_histogram_binned.png")
