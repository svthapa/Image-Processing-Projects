#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:59:59 2020

@author: samrajyathapa
"""


import cv2
import numpy as np
import matplotlib.pyplot as mp



def highFilter(name, cutoff):
    img=cv2.imread(name, 0)
    img1=np.fft.fft2(img)
    img_shift=np.fft.fftshift(img1)
    rows, cols= img.shape
    rows, cols=int(rows/2), int(cols/2)
    
    img_shift[rows-cutoff:rows+cutoff, cols-cutoff:cols+cutoff]=0 #high pass
       
    f_ishift=np.fft.ifftshift(img_shift)
    img_back=np.fft.ifft2(f_ishift)
    img_back=np.abs(img_back)
    
    return img_back.astype('uint8')
    
def lowFilter(name, cutoff):
    img=cv2.imread(name, 0)
    img1=np.fft.fft2(img)
    img_shift=np.fft.fftshift(img1)
    rows, cols= img.shape
    crows, ccols=int(rows/2), int(cols/2)
   
    mask = np.zeros((rows,cols),np.uint8)
    mask[crows-cutoff:crows+cutoff, ccols-cutoff:ccols+cutoff] = 1    
    img_shift= img_shift*mask
    
    f_ishift=np.fft.ifftshift(img_shift)
    img_back=np.fft.ifft2(f_ishift)
    img_back=np.abs(img_back)
    
    #mp.imshow(img_back, 'gray')
    return img_back.astype('uint8')
    

def getHist(name):
    #img=cv2.imread(name, 0)
    hist=cv2.calcHist([name], [0], None, [256], [0,255])
    hist=hist.reshape(256,)
    
    return hist


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
            index=int(img[x,y])
            img[x,y]=round(newCDF[index] * 255)
            
    histogram=cv2.calcHist([img], [0], None, [256], [0,255])
    
    return img, histogram 

def morph(img, openIt, closeIt):
    kernel = np.ones((3, 3), np.uint8) 
    _,threshImg = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    openingImg = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, kernel, iterations=openIt)
    closingImg = cv2.morphologyEx(openingImg, cv2.MORPH_CLOSE, kernel, iterations=closeIt)
    
    return openingImg, closingImg

def erode(img, it, x, y):
    kernel = np.ones((x,y),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = it)
    
    return erosion

def dilation(img, it):
    kernel = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(img,kernel,iterations = it)
    return dilation

def median(img, level, times):
    for i in range(0, times):
        img = cv2.medianBlur(img, level)
    return img

#functions for different images
def image03(): #horizontal defect
    low_image=lowFilter('0003.jpg', 250)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    opening, closing = morph(histImg, 1, 1)
    erodeImg = erode(closing, 2, 1, 30)
    mp.imshow(erodeImg, 'gray')

def image076(): #horizontal defect
    low_image=lowFilter('0076.jpg', 60)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    opening, closing = morph(histImg, 1, 1)
    erodeImg = erode(closing, 1, 1, 30)
    mp.imshow(erodeImg, 'gray')
    
def image0192(): # high frequency change defect
    high_image = highFilter('0192.jpg', 10)
    pdf = getHist(high_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, high_image)
    
    mp.imshow(histImg, 'gray')
    opening, closing = morph(histImg, 1, 1)
    mp.imshow(closing, 'gray')
    erodeImg = erode(closing, 17, 1, 1)
    mp.imshow(erodeImg, 'gray')



def image0158(): #horizontal defect
    low_image=lowFilter('0158.jpg', 30)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    opening, closing = morph(histImg, 1, 1)
    erodeImg = erode(closing, 1, 1, 20)
    mp.imshow(erodeImg, 'gray')

def image0106(): #low frequency change defect 
    low_image=lowFilter('0106.jpg', 250)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    opening, closing = morph(histImg, 1, 1)
    erodeImg = erode(closing, 3, 3, 3)
    mp.imshow(erodeImg, 'gray')
 
def image012(): #blob defect in the middle
    low_image=lowFilter('0012.jpg', 250)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    opening, closing = morph(histImg, 1, 1)
    erodeImg = erode(closing, 3, 3, 3)
    #mp.imshow(erodeImg, 'gray')
    dilateImg = dilation(erodeImg, 2)
    mp.imshow(dilateImg, 'gray')

def image020(): #line defect in the middle
    high_image = lowFilter('0020.jpg', 500)
    pdf = getHist(high_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, high_image)
    mp.imshow(histImg, 'gray')
    
    opening, closing = morph(histImg, 2, 1)
    erodeImg = erode(closing, 1, 3, 3)
    mp.imshow(erodeImg, 'gray')
    median = cv2.medianBlur(erodeImg, 5)
    mp.imshow(median, 'gray')

    
def image041(): #scattered holes defect
    low_image=lowFilter('0041.jpg', 250)
    pdf = getHist(low_image) #histogram of image after lowpass filter
    histImg, hist = histEqualization(pdf, low_image)
    
    histImg= 255-histImg #inverting pixel values
    #mp.imshow(histImg, 'gray')
    opening, closing = morph(histImg, 2, 1)
    mp.imshow(closing, 'gray')
    erodeImg = erode(closing, 1, 3 ,3)
    #mp.imshow(erodeImg, 'gray')


    
def main():
    image0192()
    
if __name__=='__main__':
    main()