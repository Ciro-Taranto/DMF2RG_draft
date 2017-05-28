#!/usr/bin/python

import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py 
from PIL import Image 

filelist = []
loadedimages = [] 
filename = "rawdata_function_lam.dat.png" 
print os.getcwd() 
for d in  next(os.walk('.'))[1]: 
    print d.split("-")
    filelist.append(os.getcwd()+"/"+d+"/"+str(float(d.split("-")[1]))+filename)
for f in filelist : 
    print os.path.isfile(f)
    print f
    try: 
        loadedimages.append(  Image.open(f) )  
    except: 
        print "unable to load image"
x,y = loadedimages[0].size 
result = Image.new("RGB", (2*x, 2*y))
for i in range(len(loadedimages)): 
    img = loadedimages[i] 
    # img.thumbnail((400, 400), Image.ANTIALIAS)
    xnow = i // 2 * x 
    ynow = i %  2 * y 
    w,h = img.size
    print('pos {0},{1} size {2},{3}'.format(xnow, ynow, 2*x, 2*y))
    result.paste(img, (xnow, ynow, xnow + w, ynow + h))

result.save("all.png") 
