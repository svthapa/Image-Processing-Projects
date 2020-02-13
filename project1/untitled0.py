#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:00:52 2020

@author: samrajyathapa
"""
import cv2
import matplotlib.pyplot as mp
import numpy as np

def changeResolution(name,value):
    image=cv2.imread(name,0)
    rows, cols = image.shape[:2]
    if(value==0):
        mp.imshow(image)
        val1=input('Do you want to change bits/pixel of image ?:(y/n):\n').lower()
        if(val1=='y'):
            intensityVal=int(input('Enter bits/pixel to change to: \n'))
            intensity= 2**intensityVal
            reduceBits(image,rows,cols,intensity)
    else:
        output=rescale(image, rows, cols, value)
    
        mp.imshow(output)
        
        val1=input('Do you want to change bits/pixel of image ?:(y/n):\n').lower()
        if(val1=='y'):
            intensityVal=int(input('Enter bits/pixel to change to: \n'))
            intensity= 2**intensityVal
            reduceBits(image,rows,cols,intensity)
    

    #cv2.imwrite('test.png', value)

def rescale(img, rows, cols, step):
    
    for x in range(0, rows-step, step):
    
        for y in range(0, cols-step, step):
            
            sum=0
            avg=0
            for i in range(0,step):
                for j in range(0, step):
                    sum= sum + img[x+i,y+j]
            avg=sum/(step ** 2)
            avg = np.round(avg)
            for i in range(0,step):
                for j in range(0, step):
                    img[x+i,y+j]=avg
            
            '''
            avg=(img[x, y]+img[x,y+1]+ img[x+1,y]+img[x+1, y+1])/4
            img[x, y]=avg
            img[x+1, y]=avg
            img[x,y+1]=avg
            img[x+1, y+1]=avg
            '''
    return img

def reduceBits(image, rows, cols, value):
    
    for x in range(0, rows):
        for y in range(0, cols):
            if(image[x,y]>value):
                image[x,y]=value
            else:
                continue
    return image
    
def main():
    
    val=input('Which image do you want to change resolution of ?:\n')  
    if(val=='1'):
        name='fish.pgm'
    elif(val=='2'):
        name='jet.pgm'
    else:
        name='modern.pgm'
    
    while(True):
        val1=input('what resolution do you want to change it to ?(leave original/256/128/64):\n')
        if  (val1=='256'):
            res=2
            break
        elif(val1=='128'):
            res=4
            break
        elif(val1=='64'):
            res=8
            break
        elif(val1=='leave original'):
            res=0
            break
        else:
            print('wrong input')
    
    changeResolution(name,res)

if __name__=='__main__':
    main()

