#!/usr/bin/python
import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py


tpri = float( 0.075)

title = r"Channel maximum, $t'=$"+str(tpri)
plotname = "dmf2rg_sevsnose"

def(rawfilename, mark, se):
    data = np.loadtxt(rawfilename, comments="#")
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
        iAF = True if (np.rint(data[i,1]) != 16  and np.rint(data[i,1]) != 0 ) else iAF   
        FM  = True if (np.rint(data[i,1]) ==  0) else FM 
    
    string = [  'AF',  'iAF',  'Charge' , 'FM', 'dWave', 'swave']
    string2 = [  'AF x 20',  'iAF x 20',  'Charge x 20 ' , 'FM x 20 ', 'dWave x 20', 'swave x 20']
    col    = [   'r',   'r' ,  'Black'  , 'Blue', 'c'   , 'Green']
    
    # AF
    small = False if np.max(commensurateAF) > 100./40. else True  
    plt.plot(  np.log(lam[:]) , (20. if small else 1.)* commensurateAF, 'o' , color=col[0], label=string[0] if not small else string2[0]  )
    # plt.plot(  (np.log(1.-lam[:])) , commensurateAF, 'o' , color=col[0], label=string[0] )
    # iAF
    if iAF: 
        plt.plot(  np.log(lam[:]) , incommensurateAF, 'v' , color=col[1], label=string[1] )
        # plt.plot(  np.log(lam[ivector != 0 and ivector != 16 ]) , incommensurateAF[ivector!=0 and ivector != 16], 'v' , color=col[1], label=string[1] )
        # plt.plot(  (lam[ivector != 0 and ivector != 16 ]) , incommensurateAF[ivector!=0 and ivector != 16], 'v' , color=col[1], label=string[1] )
    # density 
    small = False if np.max(density) > 100./40. else True  
    plt.plot(  np.log(lam[:]) , (20. if small else 1.) * density, 'o' , color=col[2], label=string[2] if not small else string2[2] )
    # FM 
    if FM :
        plt.plot(  np.log(lam[:]) , incommensurateAF, 'o' , color=col[3], label=string[3] )
        # plt.plot(  np.log(lam[ivector == 0 ]) , incommensurateAF[ivector == 0 ], 'o' , color=col[3], label=string[3] )
    # swave 
    small = False if np.max(sc_s) > 100./40. else True  
    plt.plot(  np.log(lam[:]) , (20. if small else 1. )*  sc_s, 'o' , color=col[5], label=string[5] if not small else string2[5]  )
    # dwave 
    small = False if np.max(sc_d) > 100./40. else True  
    plt.plot(  np.log(lam[:]) , (20. if small else 1. )*  sc_d, 'o' , color=col[4], label=string[4] if not small else string2[4] )

lmin = np.min(lam)
ticks =[] 
location=[]
i = 0. 
while  i   <= 1. : 
    if  i > lmin : 
        ticks.append(str(i)) 
        location.append(np.log(i) ) 
    i +=0.1
# plt.gca().invert_xaxis()
plt.legend(loc=4)
plt.ylabel(r"$\Phi_{\mathrm{max}}$", fontsize = 24) 
plt.xlabel(r"$(1-\Lambda)$", fontsize = 24)  
# plt.xlim([0.001,1])
plt.xticks(location, ticks) 
plt.ylim([0,100.]) 
plt.title(title)
plt.savefig(str(tpri)+rawfilename+".eps")
plt.savefig(str(tpri)+rawfilename+".pdf")
plt.savefig(str(tpri)+rawfilename+".png")
plt.clf()

