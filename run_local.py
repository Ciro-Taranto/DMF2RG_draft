#!/usr/bin/python

import sys
import subprocess
import os 
import fileinput
import numpy as np 

def run(command): 
    output = subprocess.check_output(command, shell = True) 
    return output 
def myreplaceall(filename, searchExpr, replaceExpr): 
    for line in fileinput.input(filename, inplace = 1):
        if searchExpr in line: 
            line = line.replace(searchExpr,replaceExpr)
        sys.stdout.write(line)

def read_vsmu():
	dat = np.loadtxt('vsmu',comments='c')
	return dat[0], dat[1], dat[2], dat[3] # in order: beta, U, mu, densi

def write_vsmu(uhub,beta,tpri,nocc):
    f = open("vsmu") 
    lines = f.readlines() 
    dat = np.loadtxt('vsmu',comments='c')
    dat[0] = beta 
    dat[1] = uhub
    dat[3] = nocc 
    dat[-1]= tpri 
    string = ' ' 
    for i in range( len (dat)): 
        string = string+ "%.4f"%dat[i]+"   "
    string = string + "\n"
    lines[1] = string 
    with open("vsmu","w") as filew:
        filew.writelines(lines)
def myreplaceall(lineold, uhub, beta, tpri, nocc, thr):
    search = ['UUU','BBB','TTT','NNN','THR']
    put    = ['%.4f'%uhub,'%.4f'%beta,'%.4f'%tpri,'%.4f'%nocc,'%.4f'%thr]
    linenew = lineold
    for i in range(len(search)):
        if search[i] in linenew: 
            linenew = linenew.replace(search[i],put[i])
    return linenew
def fRG(uhub,beta,trpi,nocc,thr): 
    runString = myreplaceall(templateString,uhub,beta,tpri,nocc,thr) 
    run(runString) 
    dat = np.loadtxt("susc_beta.txt", comments ='c')
    if abs(dat[1]-beta) > 0.01 : 
        print "the beta input does not coincide with the beta output" 
        sys.exit() 
    chi = dat[2]
    for i in range(3,len(dat)): 
        if abs(dat[i]) > thr : 
            print "instability detected in SC or DEN channel. Check susc_beta.txt" 
            sys.exit()
    foldername = "funRG_U%.2f"%uhub+"beta%.2f"%beta+"n%.2f"%nocc+"tpri_minus_%.3f"%(abs(tpri))
    if not os.path.exists(foldername):
        run ("mkdir -p  "+foldername)
    run ("cp *h5 "+foldername) 
    return chi 
def newbeta(beta): 
    f = open("vsmu")
    lines= f.readlines()
    dat = np.loadtxt('vsmu', comments = 'c' )
    dat[0] =beta 
    string = ' '
    for i in range( len (dat)): 
        string = string+ "%.4f"%dat[i]+"   "
    string = string + "\n"
    lines[1] = string 
    with open("vsmu","w") as filew:
        filew.writelines(lines)
def newuhub(u):
    f = open("vsmu") 
    lines = f.readlines() 
    dat = np.loadtxt('vsmu',comments='c')
    dat[1] = u
    string = ' ' 
    for i in range( len (dat)): 
        string = string+ "%.4f"%dat[i]+"   "
    string = string + "\n"
    lines[1] = string 
    with open("vsmu","w") as filew:
        filew.writelines(lines)
 
templateString= "./x86_64_dmf2rg --frg --U UUU --beta BBB --tp TTT  --starting-filling NNN --no-self-energy-flow  --keep-last-step-only --threshold THR"
#################DEFAULT PARAMETERS##################################################
alpha = 2.0 
gamma = 0.1
uhub =  1.0 
beta = 10.0 
tpri = -0.04
nocc =  0.87
thr  =100.00
#################READING INPUT FROM COMMAND LINE#####################################
if len(sys.argv) != 5 :
    print "wrong number of arguments in run.py. Required",5,"given",len(sys.argv)-1
    sys.exit()
else:
    try: 
        uhub = float(sys.argv[1])
    except ValueError: 
        print "Taking default value uhub= ",uhub
    try:
        tpri  = float(sys.argv[2])
    except ValueError  : 
        print "Taking default tpri = ",tpri 
    try:
        nocc  = float(sys.argv[3])
    except ValueError  : 
        print "Taking default nocc = ",nocc 
    try:
        thr  = float(sys.argv[4])
    except ValueError  : 
        print "Taking default thr = ",thr
#####################################################################################
################FINDING THE NEEL TEMPERATURE FROM MAG LADDER#########################
#####################################################################################
verbose = True 
gamma=10./thr
gammaLadder = 0.01
beta = 10 
write_vsmu(uhub,beta,tpri,nocc)
run("./ladder >> output_ladder")
chiold1 = np.loadtxt('susc_beta.txt', comments = 'c')[3]
while chiold1 < 0.0: 
    print "Initial guess of beta too high"
    beta = beta/2.
    write_vsmu(uhub,beta,tpri,nocc)
    run("./ladder >> output_ladder") 
    chiold1 = np.loadtxt('susc_beta.txt',comments = 'c')[3]
beta2 = alpha*beta 
write_vsmu(uhub,beta2,tpri,nocc) 
run ("./ladder >> output_ladder")
chiold2=np.loadtxt("susc_beta.txt",comments = 'c')[3]
while chiold2 > 0.0: 
    print "Initial guess of beta too high"
    beta2 = alpha*beta2
    write_vsmu(uhub,beta2,tpri,nocc)
    run("./ladder >> output_ladder") 
    chiold2 = np.loadtxt('susc_beta.txt',comments = 'c')[3]
itera   = 0 
small   = 0.01 
big     = 1E4 
betaold = 1E4
while abs(betaold-beta2) > small and itera <= 50 and abs (betaold- beta) > small and chiold1 < big :
    betaI = beta+(beta2-beta)*(1./(1.+gammaLadder*chiold1))
    write_vsmu(uhub,betaI,tpri,nocc)
    run("./ladder >> output ")
    chioldI = np.loadtxt('susc_beta.txt',comments = 'c')[3] 
    if chioldI > 0 :
        betaold=beta
        beta = betaI
        chiold1 = chioldI 
    else  : 
        betaold=beta2
        beta2= betaI 
        chiold2 = chioldI
    itera = itera+1
    if verbose : 
        print itera 
        print "while: beta1,beta2=","%.2f"%beta,"%.2f"%beta2,"chiold1, chiold2 =","%.2f"%chiold1,"%.2f"%chiold2 
   
print "RPA beta=",betaI 

beta = betaI
chi1 = fRG(uhub,beta,tpri,nocc,thr)  
while abs(chi1) > thr : 
    print 'initial guess of beta (fRG)  too large' 
    print 'reset beta to',beta/alpha
    beta = beta/alpha
    chi1 = fRG(uhub,beta,tpri,nocc,thr) 
beta2 = alpha*beta 
chi2 = fRG (uhub,beta2,tpri,nocc,thr)
while abs(chi2) < thr : 
    print 'initial guess of beta2 (fRG) too small' 
    print 'reset beta2 to',beta2*alpha
    beta2 = alpha*beta2 
    chi2  = fRG (uhub,beta2,tpri,nocc,thr)

itera = 0 
small = 0.01 
big   = thr-1.

while abs(betaold-beta2) > small  and itera <= 50 and abs(betaold-beta)> small and abs(chi1)<big  :
    print "ITERA=",itera
    print "while: beta1,beta2=","%.2f"%beta,"%.2f"%beta2,"chiold1, chiold2 =","%.2f"%chi1,"%.2f"%chi2 
    reitera = 0
    betaI=beta+(beta2-beta)*(1/(1.+gamma*chi1))
    chiI = fRG (uhub,betaI,tpri,nocc,thr)  
    if abs(chioldI) < thr :
        # if abs(betaI-beta) < small:
            # itera = 2000
        betaold=beta
        beta = betaI
        chiold1 = chioldI 
    else  : 
        # if abs(beta2-beta) < small:
            # itera = 2000
        betaold=beta2
        beta2= betaI 
        chiold2 = chioldI
    itera = itera + 1

if itera == 50 : 
    print 'not converged after ',50,' iterations of the bracketing method'
else : 
    print 'The final beta = ', betaI




