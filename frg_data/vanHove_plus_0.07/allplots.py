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
if not os.path.isfile('./loglam.py') : 
    print "Missing the file that produces the subplots, look for loglam.py" 
    sys.exit() 
if (len(sys.argv)) > 1 : 
    outputname = sys.argv[1]
for d in next(os.walk(origin))[1]: 
    shutil.copy('loglam.py',d) 
    os.chdir(origin+'/'+d)
    os.system("./loglam.py")
    os.chdir(origin)

filelist = []
loadedimages = [] 
filename = "rawdata_function_lam.dat.png" 
here = os.getcwd() 
dire  = next(os.walk(here))[1]
tlist = np.array ( [ float( dire[i].split("-")[1] ) for i in range(len(dire)) ] )  
for i in range(len(dire)): 
    d = dire[np.argsort(tlist)[i]] 
    print "considering trpi = ",  d.split("-")
    filelist.append(os.getcwd()+"/"+d+"/"+str(float(d.split("-")[1]))+filename)
for f in filelist : 
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

result.save(outputname+".png") 
