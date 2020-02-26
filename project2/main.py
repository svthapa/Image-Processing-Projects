#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:24:59 2020

@author: samrajyathapa
"""

import cv2
import matplotlib.pyplot as mp
import numpy as np

#this function returns the histogram of the image.
def getHist(name):
    img=cv2.imread(name, 0)
    hist=cv2.calcHist([img], [0], None, [256], [0,255])
    hist=hist.reshape(256,)
    
    return hist
    

#this function returns the cdf of the image
def calcCDF(pdf):
    sum=0
    list=[]
    for each in pdf:
        sum+=each
        list.append(sum)
    return list

#this function changes the contrats stretches it.
def contrastStretch(cdf, img):
    val=cdf[-1]
    val10=0.1 * val
    val90=0.9 * val
    list10=[]
    list90=[]
    img2=img.copy()
    for each in cdf:
        if (each <= val10):
            list10.append(cdf.index(each))
        
        elif(each >= val90):
            list90.append(cdf.index(each))
    
    list10=sorted(list10)
    list90=sorted(list90)
    
    if (len(list10) == 0 ):
        l1=0
    else:
        l1=list10[-1]
        
    if (len(list90) == 0 ):
        l2=255
    else:
        l2=list90[0]

    
    m=255/l2
    b= -m * l1
    rows, cols = img2.shape
    for x in range(rows):
        for y in range(cols):
           if(img2[x,y] >= l2):
               img2[x,y]=255
               
           elif(img2[x,y] >=0 and img2[x,y] <= l1):
               img2[x,y] = 0
               
           else:
               img2[x,y] = m * img2[x,y] +b
        
    hist=cv2.calcHist([img2], [0], None, [256], [0,255])
    return img2, hist

# this function slices the image from a certain pixel to another
def levelSlicing(img):
    rows, cols = img.shape
    
    L= int(input("enter value of L: "))
    list=[]
    for each in range(L, L+11):
        list.append(each)
    
    for x in range(rows):
        for y in range(cols):
            if(img[x,y] in list):
                img[x,y] = 255
            else:
                img[x,y] = 0
                
    hist=cv2.calcHist([img], [0], None, [256], [0,255])
    return img, hist
 
def histEqualization(hist, img):
    newHist=[]
    sum=0
    rows, cols = img.shape
    newCDF=[]
    for each in hist:
        each=each/(512**2)
        newHist.append(each)
    
    for each1 in newHist:
        sum+=each1
        newCDF.append(sum)
    
    for x in range(rows):
        for y in range(cols):
            index=img[x,y]
            img[x,y]=round(newCDF[index] * 255)
            
    histogram=cv2.calcHist([img], [0], None, [256], [0,255])
    
    return img, histogram
    

    
    
img=cv2.imread('jet.pgm', 0)   

pdf=getHist('jet.pgm') #histogram img

cdf=calcCDF(pdf) #cdf img

contrastImg, contrastHist=contrastStretch(cdf, img) #contrast stretched img

sliceImg, sliceHist=levelSlicing(img) #image slicing

histImg, histogram=histEqualization(pdf, img) #equalized image

cv2.imwrite('test.png', sliceImg)