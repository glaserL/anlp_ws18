from db import database
import matplotlib.pyplot as plt


def visualize_data():
    """
    Visualizes all genre/data combinations using boxplot
    """
    rows = []
    genres = ["Country", "Pop", "Hip-Hop"]
    features = ["avg_word_length", "ttr", "non_std_words", "egocentrism", "sentiment"]
    db = database.Database()
    conn = db.get_connection()
    cur = conn.cursor()

    for genre in genres:
        for feature in features:
            # fetch songs from database
            s1 = 'SELECT ' + feature + ' FROM songs WHERE (year NOT LIKE "2%" OR year IS "2000") AND genre IS ?;'
            s2 = 'SELECT ' + feature + ' FROM songs WHERE (year LIKE "200%" OR year IS "2010") AND year IS NOT "2000" AND genre IS ?;'
            s3 = 'SELECT ' + feature + ' FROM songs WHERE year LIKE "201%" AND year IS NOT "2010"  AND genre IS ?;'
            cur.execute(s1, (genre,))
            iterator = cur.fetchall()
            s1_vals = [el[0] for el in iterator]
            cur.execute(s2, (genre,))
            iterator = cur.fetchall()
            s2_vals = [el[0] for el in iterator]
            cur.execute(s3, (genre,))
            iterator = cur.fetchall()
            s3_vals = [el[0] for el in iterator]

            # make sure we have equal lengths
            min_len = min(len(s1_vals), len(s2_vals), len(s3_vals))
            s1_vals, s2_vals, s3_vals = equal_len(s1_vals, s2_vals, s3_vals, min_len)
            rows.append([genre, feature, s1_vals, s2_vals, s3_vals])
            # create boxplots
            boxplot(rows)

    conn.close()

    return


def equal_len(s1_vals, s2_vals, s3_vals, min_len):
    """
    Makes sure all groups have the same length

    :param s1_vals: lyrics corresponding to year <= 2000
    :param s2_vals: lyrics corresponding to 2001 <= year <= 2010
    :param s3_vals: lyrics corresponding to year >= 2011
    :param min_len: minimal group size
    :return: equalized groups
    """

    return s1_vals[:min_len], s2_vals[:min_len], s3_vals[:min_len]


def boxplot(rows):
    """
    Creates boxplots for data
    :param rows: contains information about genre, feature and groups
    """
    for i in range(len(rows)):
        data = [rows[i][2], rows[i][3], rows[i][4]]

        title = rows[i][0] + " " + rows[i][1]
        # basic plot
        fig, ax = plt.subplots()
        ax.boxplot(data)
        plt.title(title)

        plt.show()
        graphic_name = rows[i][0] + " " + rows[i][2]+".pdf"
        fig.savefig(graphic_name)

    return
