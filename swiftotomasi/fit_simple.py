#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 20:48:53 2019

@author: fahmi
"""
import os,glob,shutil,sys,time
import numpy as np
import matplotlib.pyplot as pl

nH=[]
file=open('obj.txt','r')
txt=file.readlines()
fol=[]
objek=[]

tin=[]
kt=[]
p=[]
tau=[]
flux=[[],[],[],[],[],[]]
cr=[[],[]]
rcs=[]


ti=time.time()
for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        fol.append(txt[i].split('\t')[0][1:-1])
        objek.append(txt[i].split('\t')[1])
        nH.append(float(txt[i].split('\t')[-1][:-1]))
    if txt[i][0]=='/':
        folder=txt[i][:-1]

for i in range(len(fol)):
    os.chdir(folder+fol[i]+'/Swift/')
    obs_id=glob.glob('00*')

    for j in range(len(obs_id)):
        os.chdir(obs_id[j]+'/xrt/event/')
        if len(glob.glob('*wt_diskpbbcomptt_1.xcm'))==0 and len(glob.glob('*wt_grp.pha'))>0:
            print(obs_id[j],'is begin to fit.')
            with open('XSPEC','w') as fout:
                fout.write('query yes\n')
                fout.write('setplot energy\n')
                fout.write('data '+obs_id[j]+'_wt_grp.pha\n')
                fout.write('ign 0.0-0.3,10.0-**\n')
                fout.write('mo tbabs*diskpbb\n')
                fout.write('\n')
                fout.write('1.\n')
                fout.write('0.75 \n')
                fout.write('1.\n')
                fout.write('fit\n')
                fout.write('steppar 2 0.5 10. 50\n')
                fout.write('editmo tbabs*(diskpbb+compTT)\n')
                fout.write('\n')
                fout.write('=p2\n')
                fout.write('\n')
                fout.write('\n')
                fout.write('\n')
                fout.write('\n')
                fout.write('fit\n')
                fout.write('steppar 2 0.5 1. 50\n')
                fout.write('steppar 7 30 200 100\n')
                fout.write('steppar 8 0 200 100\n')
                fout.write('show all\n')
                fout.write('flux 0.6 2.5\n')
                fout.write('flux 2.5 4.5\n')
                fout.write('flux 4.5 10.0\n')
                fout.write('save all '+obs_id[j]+'_wt_diskpbbcomptt_1.xcm')
            os.system('xspec < XSPEC > '+ obs_id[j]+'_xspec_diskpbbcomptt_1.log')
            print('Fitting done.')
        else:
            print(obs_id[j],'has been fitted.')
#        if len(glob.glob('*wt.xcm'))>0 and len(glob.glob('*wt_grp.pha'))>0:
#            log=open(obs_id[j]+'_xspec.log','r')
#            data=log.readlines()
#            for l in range(len(data)):
#                if data[l]=='XSPEC12>show all\n':
#                    break
#            cr[0].append(float(data[l+45].split()[6]))
#            cr[1].append(float(data[l+45].split()[8]))
#            rcs.append(float(data[l+91].split()[3]))
#            for k in range(len(data)):
#                if data[k]=='XSPEC12>flux 0.6 2.5\n':
#                    break
#            flux[0].append(float(data[k+1].split()[4][1:]))
#            for k in range(len(data)):
#                if data[k]=='XSPEC12>flux 2.5 4.5\n':
#                    break
#            flux[1].append(float(data[k+1].split()[4][1:]))
#            
#            for k in range(len(data)):
#                if data[k]=='XSPEC12>flux 4.5 10.0\n':
#                    break
#            flux[2].append(float(data[k+1].split()[4][1:]))
        os.chdir(folder+fol[i]+'/Swift/')

#soft=np.array(flux[1])/np.array(flux[0])
#hard=np.array(flux[2])/np.array(flux[1])
#
#fig=pl.figure(0)
#f=fig.add_subplot(111)
#f.scatter(soft,hard)
#f.set_xlim(0,5)
#f.set_ylim(0,5)
        
        
        