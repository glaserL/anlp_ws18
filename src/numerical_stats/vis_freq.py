#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dependencies
import csv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from matplotlib import rc
from matplotlib import rcParams

# set parameters for latex infusion
rcParams['text.latex.preamble'] = [r'\boldmath']
rcParams['axes.titlepad'] = 20
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

# make wordcloud
def makeWordCloud(path):
    with open("../data/freq.csv", "r") as file:
        reader = csv.reader(file)
        ls = list(reader)
    k = [dict(zip(ls[i], [int(el) for el in ls[i+1]])) for i in range(0, len(ls),2)]
    for d in k:
        for key in d.keys():
            if key == "ai":
                d["ain't"] = d.pop(key)
            elif key == "ca":
                d["can't"] = d.pop(key)
            elif key == "wo":
                d["won't"] = d.pop(key)
    title = [r'$T_1$',r'$T_2$',r'$T_3$']
    my_dpi=200
    fig = plt.figure(figsize=(1800/my_dpi, 1600/my_dpi), dpi=my_dpi)
    for i in range(len(k)):
        im = Image.open("../data/img/cloud.png")
        im = im.convert('L')
        im2 = np.asarray(im).copy()
        im2[im2 < 250] = 0
        im2[im2 >= 250] = 255
        w = WordCloud(background_color="white", colormap= "inferno_r", min_font_size = 20, contour_width=1, prefer_horizontal= 0.95, contour_color="white", mask=im2, margin = 1, width = 800, height = 1000)
        w.generate_from_frequencies(k[i])
        ax = fig.add_subplot(3,3,i+1)
        ax.imshow(w)
        if i in [0,1,2]:
            plt.title(title[i], size=17, color="black", y=1.1)
        if i == 0:
            ax.set_ylabel(r'\textbf{Country}', labelpad = 30, fontsize = 10)
        elif i == 3:
            ax.set_ylabel(r'\textbf{Pop}', labelpad = 30, fontsize = 10)
        elif i == 6:
            ax.set_ylabel(r'\textbf{Hip-Hop}',labelpad = 30, fontsize = 10)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
    plt.savefig(path)

# make barplot
def makeBar(path):
    # read and process freq file
    with open("../data/freqRefined.csv", "r") as file:
        reader = csv.reader(file)
        ls = list(reader)
    k = [dict(zip(ls[0], [int(el) for el in ls[i]])) for i in range(1, len(ls[:4]))]
    k.extend([dict(zip(ls[4], [int(el) for el in ls[i]])) for i in range(5, len(ls[:8]))])
    k.extend([dict(zip(ls[8], [int(el) for el in ls[i]])) for i in range(9, len(ls[:12]))])
    for d in k:
        for key in d.keys():
            if key == "ai":
                d["ain't"] = d.pop(key)
            elif key == "ca":
                d["can't"] = d.pop(key)
            elif key == "wo":
                d["won't"] = d.pop(key)
    title = [r'$T_1$',r'$T_2$',r'$T_3$']
    color = ["blue", "orangered", "lightcoral"]
    maxi = []
    maxi.extend([1.1*max([item for el in k[:3] for item in list(el.values())])])
    maxi.extend([1.1*max([item for el in k[3:6] for item in list(el.values())])])
    maxi.extend([1.1*max([item for el in k[6:9] for item in list(el.values())])])
    my_dpi=200
    fig = plt.figure(figsize=(2400/my_dpi, 1600/my_dpi), dpi=my_dpi)
    rcParams['axes.axisbelow'] = True
    for i in range(len(k)):
        ax = fig.add_subplot(3,3,i+1)
        plt.subplots_adjust(wspace=0.3, hspace = 0.3)
        plt.bar([g for g, v in sorted(k[i].items())], [v for g, v in sorted(k[i].items())], color=color[i%len(color)])
        plt.xticks(rotation=90, fontsize = 6)
        ax.set_ylim(0,maxi[int(i/3)])
        plt.grid(True, alpha = 0.2, color = "gray")
        if i in [0,1,2]:
            plt.title(title[i], size=17, color="black", y=1.1)
        if i == 0:
            ax.set_ylabel(r'\textbf{Country}', labelpad = 50, fontsize = 12)
        elif i == 3:
            ax.set_ylabel(r'\textbf{Pop}\\\\[11pt]Frequency', labelpad = 13, fontsize = 12)
        elif i == 6:
            ax.set_ylabel(r'\textbf{Hip-Hop}',labelpad = 40, fontsize = 12)
        elif i == 7:
            ax.set_xlabel(r'Frequent Words',labelpad = 13, fontsize = 12)
    plt.savefig(path)
    
# make barplot
def makeBarExtend(path):
    # read and process freq file
    with open("../data/freqRefined.csv", "r") as file:
        reader = csv.reader(file)
        ls = list(reader)
    k = [dict(zip(ls[0], [int(el) for el in ls[i]])) for i in range(1, len(ls[:4]))]
    k.extend([dict(zip(ls[4], [int(el) for el in ls[i]])) for i in range(5, len(ls[:8]))])
    k.extend([dict(zip(ls[8], [int(el) for el in ls[i]])) for i in range(9, len(ls[:12]))])
    for d in k:
        for key in d.keys():
            if key == "ai":
                d["ain't"] = d.pop(key)
            elif key == "ca":
                d["can't"] = d.pop(key)
            elif key == "wo":
                d["won't"] = d.pop(key)
    title = [r'$T_1$',r'$T_2$',r'$T_3$']
    color = ["blue", "orangered", "lightcoral"]
    maxi = []
    maxi.extend([1.1*max([item for el in k[:3] for item in list(el.values())])])
    maxi.extend([1.1*max([item for el in k[3:6] for item in list(el.values())])])
    maxi.extend([1.1*max([item for el in k[6:9] for item in list(el.values())])])
    my_dpi=200
    fig = plt.figure(figsize=(2400/my_dpi, 1600/my_dpi), dpi=my_dpi)
    rcParams['axes.axisbelow'] = True
    for i in range(len(k)):
        ax = fig.add_subplot(3,3,i+1)
        plt.subplots_adjust(wspace=0.3, hspace = 0.3)
        plt.bar([g for g, v in sorted(k[i].items())], [v for g, v in sorted(k[i].items())], color=color[i%len(color)], zorder=10)
        z = np.polyfit([j for j in range(len(k[i].items()))], [v for g, v in sorted(k[i].items())], 7)
        f = np.poly1d(z)
        y_new = f([j for j in range(len(k[i].items()))])
        plt.plot([g for g, v in sorted(k[i].items())], y_new+(0.15*maxi[int(i/3)]), alpha = 0.5, linestyle = '--', zorder=5)
        plt.xticks(rotation=90, fontsize = 6)
        ax.set_ylim(0,maxi[int(i/3)])
        plt.grid(True, alpha = 0.2, color = "gray")
        if i in [0,1,2]:
            plt.title(title[i], size=17, color="black", y=1.1)
        if i == 0:
            ax.set_ylabel(r'\textbf{Country}', labelpad = 50, fontsize = 12)
        elif i == 3:
            ax.set_ylabel(r'\textbf{Pop}\\\\[11pt]Frequency', labelpad = 13, fontsize = 12)
        elif i == 6:
            ax.set_ylabel(r'\textbf{Hip-Hop}',labelpad = 40, fontsize = 12)
        elif i == 7:
            ax.set_xlabel(r'Frequent Words',labelpad = 13, fontsize = 12)
    plt.savefig(path)