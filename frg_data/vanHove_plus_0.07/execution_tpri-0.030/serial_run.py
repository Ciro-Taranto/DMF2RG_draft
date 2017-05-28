#!/usr/bin/python

import numpy as np
import sys
import os
import shutil
def loadtxt(filename):
	f     = open(filename)  
	lines = f.readlines()
	gl = [] 
	for l in lines: 
		if len(l)>0 : 
			gl.append(l[:48]) 
	return gl 

casa="/u/tciro/DMFT_DATA/Annealing/"
puntidir = os.walk(casa)
tocommit = [] 
for x in  puntidir:
	last = x[0].split('/')[-1]
	if (len(last) >3) and last[:4] == "beta":  
#		print x[0]
		tocommit.append(x[0][19:])

for x in tocommit: 
	print x,len(x)

giafatti = loadtxt("gialanciati") 

for x in tocommit: 
	if x in giafatti : 
		print "ce l'ho",x 
	else:   
                y = x.split('/')
                print y 
		f = open("submit_dmft_mpi_template.sh","r")
                lines = f.readlines()
                string = "D_DMFT_DIR="+x+"\n"
		lines[8]=string
		lines[7]="D_JOB_NAME="+y[1]+"-"+y[2]+"-"+y[3]+"-"+y[4]+"\n" 
		with open("submit_dmft_mpi_template.sh","w") as filew: 
			filew.writelines(lines)
		with open("uglytrick.txt","w") as fileu: 
			fileu.writelines(x+"\n")
		os.system("cat uglytrick.txt >> gialanciati")
		os.system("./submit_dmft_mpi_template.sh")

    
