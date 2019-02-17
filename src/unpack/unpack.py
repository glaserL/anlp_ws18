#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool

def _unpack(do):
    work = [ast.literal_eval(el) for el in do]
    return work

def unpack(packed, nocores = None, chunksize = 5000):
    
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
           statements = list(tqdm(p.imap(_unpack, [packed[i:i+chunksize] for i in range(0, len(packed),chunksize)]), total=len(packed)/chunksize))
        
        statements = [item for sublist in statements for item in sublist]
        return statements