#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 21:10:20 2019

@author: fahmi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:07:38 2019

@author: fahmi
"""

import pandas as pd
import matplotlib.pyplot as pl
import os,glob
import numpy as np




obj=[]
file=open('obj.txt','r')
txt=file.readlines()

for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        obj.append(txt[i].split('\t')[0][1:-1])

for z in range(len(obj)):
    flux=[[],[],[],[]]
    obsid=[]
    cr=[[],[]]
    fol='/home/fahmi/Documents/data/'+obj[z]+'/Swift'
    os.chdir(fol)
    obs_id=glob.glob('00*')
    for i in range(len(obs_id)):
        os.chdir(fol+'/'+str(obs_id[i])+'/xrt/event/')
        if len(glob.glob('*wt_diskbbpo.xcm'))>0 and len(glob.glob(str(obs_id[i])+'wthard_xcm.log'))==0:
            with open ('XSPEC','w') as fout:
                fout.write('setplot energy\n')
                fout.write('query yes\n')
                fout.write('@0'+glob.glob('*_diskbbpo.xcm')[0][1:]+'\n')
                fout.write('ign 0.0-0.3,10.-**\n')
                fout.write('fit\n')
                fout.write('show all\n')
                fout.write('new 1 0\n')
                fout.write('flux 0.3 1.5\n')
                fout.write('flux 1.5 10\n')
            os.system('xspec < XSPEC > '+ str(obs_id[i])+'wthard_xcm.log')
            
        if len(glob.glob(str(obs_id[i])+'wthard_xcm.log'))>0:
            log=open(str(obs_id[i])+'wthard_xcm.log','r')
            dat=log.readlines()
            obsid.append(str(obs_id[i]))
            for l in range(len(dat)):
                if dat[l]=='XSPEC12>show all\n':
                    break
            for k in range(len(dat)):
                if dat[k]=='XSPEC12>flux 0.3 1.5\n':
                    break
            flux[0].append(float(dat[k+1].split()[4][1:]))
            if float(dat[l+45].split()[6])>0:
                flux[2].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
            else:
                flux[2].append(0)
                
            for k in range(len(dat)):
                if dat[k]=='XSPEC12>flux 1.5 10\n':
                    break
            flux[1].append(float(dat[k+1].split()[4][1:]))
            if float(dat[l+45].split()[6])>0:
                flux[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
            else:
                flux[3].append(0)
        if len(glob.glob('*pc_diskbbpo.xcm'))>0 and len(glob.glob(str(obs_id[i])+'pchard_xcm.log'))==0:
            with open ('XSPEC','w') as fout:
                fout.write('setplot energy\n')
                fout.write('query yes\n')
                fout.write('@0'+glob.glob('*_diskbbpo.xcm')[0][1:]+'\n')
                fout.write('ign 0.0-0.3,10.-**\n')
                fout.write('fit\n')
                fout.write('show all\n')
                fout.write('new 1 0\n')
                fout.write('flux 0.3 1.5\n')
                fout.write('flux 1.5 10\n')
            os.system('xspec < XSPEC > '+ str(obs_id[i])+'pchard_xcm.log')
            
        if len(glob.glob(str(obs_id[i])+'pchard_xcm.log'))>0:
            log=open(str(obs_id[i])+'pchard_xcm.log','r')
            dat=log.readlines()
            obsid.append(str(obs_id[i]))
            for l in range(len(dat)):
                if dat[l]=='XSPEC12>show all\n':
                    break
            for k in range(len(dat)):
                if dat[k]=='XSPEC12>flux 0.3 1.5\n':
                    break
            flux[0].append(float(dat[k+1].split()[4][1:]))
            if float(dat[l+45].split()[6])>0:
                flux[2].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
            else:
                flux[2].append(0)
                
            for k in range(len(dat)):
                if dat[k]=='XSPEC12>flux 1.5 10\n':
                    break
            flux[1].append(float(dat[k+1].split()[4][1:]))
            if float(dat[l+45].split()[6])>0:
                flux[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
            else:
                flux[3].append(0)
                    
                
         
    hardness=np.array(flux[1])/np.array(flux[0])
    errhardness=np.sqrt((1/np.array(flux[0]))**2 *np.array(flux[2])**2 +(np.array(flux[1])/np.array(flux[0])**2)**2 *np.array(flux[3])**2)
    
    result=pd.DataFrame({'obsid':obsid,
                         'Flux 0.3-1.5':flux[0],'err0.3-1.5':flux[2],
                         'Flux 1.5-10':flux[1],'err1.5-10':flux[3],
                         'Soft':hardness,'err Soft':errhardness})
    
    
    result.to_excel('~/Documents/'+obj[z]+' hardness.xlsx')