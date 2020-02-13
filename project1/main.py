#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:00:52 2020

@author: samrajyathapa
"""
import cv2
import matplotlib.pyplot as mp
import numpy as np
import math

def changeResolution(name,value):
    image=cv2.imread(name,0)
    rows, cols = image.shape[:2]
    if(value==0):
        #mp.imshow(image)
        val1=input('Do you want to change bits/pixel of image ?:(y/n):\n').lower()
        if(val1=='y'):
            intensityVal=int(input('Enter bits/pixel to change to: \n'))
            intensity=2**intensityVal
            intensity1=int(256/intensity)
            print(intensity1)
            output=reduceBits(image,rows,cols,intensity1)
            #mp.imshow(output)
            cv2.imwrite('output6Bits.png', output)
            
    else:
        output=rescale(image, rows, cols, value)
    
        #mp.imshow(output)
        #cv2.imwrite('output64.png', output)
        
        val1=input('Do you want to change bits/pixel of image ?:(y/n):\n').lower()
        if(val1=='y'):
            intensityVal=int(input('Enter bits/pixel to change to: \n'))
            intensity= 2**intensityVal
            intensity1=int(256/intensity)
            output1=reduceBits(image,rows,cols,intensity1)
            cv2.imwrite('output4Bits.png', output1)
        
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
    print(intensityMapping(value))
    iDict=intensityMapping(value)
    for x in range(0, rows):
        for y in range(0, cols):
            image[x,y]=math.floor(image[x,y]/value)
            #if(image[x,y] in iDict.keys()):
                #image[x,y]=iDict[image[x,y]][0]
            #else:
                #continue
    return image


def intensityMapping(step):
    intensityMap=dict()
    #value=2**intensity
    #step=int(256/value)
    #value=int(value)
    count=0
    try:
        for i in range(0, 255, step):
            for j in range(i,i+step):
                try:
                    intensityMap[count].append(j)
                except KeyError:
                    intensityMap[count]=[j]
            count+=step
    except ValueError:
        print('error')
        
    return intensityMap
    
    
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

