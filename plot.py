#!/usr/bin/python

import numpy as np
import sys
import matplotlib.pyplot as plt

title = "van Hove: critical scale"
filename = "vanHove_scan_critical_lambda_phi"

data = np.loadtxt("phi.rodata", comments="#")

tpri = data[:,4]
lamc = data[:,1]
instability = data[:,0]

string = [  'AF',  'FM' , 'iAF', 'dWave', 'Charge']
col    = [   'r', 'blue',  'g' ,  'c'   ,  'black']

# AF
plt.plot( tpri[instability==0] , lamc[instability==0], 'o' , color=col[0], label=string[0] )
# FM
plt.plot( tpri[instability==1] , lamc[instability==1], 'o' , color=col[1], label=string[1] )
# iAM
plt.plot( tpri[instability==2] , lamc[instability==2], 'o' , color=col[2], label=string[2] )
# dWave
plt.plot( tpri[instability==3] , lamc[instability==3], 'o' , color=col[3], label=string[3] )
# Charge
plt.plot( tpri[instability==4] , lamc[instability==4], 'o' , color=col[4], label=string[4] )

plt.gca().invert_xaxis()
plt.legend(loc=3)
plt.xlabel(r"$t'$", fontsize = 24) 
plt.ylabel(r"$\Lambda_c$", fontsize = 24)  
plt.title(title)
plt.savefig(filename+".eps")
plt.savefig(filename+".pdf")
plt.clf()



title = "van Hove filling + 7%: critical scale"
filename = "vanHove_plus_scan_critical_lambda_phi"

data = np.loadtxt("Phi_info.dat", comments="#")

tpri = data[:,4]
lamc = data[:,1]
instability = data[:,0]

string = [  'AF',  'FM' , 'iAF', 'dWave', 'Charge']
col    = [   'r', 'blue',  'g' ,  'c'   ,  'black']

# AF
plt.plot( tpri[instability==0] , lamc[instability==0], 'o' , color=col[0], label=string[0] )
# FM
plt.plot( tpri[instability==1] , lamc[instability==1], 'o' , color=col[1], label=string[1] )
# iAM
plt.plot( tpri[instability==2] , lamc[instability==2], 'o' , color=col[2], label=string[2] )
# dWave
plt.plot( tpri[instability==3] , lamc[instability==3], 'o' , color=col[3], label=string[3] )
# Charge
plt.plot( tpri[instability==4] , lamc[instability==4], 'o' , color=col[4], label=string[4] )

plt.gca().invert_xaxis()
plt.legend(loc=3)
plt.xlabel(r"$t'$", fontsize = 24) 
plt.ylabel(r"$\Lambda_c$", fontsize = 24)  
plt.title(title)
plt.savefig(filename+".eps")
plt.savefig(filename+".pdf")
plt.clf()
