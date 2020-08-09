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
from astropy.io import fits

obj=[]
file=open('obj.txt','r')
txt=file.readlines()

for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        obj.append(txt[i].split('\t')[0][1:-1])

for z in range(len(obj)):
    fol='/home/fahmi/Documents/data/'+obj[z]+'/Swift/pileup/'
    fake=pd.read_csv('/home/fahmi/Documents/data/'+obj[z]+'/fakeit_swift.tsv',delimiter=' ')
    
    os.chdir(fol)
    obs_id=glob.glob('00*')
    
    tin=[[],[],[]]
    NH=[[],[],[]]
    normtin=[[],[],[]]
    gam=[[],[],[]]
    flux=[[],[],[],[],[],[]]
    fluxbb=[]
    lumr=[]
    cr=[[],[]]
    rcs=[]
    obsid=[]
    mode=[]
    fluxall=[]
    date=[]
    hardness=[[],[],[],[],[]]
    
    for i in range(len(obs_id)):
        os.chdir(fol+str(obs_id[i])+'/xrt/event/')
        if len(glob.glob('*wt_diskbbpo.xcm'))>0 and len(glob.glob('*wt_xcm_xcm.log'))==0:
            print(str(i)+'/'+str(len(obs_id)),'-',obs_id[i],'wt mode is being proceed')
            with open ('XSPEC','w') as fout:
                fout.write('setplot energy\n')
                fout.write('query yes\n')
                fout.write('@'+str(obs_id[i])+'_wt_diskbbpo.xcm\n')
                fout.write('ign 0.0-0.3,10.-**\n')
                fout.write('fit\n')
                #fout.write('thaw 1\n')
                #fout.write('fit\n')
                #fout.write('steppar 1 1. 3. 20\n')
                #fout.write('steppar 2 0.1 1.3 20\n')
                #fout.write('steppar 4 0.5 3 20\n')
                fout.write('err 1\n')
                fout.write('err 2\n')
                fout.write('err 3\n')
                fout.write('err 4\n')
                fout.write('show all\n')
                fout.write('setplot command cpd '+obs_id[i]+'_wt.gif/gif\n')
                fout.write('plot ld de\n')
                fout.write('new 1 0\n')
                fout.write('flux 0.6 2.5\n')
                fout.write('flux 2.5 4.5\n')
                fout.write('flux 4.5 10.0\n')
                fout.write('flux 0.3 1.5\n')
                fout.write('flux 1.5 10.0\n')
                fout.write('flux 0.3 10.0\n')
                fout.write('new 5 0\n')
                fout.write('flux 0.3 10.0\n')
                fout.write('save all '+obs_id[i]+'_wt_xcm.xcm\n')
            os.system('xspec < XSPEC > '+ str(obs_id[i])+'_wt_xcm_xcm.log')
            
        if len(glob.glob(str(obs_id[i])+'_wt_xcm_xcm.log'))>0:
            hdul=fits.open(glob.glob(str(obs_id[i])+'*grp.pha')[0])
            date.append(hdul[0].header['DATE-OBS'])
            hdul.close()
            mode.append('WT')
            log=open(str(obs_id[i])+'_wt_xcm_xcm.log','r')
            dat=log.readlines()
            obsid.append(str(obs_id[i]))
            for l in range(len(dat)):
                if dat[l]=='XSPEC12>show all\n':
                    break
            try:
                cr[0].append(float(dat[l+45].split()[6]))
            except:
                cr[0].append(0)
            try:
                cr[1].append(float(dat[l+45].split()[8]))
            except:
                cr[1].append(0)
            try:
                NH[0].append(float(dat[l+67].split()[5]))
            except:
                NH[0].append(0)
            try:
                tin[0].append(float(dat[l+68].split()[5]))
            except:
                tin[0].append(0)
            try:
                normtin[0].append(float(dat[l+69].split()[4]))
            except:
                normtin[0].append(0)
            try:
                gam[0].append(float(dat[l+70].split()[4]))
            except:
                gam[0].append(0)
            try:
                for x in range(l,len(dat)):
                    if dat[x].split('=')[0]==' Reduced chi-squared ':
                        break
                rcs.append(float(dat[x].split()[3]))
            except:
                rcs.append(0)
            try:
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.6 2.5\n':
                        break
                flux[0].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    flux[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[3].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 2.5 4.5\n':
                        break
                flux[1].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    flux[4].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[4].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 4.5 10.0\n':
                        break
                flux[2].append(float(dat[k+1].split()[4][1:]))
                
                if float(dat[l+45].split()[6])>0:
                    flux[5].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[5].append(0)
                pass
            
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.3 1.5\n':
                        break
                hardness[0].append(float(dat[k+1].split()[4][1:]))
                hardness[4].append(obs_id[i])
                if float(dat[l+45].split()[6])>0:
                    hardness[2].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    hardness[2].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 1.5 10.0\n':
                        break
                hardness[1].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    hardness[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    hardness[3].append(0)
            
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.3 10.0\n':
                        break
                lumr.append(4*np.pi*float(dat[k+1].split()[4][1:]))
                fluxall.append(float(dat[k+1].split()[4][1:]))
                
                for m in range(len(dat)):
                    if dat[m]=='XSPEC12>new 5 0\n':
                        break
                for n in range(m,len(dat)):
                    if dat[n]=='XSPEC12>flux 0.3 10.0\n':
                        break
                fluxbb.append(float(dat[n+1].split()[4][1:]))
        #            if float(dat[l+45].split()[6])>0:
        #                flux[5].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
        #            else:
        #                flux[5].append(0)
        #            pass
            except:
                flux[0].append(0)
                flux[1].append(0)
                flux[2].append(0)
                flux[3].append(0)
                flux[4].append(0)
                flux[5].append(0)
                lumr.append(0)
                fluxall.append(0)
                fluxbb.append(0)
           
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 1\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='2':
                        break
                if x>0:
                    NH[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    NH[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    NH[1].append(0)
                    NH[2].append(0)
            except:
                NH[1].append(0)
                NH[2].append(0)
            
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 2\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='2':
                        break
                if x>0:
                    tin[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    tin[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    tin[1].append(0)
                    tin[2].append(0)
            except:
                tin[1].append(0)
                tin[2].append(0)
            
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 3\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='3':
                        break
                if x>0:
                    normtin[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    normtin[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    normtin[1].append(0)
                    normtin[2].append(0)
            except:
                normtin[1].append(0)
                normtin[2].append(0)
            
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 4\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='4':
                        break
                if x>0:
                    gam[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    gam[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    gam[1].append(0)
                    gam[2].append(0)
            except:
                gam[1].append(0)
                gam[2].append(0)
            print(obs_id[i],'wt mode is done')
            
        if len(glob.glob('*pc_diskbbpo.xcm'))>0 and len(glob.glob('*pc_xcm_xcm.log'))==0:
            print(str(i)+'/'+str(len(obs_id)),'-',obs_id[i],'pc mode is being proceed')
            with open ('XSPEC','w') as fout:
                fout.write('setplot energy\n')
                fout.write('query yes\n')
                fout.write('@'+str(obs_id[i])+'_pc_diskbbpo.xcm\n')
                fout.write('ign 0.0-0.3,10.-**\n')
                #fout.write('new 1 1.\n')
                fout.write('fit\n')
                #fout.write('steppar 1 1. 3. 20\n')
                #fout.write('steppar 2 0.1 1.3 20\n')
                #fout.write('steppar 4 0.5 3 20\n')
                fout.write('err 1\n')
                fout.write('err 2\n')
                fout.write('err 3\n')
                fout.write('err 4\n')
                fout.write('show all\n')
                fout.write('setplot command cpd '+obs_id[i]+'_pc.gif/gif\n')
                fout.write('plot ld de\n')
                fout.write('new 1 0\n')
                fout.write('flux 0.6 2.5\n')
                fout.write('flux 2.5 4.5\n')
                fout.write('flux 4.5 10.0\n')
                fout.write('flux 0.3 1.5\n')
                fout.write('flux 1.5 10.0\n')
                fout.write('flux 0.3 10.0\n')
                fout.write('new 5 0\n')
                fout.write('flux 0.3 10.0\n')
                fout.write('save all '+obs_id[i]+'_pc_xcm.xcm\n')
            os.system('xspec < XSPEC > '+ str(obs_id[i])+'_pc_xcm_xcm.log')
            
        if len(glob.glob(str(obs_id[i])+'_pc_xcm_xcm.log'))>0:
            hdul=fits.open(glob.glob(str(obs_id[i])+'*grp.pha')[0])
            date.append(hdul[0].header['DATE-OBS'])
            hdul.close()
            mode.append('PC')
            log=open(str(obs_id[i])+'_pc_xcm_xcm.log','r')
            dat=log.readlines()
            obsid.append(str(obs_id[i]))
            for l in range(len(dat)):
                if dat[l]=='XSPEC12>show all\n':
                    break
            for l in range(len(dat)):
                if dat[l]=='XSPEC12>show all\n':
                    break
            try:
                cr[0].append(float(dat[l+45].split()[6]))
            except:
                cr[0].append(0)
            try:
                cr[1].append(float(dat[l+45].split()[8]))
            except:
                cr[1].append(0)
            try:
                NH[0].append(float(dat[l+67].split()[5]))
            except:
                NH[0].append(0)
            try:
                tin[0].append(float(dat[l+68].split()[5]))
            except:
                tin[0].append(0)
            try:
                normtin[0].append(float(dat[l+69].split()[4]))
            except:
                normtin[0].append(0)
            try:
                gam[0].append(float(dat[l+70].split()[4]))
            except:
                gam[0].append(0)
            try:
                for x in range(l,len(dat)):
                    if dat[x].split('=')[0]==' Reduced chi-squared ':
                        break
                rcs.append(float(dat[x].split()[3]))
            except:
                rcs.append(0)
            try:
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.6 2.5\n':
                        break
                flux[0].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    flux[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[3].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 2.5 4.5\n':
                        break
                flux[1].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    flux[4].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[4].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 4.5 10.0\n':
                        break
                flux[2].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    flux[5].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    flux[5].append(0)
                pass
                
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.3 1.5\n':
                        break
                hardness[0].append(float(dat[k+1].split()[4][1:]))
                hardness[4].append(obs_id[i])
                if float(dat[l+45].split()[6])>0:
                    hardness[2].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    hardness[2].append(0)
                    
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 1.5 10.0\n':
                        break
                hardness[1].append(float(dat[k+1].split()[4][1:]))
                if float(dat[l+45].split()[6])>0:
                    hardness[3].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
                else:
                    hardness[3].append(0)
            
                for k in range(len(dat)):
                    if dat[k]=='XSPEC12>flux 0.3 10.0\n':
                        break
                lumr.append(4*np.pi*float(dat[k+1].split()[4][1:]))
                fluxall.append(float(dat[k+1].split()[4][1:]))
                
                for m in range(len(dat)):
                    if dat[m]=='XSPEC12>new 5 0\n':
                        break
                for n in range(m,len(dat)):
                    if dat[n]=='XSPEC12>flux 0.3 10.0\n':
                        break
                fluxbb.append(float(dat[n+1].split()[4][1:]))
        #            if float(dat[l+45].split()[6])>0:
        #                flux[5].append(float(dat[k+1].split()[4][1:])*float(dat[l+45].split()[8])/float(dat[l+45].split()[6]))
        #            else:
        #                flux[5].append(0)
        #            pass
            except:
                flux[0].append(0)
                flux[1].append(0)
                flux[2].append(0)
                flux[3].append(0)
                flux[4].append(0)
                flux[5].append(0)
                lumr.append(0)
                fluxall.append(0)
                fluxbb.append(0)

            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 1\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='2':
                        break
                if x>0:
                    NH[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    NH[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    NH[1].append(0)
                    NH[2].append(0)
            except:
                NH[1].append(0)
                NH[2].append(0)
        
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 2\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='2':
                        break
                if x>0:
                    tin[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    tin[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    tin[1].append(0)
                    tin[2].append(0)
            except:
                tin[1].append(0)
                tin[2].append(0)
            
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 3\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='3':
                        break
                if x>0:
                    normtin[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    normtin[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    normtin[1].append(0)
                    normtin[2].append(0)
            except:
                normtin[1].append(0)
                normtin[2].append(0)
            
            try:
                for a in range(len(dat)):
                    if dat[a]=='XSPEC12>err 4\n':
                        break
                    x=0
                for b in range(a,len(dat)):
                    if len(dat[b].split())>1 and dat[b].split()[0]=='Parameter':
                        x+=1
                        break
                for c in range(b,len(dat)):
                    if len(dat[c].split())==4 and dat[c].split()[0]=='4':
                        break
                if x>0:
                    gam[1].append(float(dat[c].split()[3].split(',')[0][2:]))
                    gam[2].append(float(dat[c].split()[3].split(',')[1][:-1]))
                elif x==0:
                    gam[1].append(0)
                    gam[2].append(0)
            except:
                gam[1].append(0)
                gam[2].append(0)
            print(obs_id[i],'pc mode is done')
         
    soft=np.array(flux[1])/np.array(flux[0])
    hard=np.array(flux[2])/np.array(flux[1])
    errsoft=np.sqrt((1/np.array(flux[0]))**2 *np.array(flux[3])**2 +(np.array(flux[1])/np.array(flux[0])**2)**2 *np.array(flux[4])**2)
    errhard=np.sqrt((1/np.array(flux[1]))**2 *np.array(flux[4])**2 +(np.array(flux[2])/np.array(flux[1])**2)**2 *np.array(flux[5])**2)
    Hardness=np.array(hardness[1])/np.array(hardness[0])
    errhardness=np.sqrt((1/np.array(hardness[0]))**2 *np.array(hardness[2])**2 +(np.array(hardness[1])/np.array(hardness[0])**2)**2 *np.array(hardness[3])**2)
    
    result=pd.DataFrame({'obsid':obsid,'date':date,'mode':mode,'rcs':rcs,'NH':NH[0],'err1 NH':NH[1],'err2 NH':NH[2],
                         'Tin':tin[0],'err1 Tin':tin[1],'err2 Tin':tin[2],
                         'Norm diskbb':normtin[0],'err1 Norm':normtin[1],'err2 Norm':normtin[2],
                         'Gamma':gam[0],'err1 Gamma':gam[1],'err2 Gamma':gam[2],
                         'Count rate':cr[0],'err Count rate':cr[1],
                         'Flux 0.6-2.5':flux[0],'err0.6-2.5':flux[3],
                         'Flux 2.5-4.5':flux[1],'err2.5-4.5':flux[4],
                         'Flux 4.5-10':flux[2],'err4.5-10':flux[5],
                         'fluxall':fluxall,'Lum/d^2':lumr, 'kompbb':fluxbb,
                         'Soft':soft,'err Soft':errsoft,'Hard':hard,'err Hard':errhard,'Hardness':Hardness,'err Hardness':errhardness})
    
#    ha=result[result['rcs']<=2].reset_index()
#    has=result[result['err1 Tin']!=0]
#    fig=pl.figure(0)
#    f=fig.add_subplot(111)
#    #f.errorbar(soft,hard,xerr=errsoft,yerr=errhard,fmt='.',label=r'$\chi^{2}/\nu > 2$')
#    f.errorbar(ha['Soft'],ha['Hard'],xerr=ha['err Soft'],yerr=ha['err Hard'],fmt='.',label=r'$\chi^{2}/\nu < 2$')
#    f.plot(fake['softbb'],fake['hardbb'],label='diskbb')
#    f.plot(fake['softpo']*1.3,fake['hardpo']+0.6,label='powerlaw')
#    f.legend()
#    #f.scatter(soft,hard)
#    f.set_xlim(0,1)
#    f.set_ylim(0,2.5)
#    f.set_xlabel('Soft')
#    f.set_ylabel('Hard')
    
#    fig=pl.figure(1)
#    f=fig.add_subplot(111)
#    f.errorbar(ha['Tin'],ha['Lum/d^2']/ha['Lum/d^2'].min(),xerr=ha['err1 Tin'],fmt='o')
    #f.set_ylim(0,100)
    #f.set_xlim(0,50)
    
    result.to_excel('/home/fahmi/Documents/data/'+obj[z]+'_pileup.xlsx')