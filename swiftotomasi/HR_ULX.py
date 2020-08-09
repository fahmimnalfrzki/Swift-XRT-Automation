#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 06:49:19 2019

@author: fahmi
"""

import os,glob
import pandas as pd
import numpy as np
import astropy.io.fits as fits

file=open('obj.txt','r')
txt=file.readlines()
obj=[]
fol='/home/s20319002/test/'
for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        obj.append(txt[i].split('\t')[0][1:-1])

for i in range(len(obj)):
    os.chdir(fol+obj[i]+'/')
    obsid=glob.glob('00*')
    soft=[[],[]]
    hard=[[],[]]
    semua=[[],[]]
    MJD=[]
    for j in range(len(obsid)):
        os.chdir(obsid[j]+'/xrt/event/')
        with open ('XSPEC','w') as fout:
            fout.write('query yes\n')
            fout.write('data '+obsid[j]+'_pc_grp.pha\n')
            fout.write('ign 0.0-0.3,1.5-**\n')
            fout.write('show all\n')
            fout.write('notice all\n')
            fout.write('ign 0.0-1.5,10.0-**\n')
            fout.write('show all\n')
            fout.write('notice all\n')
            fout.write('ign 0.0-0.3,10.0-**\n')
            fout.write('show all\n')
        os.system('xspec < XSPEC > '+obsid[j]+'_xspec.log')
        
        hdul=fits.open(obsid[j]+'_pc_grp.pha')
        MJD.append(hdul[0].header['MJD-OBS'])
        hdul.close()
        
        file=open(obsid[j]+'_xspec.log','r')
        dat=file.readlines()
        for k in range(len(dat)):
            if dat[k]=='XSPEC12>ign 0.0-0.3,1.5-**\n':
                break
        for l in range(k,len(dat)):
            if dat[l]=='XSPEC12>show all\n':
                break
        soft[0].append(float(dat[l+44].split()[6]))
        soft[1].append(float(dat[l+44].split()[8]))
        
        for k in range(len(dat)):
            if dat[k]=='XSPEC12>ign 0.0-1.5,10.0-**\n':
                break
        for l in range(k,len(dat)):
            if dat[l]=='XSPEC12>show all\n':
                break
        hard[0].append(float(dat[l+44].split()[6]))
        hard[1].append(float(dat[l+44].split()[8]))
        
        for k in range(len(dat)):
            if dat[k]=='XSPEC12>ign 0.0-0.3,10.0-**\n':
                break
        for l in range(k,len(dat)):
            if dat[l]=='XSPEC12>show all\n':
                break
        semua[0].append(float(dat[l+44].split()[6]))
        semua[1].append(float(dat[l+44].split()[8]))
        os.chdir(fol+obj[i]+'/')
    
    x=(1/np.array(soft[0]))**2
    ex=np.array(hard[1])**2
    y=(-np.array(hard[0])/(np.array(soft[0])**2))**2
    ey=np.array(soft[1])**2    
    errHR=np.sqrt(x*ex+y*ey)

    HR=pd.DataFrame()
    HR['MJD']=MJD
    HR['HR']=np.array(hard[0])/np.array(soft[0])
    HR['err_HR']=errHR
    HR['cts']=semua[0]
    HR['err_cts']=semua[1]
    HR.to_csv(obj[i]+'_HR.csv')
