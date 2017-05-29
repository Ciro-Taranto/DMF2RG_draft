#!/usr/bin/python
import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py 
from PIL import Image 

outputname = "merged" 
origin = os.getcwd() 
dire = next(os.walk(origin))[1] 
plotstomerge = []
tpri =0.075
rawfilename = "rawdata_function_lam.dat"
for d in next(os.walk(origin))[1]:
    f=d+'/'+str(tpri)+rawfilename+".png"
    if not os.path.isfile(f): 
        print "non c'e' il file", f 
        sys.exit() 
    try : 
        plotstomerge.append(Image.open(f)) 
    except: 
        print "Something went wrong while reading" 
x,y = plotstomerge[0].size 
result = Image.new("RGB", (2*x, y))
for i in range(len(plotstomerge)): 
    img = plotstomerge[i] 
    # img.thumbnail((400, 400), Image.ANTIALIAS)
    xnow = i % 2 * x 
    ynow = 0 
    w,h = img.size
    print('pos {0},{1} size {2},{3}'.format(xnow, ynow, 2*x, 2*y))
    result.paste(img, (xnow, ynow, xnow + w, ynow + h))

result.save(outputname+".png") 
