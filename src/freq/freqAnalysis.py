#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports and definitions
import os
import nltk
import csv
import re
import random
import multiprocessing
import numpy as np
from PIL import Image
from nltk.corpus import stopwords
from multiprocessing import Pool
from wordcloud import WordCloud
from collections import Counter

class freqAnalyzer(object):
    
    def __init__(self, absPathToken, absPathClean = None):
        
        if isinstance(absPathToken, list):
            self.filesToken = absPathToken
        elif isinstance(absPathToken, str):
            self.filesToken = [absPathToken]
            
        if absPathClean == None:
            self.filesClean = []
        elif isinstance(absPathClean, list):
            self.filesClean = absPathClean
        elif isinstance(absPathClean, str):
            self.filesClean = [absPathClean]
        
    def _tokenize(ls):
            # tokenize lyrics given
            work = [nltk.word_tokenize(lyrics) for lyrics in ls]
            return work
        
    def _cleanProcess(self, ls):
        
        # check alphabetic, remove stop-words and lemmatize
        res = [word.lower() for songs in ls for word in songs if word.lower().isalpha() and word.lower() not in stopwords.words('english')] 
        return res
        
    def cleanLyrics(self, ceiling = 50000, chunksize = 10):

        # loop over all files which have tokens and need to be cleaned
        for file in self.filesToken:
        
            # open and read token file
            with open(file, 'r') as f:
                reader = csv.reader(f)
                ls = list(reader)
            
            # take random sample of ceiling if its size exceed ceciling
            if len(ls) > ceiling:
                ls = random.sample(ls, 50000)
            
            # assign one less than maximum cores and clean lyrics in parallel
            pool = Pool(multiprocessing.cpu_count()-1)
            ls = pool.map(self._cleanProcess, [ls[i:i+chunksize] for i in range(0, len(ls),chunksize)])
            pool.close()
            pool.join()
            
            # flatten resulting chunked list
            ls = [word for item in ls for word in item]
            
            # search for basename to assign to clean file
            name = re.sub("Token.csv", "", os.path.basename(file))
            
            path = os.path.dirname(os.getcwd()) + "/data/clean/" + name + "Clean.csv"
            self.filesClean.append(path)
            
            # write list to clear memory
            with open(path, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows([ls])
                
            # clear memory
            del ls
            
        return 0
    
    @classmethod
    
    def tokenizeLyrics(cls, input_list, grpNames, chunksize = 10):
        
        # in case single string is supplied, change to list of string
        if isinstance(input_list,str):
            input_list = [input_list]
        
        if all(isinstance(el, list) for el in input_list) and len(input_list) == len(grpNames):

            # initilize counter and list for path storage
            i = 0            
            filesToken = []
            
            for g in input_list:
                
                # create list of list of tokens per genre
                # assign one less than maximum cores and clean lyrics in parallel
                pool = Pool(multiprocessing.cpu_count()-1)
                res = pool.map(cls._tokenize, [g[j:j+chunksize] for j in range(0, len(g),chunksize)])
                pool.close()
                pool.join()
                        
                res = [ls for grp in res for ls in grp]
                path = os.path.dirname(os.getcwd()) + "/data/token/" + grpNames[i] + "Token.csv"
                
                # write out all files to save memory
                with open(path, "w") as output:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerows(res)
                
                # add to class variable and increment counter
                filesToken.extend([path])
                i += 1
            
            return cls(filesToken)
        else:
            raise ValueError("input_list must be a list of lists, and input_list and grpNames must have the same length")
        
class freqVisual(object):
    
    def __init__(self, absPathClean):
    
        if isinstance(absPathClean, list):
            self.filesClean = absPathClean
        else:
            self.filesClean = [absPathClean]
        
    def uniqueWords(self, limit = 100, findUnique = True):
        
        # create unique words by comparing to other options
        words = []
        z = []
    
        for file in self.filesClean:
            # read all files   
            with open(file, 'r') as f:
                reader = csv.reader(f)
                ls = list(reader)
            
            # implement counters and find most common
            words.append(Counter(ls[0]).most_common())
            
        if findUnique == False or len(words) == 1:
            
            # return top results based on limit
            words =  [dict(c[1:limit]) for c in words]
            self.words = words
            return(words)
            
        else:
            # find unique words in each genre
            for i in range(len(words)):
                wh = set(dict(words[i][1:limit]).keys())
                for j in range(len(words)):
                    if i != j:
                        wh = wh-set(dict(words[j][1:limit]).keys())
                        
                z.append({w:dict(words[i][1:limit])[w] for w in wh})
                
            return z
     
    @staticmethod    
    
    def makeCloud(dictionary, name, maskPath = None, width = 800, height = 400):

        # check for mask path and push hard into black and white
        if maskPath != None:
            im = Image.open(maskPath)
            im = im.convert('L')
            im2 = np.asarray(im).copy()
            im2[im2 < 250] = 0
            im2[im2 >= 250] = 255
        
        if maskPath == None:
            im2 = None
            
        # genenrate wordcloud and save to file
        w = WordCloud(background_color="white", colormap= "inferno_r", min_font_size = 20, contour_width=1, prefer_horizontal= 0.95, contour_color="white", mask=im2, margin = 1, width = width, height = height)
        w.generate_from_frequencies(dictionary)
        w.to_file(os.path.dirname(os.getcwd()) + "/data/img/" + name + ".png")
        
        return 0