#!/usr/bin/python

import numpy as np
import sys
import os
import shutil
import matplotlib.pyplot as plt
import h5py

def readh5andWrite(filename, data,  onlyRe, check):
    casa ="./data/"
    try: 
        f = h5py.File(casa+filename,"r")   
        Phi_mag_Re = f["DMF2RG/Vertex/Phi_magnetic_Re"] 
        Phi_mag_Im = f["DMF2RG/Vertex/Phi_magnetic_Im"]
        Phi_mag  = np.sqrt(Phi_mag_Re[:,:,:,:]**2 +((Phi_mag_Im [:,:,:,:]**2) if not onlyRe  else  0.)  ) 
        argmag =  np.unravel_index(np.argmax(Phi_mag), np.shape(Phi_mag)   )
        Phi_den_Re = f["DMF2RG/Vertex/Phi_density_Re"] 
        Phi_den_Im = f["DMF2RG/Vertex/Phi_density_Im"]
        Phi_den  = np.sqrt(Phi_den_Re[:,:,:,:]**2 + ((Phi_den_Im [:,:,:,:]**2 ) if not onlyRe else 0. )  )
        argden =  np.unravel_index(np.argmax(Phi_den), np.shape(Phi_den)   )
        Phi_sc_s_Re = f["DMF2RG/Vertex/Phi_sc_s_Re"] 
        Phi_sc_s_Im = f["DMF2RG/Vertex/Phi_sc_s_Im"]
        Phi_sc_s  =np.sqrt( Phi_sc_s_Re[:,:,:,:]**2 + ( (Phi_sc_s_Im [:,:,:,:]**2 ) if not onlyRe else 0.))
        argsc_s =  np.unravel_index(np.argmax(Phi_mag), np.shape(Phi_mag))
        if (check and argsc_s[0] != 0 ) : 
            print "what is going on?" 
            print "argsc_s=",argsc_s
            print  Phi_sc_s_Re[argsc_s], Phi_sc_s_Im[argsc_s] 
            print  Phi_sc_s_Re[0,argsc_s[1],argsc_s[2],argsc_s[3]], Phi_sc_s_Im[0,argsc_s[1],argsc_s[2],argsc_s[3]] 
        Phi_sc_d_Re = f["DMF2RG/Vertex/Phi_sc_d_Re"] 
        Phi_sc_d_Im = f["DMF2RG/Vertex/Phi_sc_d_Im"]
        Phi_sc_d  =np.sqrt( Phi_sc_d_Re[:,:,:,:]**2 + ( (Phi_sc_d_Im [:,:,:,:]**2 ) if not onlyRe else 0.) ) 
        argsc_d =  np.unravel_index(np.argmax(Phi_sc_d), np.shape(Phi_sc_d)   )
        if argsc_d[0] != 0 : 
            print "what is going on?" 
            print "argsc_d=",argsc_d 
        data.append([f["Parameters/L"][0], argmag[0], Phi_mag[argmag],argden[0], Phi_den[argden], argsc_s[0], Phi_sc_s[argsc_s], argsc_d[0], Phi_sc_d[argsc_d], Phi_mag[16,argmag[1],argmag[2],argmag[3] ] ]   )
    except:
        print "Not able to read file:", filename






casa="./data/"


tpri =0.075
# tpri = float( os.getcwd().split('-')[1])

rawfilename = "rawdata_function_lam.dat"
if not os.path.isfile(rawfilename) :
    datafiles = os.listdir(casa)
    data = []  
    onlyRe = True 
    check = False
    for filename in datafiles:
        print "Reading file:", filename
        readh5andWrite(filename, data,  onlyRe, check)
    print "all files have been read" 
    lam = np.array([ data[i][0] for i in range(len(data))] )
    orderdata=[]
    string = "# lam \t iQmag_max \t phi_mag_max \t phi_mag_pipi \t iQden_max \t Phi_den_max \t iQscs_max \t Phi_sc_s_max \t Phi_sc_d_max \n "  
    for i in range(len(lam)): 
        orderdata.append(data[np.argsort(lam)[-i-1]])
    text_file =open("rawdata_function_lam.dat","a")  
    for i in range(len(orderdata)): 
        indeces = [0, 1, 2, 9, 3,  4, 5,  6, 8 ] 
        for j in range(len(indeces))  : 
            string += "{:10.4f}".format(float(orderdata[i][indeces[j]])) + "\t"
        string += "\n"
    text_file.write(string)
    text_file.close() 

#### Finished imput files, starting the plotting ##### 

title = r"DMF$^2$RG: $\Phi_{\mathrm{max}}$, $t'=$"+str(tpri)+" ,with $\Sigma$" 
plotname = "vanHove_scan_critical_lambda_phi"

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

string = [  r'AF',  r'iAF',  r'Charge' , r'FM', r'dWave', r'swave']
for i in range(len(string)) :
    string[i] = string[i]+" with  $\Sigma$" 
string2 = [  r'AF x 20',  r'iAF x 20',  r'Charge x 20 ' , r'FM x 20 ', r'dWave x 20', r'swave x 20']
for i in range(len(string)) :
    string2[i] = string2[i]+" with  $\Sigma$" 
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
plt.legend(loc=1)
plt.ylabel(r"$\Phi_{\mathrm{max}}$", fontsize = 24) 
plt.xlabel(r"$(1-\Lambda)$", fontsize = 24)  
# plt.xlim([0.001,1])
plt.xticks(location, ticks) 
plt.ylim([0,300.]) 
plt.title(title)
plt.savefig(str(tpri)+rawfilename+".eps")
plt.savefig(str(tpri)+rawfilename+".pdf")
plt.savefig(str(tpri)+rawfilename+".png")
plt.clf()

