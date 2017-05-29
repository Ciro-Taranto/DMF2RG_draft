#!/usr/bin/python

import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import interpolate
import matplotlib
from dmftData import *
import patch 

plotMag = False
plotDen = True
plotSWave = False
plotDWave = False

iw_list = range(10)

controluce=False

# Dmf2rg data
dmf2rg = dmf2rgData( sys.argv[1] , vertex1Mom3Freq=True)

p = patch.patchScheme()
p.fixPatchFromH5File(sys.argv[1])
p.setTriangularReduced()

p_chi = patch.patchScheme()
p_chi.fixPatchFromH5File(sys.argv[1],"/DMF2RG/Susceptibilities/k_grid")
p_chi.setTriangularReduced()

U = dmf2rg.get_parameter("/Parameters/U")
beta = dmf2rg.get_parameter("/Parameters/beta")
lam = dmf2rg.get_parameter("/Parameters/L")

def plotCh( Phi_func, k, om , real):
	ik = p.getPatchIndex( k[0], k[1] )
	nfer = 17
	fer_grid = np.array(range(-nfer,nfer+1))
	print fer_grid[-1], fer_grid[-1]
	if controluce:
		arr = np.array( [[-(Phi_func(ik,om,nu,nup).real if real else Phi_func(ik,om,nu,nup).imag) for nu in fer_grid] for nup in fer_grid] )
	else:
		arr = np.array( [[(Phi_func(ik,om,nu,nup).real if real else Phi_func(ik,om,nu,nup).imag) for nu in fer_grid] for nup in fer_grid] )
	plt.pcolor( fer_grid, fer_grid, arr )
	plt.xlim(fer_grid[0],fer_grid[-1])
	plt.ylim(fer_grid[0],fer_grid[-1])
	#plt.clim(-3000,3000)
	plt.colorbar()

def plotMom( Phi_func, om, nu, nup ):
	kx = np.arange( 0, np.pi+0.02, 0.02 )
	ky = kx.copy()
	plt.pcolor( kx, ky, np.array( [[ Phi_func ( p.getPatchIndex(x,y).real, om,nu,nup).real for x in kx] for y in ky] ) )
	plt.xlim(0,np.pi)
	plt.ylim(0,np.pi)
	plt.colorbar()

def plotChi( Chi_func, om ):
	kx = np.arange( 0, np.pi+0.02, 0.02 )
	ky = kx.copy()
	plt.pcolor( kx, ky, np.array( [[ Chi_func ( p_chi.getPatchIndex(x,y).real, om) for x in kx] for y in ky] ) )
	plt.xlim(0,np.pi)
	plt.ylim(0,np.pi)
	plt.colorbar()


#def t1to4(l, sh):
#	i0 = l % sh[0]
#	i1 = (l % ( sh[0] * sh[1] )) / sh[0] - (sh[1]-1)/2
#	i2 = (l % ( sh[0] * sh[1]* sh[2] )) / ( sh[0] * sh[1] ) - (sh[2]-1)/2
#	i3 = l / ( sh[0] * sh[1] * sh[2] ) - (sh[3]-1)/2 
#	return i0,i1,i2,i3
#
#print "Shape of Den: ", dmf2rg.Phi_den.shape
#print "Max of Den: ", np.max( dmf2rg.Phi_den ), " at ", t1to4(np.argmax(dmf2rg.Phi_den),dmf2rg.Phi_den.shape)
#print "Min of Den: ", np.min( dmf2rg.Phi_den ), " at ", t1to4(np.argmin(dmf2rg.Phi_den),dmf2rg.Phi_den.shape)
#idx = t1to4(np.argmin(dmf2rg.Phi_den),dmf2rg.Phi_den.shape) 

#matplotlib.rcParams.update({'font.size': 20})
##plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# Mag
if plotMag:
	for iw in iw_list:
		plotCh( dmf2rg.Phi_mag_xphnot , [np.pi,np.pi], iw , False)
		plt.savefig('Mag_Im_'+str(iw)+'_dmf2rg_pp.png')
		plt.clf()
		plotCh( dmf2rg.Phi_mag_xphnot , [np.pi,np.pi], iw , True)
		plt.savefig('Mag_Re_'+str(iw)+'_dmf2rg_pp.png')
		plt.clf()
		plotCh( dmf2rg.Phi_mag_xphnot , [0.,0.], iw , False)
		plt.savefig('Mag_Im_'+str(iw)+'_dmf2rg_00.png')
		plt.clf()
		plotCh( dmf2rg.Phi_mag_xphnot , [0.,0.], iw , True)
		plt.savefig('Mag_Re_'+str(iw)+'_dmf2rg_00.png')
		plt.clf()
	#plotMom( dmf2rg.Phi_mag_xphnot, 0, 15 , 15 )
	#plt.savefig('Mag_BZ.png')
	#plt.clf()
	plotChi( lambda q,om: dmf2rg.Chi_mag_(q,om).real, 0 )
	plt.savefig('Chi_mag_Re.png')
	plt.clf()
	plotChi( lambda q,om: dmf2rg.Chi_mag_(q,om).imag, 0 )
	plt.savefig('Chi_mag_Im.png')
	plt.clf()

# Den
if plotDen:
	for iw in iw_list:
		plotCh( dmf2rg.Phi_den_phnot , [np.pi,np.pi], iw , True)
		plt.savefig('Den_Re_'+str(iw)+'_pp.png')
		plt.clf()
		plotCh( dmf2rg.Phi_den_phnot , [0.,0.], iw , True)
		plt.savefig('Den_Re_'+str(iw)+'_00.png')
		plt.clf()
		plotCh( dmf2rg.Phi_den_phnot , [np.pi,np.pi], iw , False)
		plt.savefig('Den_Im_'+str(iw)+'_pp.png')
		plt.clf()
		plotCh( dmf2rg.Phi_den_phnot , [0.,0.], iw , False)
		plt.savefig('Den_Im_'+str(iw)+'_00.png')
		plt.clf()
	#plotMom( dmf2rg.Phi_den_phnot, iw, 0, 0 )
	#plt.savefig('Den_Re_BZ.png')
	#plt.clf()
	plotChi( lambda q,om: dmf2rg.Chi_den_(q,om).real, 0 )
	plt.savefig('Chi_den_Re.png')
	plt.clf()
	plotChi( lambda q,om: dmf2rg.Chi_den_(q,om).imag, 0 )
	plt.savefig('Chi_den_Im.png')
	plt.clf()

# S-wave
#plotCh( dmf2rg.Phi_scs_ppnot , [0.,0.], 1 ,False)
#plt.savefig('SCS1_im_00.png')
#plt.clf()
#plotCh( dmf2rg.Phi_scs_ppnot , [np.pi,np.pi], 1 ,False)
#plt.savefig('SCS1_im_pp.png')
#plt.clf()
#plotCh( dmf2rg.Phi_scs_ppnot , [0.,0.], 0 ,False)
#plt.savefig('SCS0_im_00.png')
#plt.clf()
#plotCh( dmf2rg.Phi_scs_ppnot , [np.pi,np.pi], 0 ,False)
#plt.savefig('SCS0_im_pp.png')
#plt.clf()

if plotSWave:
	for iw in iw_list:
		plotCh( dmf2rg.Phi_scs_ppnot , [0.,0.], iw , True)
		plt.savefig('SCS_Re_'+str(iw)+'_00.png')
		plt.clf()
		plotCh( dmf2rg.Phi_scs_ppnot , [np.pi,np.pi], iw , True)
		plt.savefig('SCS_Re_'+str(iw)+'_pp.png')
		plt.clf()
		plotCh( dmf2rg.Phi_scs_ppnot , [0.,0.], iw , False)
		plt.savefig('SCS_Im_'+str(iw)+'_00.png')
		plt.clf()
		plotCh( dmf2rg.Phi_scs_ppnot , [np.pi,np.pi], iw , False)
		plt.savefig('SCS_Im_'+str(iw)+'_pp.png')
		plt.clf()

# d-wave
if plotDWave:
	plotCh( dmf2rg.Phi_scd_ppnot , [0.,0.], 0 , True)
	plt.savefig('SCD_Re_00.png')
	plt.clf()
	plotCh( dmf2rg.Phi_scd_ppnot , [0.,0.], 0 , False)
	plt.savefig('SCD_Im_00.png')
	plt.clf()
	plotCh( dmf2rg.Phi_scd_ppnot_singlet , [0.,0.], 0 , True)
	plt.savefig('SCD_s_Re_00.png')
	plt.clf()
	plotCh( dmf2rg.Phi_scd_ppnot_triplet , [0.,0.], 0 , True)
	plt.savefig('SCD_t_Re_00.png')
	plt.clf()
	plotChi( lambda q, om: dmf2rg.Chi_dwave_s_(q,om).real, 0 )
	plt.savefig('Chi_dwave_s_Re.png')
	plt.clf()

#
# Plot magnetic in BZ
#plotMom( dmf2rg.Phi_mag_xphnot, 0, 0, 0 )
#plt.savefig('Mag_BZ.png')
#plt.clf()
