#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:24:59 2020

@author: samrajyathapa
"""

def hello(step):
    intensityMap=dict()
    count=0
    for i in range(0, 255, step):
        for j in range(i,i+step):
            try:
                intensityMap[count].append(j)
            except KeyError:
                intensityMap[count]=[j]
        count+=step

    print(intensityMap)
    
hello(16)