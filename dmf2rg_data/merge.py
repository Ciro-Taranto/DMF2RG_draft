#!/usr/bin/python
import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py 
from PIL import Image 

outputname = "dmf2rglam" 
tpri =0.075
if len (sys.argv) < 3 : 
    print "not enough arguments" 

plotstomerge = [ Image.open(os.getcwd()+"/"+sys.argv[1])  ,Image.open(os.getcwd()+"/"+ sys.argv[2]) ]
x,y = plotstomerge[0].size 
result = Image.new("RGB", (2*x, y))
for i in range(len(plotstomerge)): 
    img = plotstomerge[i] 
    xnow = i % 2 * x 
    ynow = 0 
    w,h = img.size
    print('pos {0},{1} size {2},{3}'.format(xnow, ynow, 2*x, 2*y))
    result.paste(img, (xnow, ynow, xnow + w, ynow + h))

result.save(outputname+".png") 
