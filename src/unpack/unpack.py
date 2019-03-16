#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import multiprocessing
from tqdm import tqdm
from multiprocessing import Pool

def _unpack(do):
    work = ast.literal_eval(do)
    return work

def unpack(packed, nocores = None, chunksize = 200):
    if nocores == 1 or multiprocessing.cpu_count() == 1:
        res = []
        iterator = tqdm(packed)    
        for el in iterator:
            res.append(ast.literal_eval(el))    
        return res
    else:
        if nocores == None:
            nocores =  multiprocessing.cpu_count()-1    
        with Pool(nocores) as p:
           statements = list(tqdm(p.imap(_unpack,packed,chunksize), total=len(packed)))
        return statements
