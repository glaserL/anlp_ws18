#########################################
# visualize boxplots
#########################################

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

#########################################
# visualize spider plot
#########################################

# import and set dependencies
import os
import pandas as pd
from math import pi
from matplotlib import rc
from matplotlib import rcParams

# set parameters for latex infusion
plt.rcParams['text.latex.preamble'] = [r'\boldmath']
rcParams['axes.titlepad'] = 20
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

# read in statistical csv and re-project
path = os.path.join(os.path.dirname(os.path.abspath("__file__")), "../data/results.csv")
dfB = pd.read_csv(path)
dfMax = dfB[["Feature", "mean s1", "mean s2", "mean s3"]]
maxi = [max(dfMax.loc[dfMax["Feature"] == el].iloc[:,1:4].values.flatten().tolist())*1.1 for el in list(dfMax["Feature"].unique())]
df1 = dfB[["Genre","Feature", "mean s1", "mean s2", "mean s3"]]
for i in range(0,len(df1.index)):
    df1.iloc[i,2:5] = (df1.iloc[i,2:5]/maxi[i%len(maxi)])*100
a,b,c,d,e = (0,1,2,3,4)
df = pd.DataFrame({
"TTR": df1.iloc[a,2:].values.tolist()+df1.iloc[a+5,2:].values.tolist()+df1.iloc[a+10,2:].values.tolist(),
"AWL": df1.iloc[b,2:].values.tolist()+df1.iloc[b+5,2:].values.tolist()+df1.iloc[b+10,2:].values.tolist(),
"EGO": df1.iloc[c,2:].values.tolist()+df1.iloc[c+5,2:].values.tolist()+df1.iloc[c+10,2:].values.tolist(),
"NSW": df1.iloc[d,2:].values.tolist()+df1.iloc[d+5,2:].values.tolist()+df1.iloc[d+10,2:].values.tolist(),
"SEN": df1.iloc[e,2:].values.tolist()+df1.iloc[e+5,2:].values.tolist()+[el*-1 for el in df1.iloc[e+10,2:].values.tolist()]
})

# modified from https://python-graph-gallery.com/392-use-faceting-for-radar-chart/
def make_spider(ind, title, color):
    plt.subplots_adjust(wspace=25, hspace = 25)
    categories=list(df)
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    ax = plt.subplot(3,3,ind+1, polar=True)
    if ind == 0:
        ax.set_ylabel(r'Country', labelpad = 30, fontsize = 12)
    elif ind == 3:
        ax.set_ylabel(r'Pop', labelpad = 30, fontsize = 12)
    elif ind == 6:
        ax.set_ylabel(r'Hip-Hop',labelpad = 30, fontsize = 12)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories, color='dimgray', size=8)
    ax.set_rlabel_position(45)
    plt.yticks(list(range(0,101,20)), color="dimgray", size=7)
    plt.ylim(0,100)
    values=df.loc[ind].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)    
    if ind in [6,7,8]:
         plt.xticks(angles[:-1], ['AWL', 'EGO', 'NSW', r'SEN$^\dagger$', 'TTR'], color='dimgray', size=8)
    if ind in [0,1,2]:
        plt.title(title, size=17, color="black", y=1.1)
    plt.tight_layout()
    
# run pipeline
def run(path):
    my_dpi=180
    plt.figure(figsize=(1800/my_dpi, 2000/my_dpi), dpi=my_dpi)
    colour = ["blue", "orangered", "lightcoral"]
    group = [r'$T_1$',r'$T_2$',r'$T_3$']
    for ind in range(0, len(df.index)):
        make_spider(ind=ind, title=group[ind%len(group)], color=colour[ind%len(colour)])
    plt.savefig(path)