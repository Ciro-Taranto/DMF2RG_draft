#!/usr/bin/python

import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py

tpri = 0.075
title = r"DMF$^2$RG, $t'=$"+str(tpri) 
plotname = "dmf2rgsevsnose"

def plot_data(data, mark,info):
	lam = data[:,0]
	ivector = np.rint(data[:,1])
	incommensurateAF = data[:,2]
	commensurateAF = data[:,3]
	density = data[:,5]
	sc_s = data[:,7]
	sc_d = data[:,8]
	iAF = False 
	FM  = False 
	for i in range(1,np.shape(data)[0]) : 
	    iAF = True if (np.rint(data[i,1]) ==  1) else iAF   
	    FM  = True if (np.rint(data[i,1]) ==  0) or (np.rint(data[i,1]) == -1) else FM 
	
	string = [  'AF ',  'iAF',  'Charge' , 'FM', 'dWave', 'swave']
	for i in range(len(string)):
		string[i] = string[i] + info
	print string
	string2 = [  'AF x 20',  'iAF x 20',  'Charge x 20 ' , 'FM x 20 ', 'dWave x 20', 'swave x 20']
	col    = [   'r',   'r' ,  'Black'  , 'Blue', 'c'   , 'Green']
	
	# AF
	small = False #if np.max(commensurateAF) > 100./40. else True  
	plt.plot(  np.log(lam[:]) , (20. if small else 1.)* commensurateAF, mark , color=col[0], label=string[0] if not small else string2[0]  )
	# density 
	small = False if np.max(density) > 100./40. else True  
	plt.plot(  np.log(lam[:]) , (20. if small else 1.) * density, mark , color=col[2], label=string[2] if not small else string2[2] )
	# FM 
	if FM :
	    plt.plot(  np.log(lam[:]) , incommensurateAF, mark if (np.rint(data[-1][1]) ==0) else mark , color=col[3], label= string[3] if (np.rint(data[-1][1]) ==0) else string[3]  )
	return lam

lmin1 = np.min(plot_data( np.loadtxt(sys.argv[1]), 'o' , "" ) )
lmin2 = np.min(plot_data( np.loadtxt(sys.argv[2]) , '*', "$\Sigma$") ) 

lmin = np.min(lmin1,lmin2)

ticks =[] 
location=[]
i = 0. 
while  i   <= 1. : 
    if  i > lmin : 
        ticks.append(str(i)) 
        location.append(np.log(i) ) 
    i +=0.1
# plt.gca().invert_xaxis()
plt.legend(loc=1)
plt.ylabel(r"$\Phi_{\mathrm{max}}$", fontsize = 24) 
plt.xlabel(r"$(1-\Lambda)$", fontsize = 24)  
# plt.xlim([0.001,1])
plt.xticks(location, ticks) 
plt.ylim([0,300.]) 
plt.title(title)
plt.savefig(str(tpri)+plotname+".eps")
plt.savefig(str(tpri)+plotname+".pdf")
plt.savefig(str(tpri)+plotname+".png")
plt.clf()

