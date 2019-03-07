#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import and set dependencies
import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from matplotlib import rc
from matplotlib import rcParams

# set parameters for latex infusion
rcParams['text.latex.preamble'] = [r'\boldmath']
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
"AWL": df1.iloc[a,2:].values.tolist()+df1.iloc[a+5,2:].values.tolist()+df1.iloc[a+10,2:].values.tolist(),
"TTR": df1.iloc[b,2:].values.tolist()+df1.iloc[b+5,2:].values.tolist()+df1.iloc[b+10,2:].values.tolist(),
"NSW": df1.iloc[c,2:].values.tolist()+df1.iloc[c+5,2:].values.tolist()+df1.iloc[c+10,2:].values.tolist(),
"EGO": df1.iloc[d,2:].values.tolist()+df1.iloc[d+5,2:].values.tolist()+df1.iloc[d+10,2:].values.tolist(),
"SEN": df1.iloc[e,2:].values.tolist()+df1.iloc[e+5,2:].values.tolist()+[el*-1 for el in df1.iloc[e+10,2:].values.tolist()]
})

# modified from https://python-graph-gallery.com/392-use-faceting-for-radar-chart/
def make_spider(ind, title, color):
    plt.subplots_adjust(wspace=9, hspace = 16)
    categories=list(df)
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    ax = plt.subplot(3,3,ind+1, polar=True)
    if ind == 0:
        ax.set_ylabel(r'\textbf{Country}', labelpad = 40, fontsize = 12)
    elif ind == 3:
        ax.set_ylabel(r'\textbf{Pop}', labelpad = 40, fontsize = 12)
    elif ind == 6:
        ax.set_ylabel(r'\textbf{Hip-Hop}',labelpad = 40, fontsize = 12)
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
        plt.title(title, size=14, color="black", y=1.1)
    plt.tight_layout()
    
# run pipeline
def run(path):
    my_dpi=180
    plt.figure(figsize=(1800/my_dpi, 1600/my_dpi), dpi=my_dpi)
    colour = ["blue", "orangered", "lightcoral"]
    group = [r'$T_1$ $[\leq 2000]$',r'$T_2$ $[2001-2010]$',r'$T_3$ $[2011-2019]$']
    for ind in range(0, len(df.index)):
        make_spider(ind=ind, title=group[ind%len(group)], color=colour[ind%len(colour)])
    plt.savefig(path)