#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 00:39:06 2019

@author: fahmi
"""
import os, mmap,glob
import numpy as np
import pandas as pd

file=open('obj.txt','r')
txt=file.readlines()
obj=[]
for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        obj.append(txt[i].split('\t')[0][1:-1])
        
for j in range(len(obj)):
    folder='/home/fahmi/Documents/data/'+obj[j]+'/'
    os.chdir(folder+'fakeit_dbbpo1/')
    
    flux_dbb=[[],[],[]]
    PhotIndex=np.linspace(1,3,75)
    for i in PhotIndex:
        with open("XSPEC","w") as fout:
            fout.write("setplot energy\n")
            fout.write("query yes\n")
            fout.write("mo tbabs*(diskbb+po)\n")
            fout.write("1.45 -1\n")
            fout.write("0.5 -1\n")
            fout.write("1. \n")
            fout.write(str(i)+"\n")
            fout.write("1.\n")
            fout.write("energies 0.3 10.0 1000\n")
            fout.write("flux 0.3 10.0")
        os.system("xspec < XSPEC > logfile.xspec")
        
        f = open('logfile.xspec','r')
        flux=f.readlines()
        for j in range(len(flux)):
            if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
                x=float(flux[j].split()[4][1:])
        
        norm=0.007515584704146/x
        
        with open("XSPEC","w") as fout:
            fout.write('setplot energy\n')
            fout.write('query yes\n')
            fout.write("mo tbabs*(diskbb+po)\n")
            fout.write("1.45 -1\n")
            fout.write("0.5 -1\n")
            fout.write("1. \n")
            fout.write(str(i)+"\n")
            fout.write("1.\n")
            fout.write('energies 0.3 10.0 1000\n')
            fout.write('flux 0.3 10.0\n')
            fout.write('new 3 '+str(norm)+'\n')
            fout.write('energies reset\n')
            fout.write('fakeit none\n')
            fout.write(glob.glob('*wt*.rmf')[0]+'\n')
            fout.write(glob.glob('*wt_exp.arf')[0]+'\n')
            fout.write('y\n')
            fout.write('fake\n')
            fout.write('dbb_'+str(i)+'keV.fak\n')
            fout.write('512\n')
            fout.write('statistic cstat\n')
            fout.write('statistic test pchi\n')
            fout.write('ignore 0.0-0.3,10.0-**\n')
            fout.write('fit\n')
            fout.write('new 1 0\n')
            fout.write('flux 0.6 2.5\n')
            fout.write('flux 2.5 4.5\n')
            fout.write('flux 4.5 10.0')
        os.system("xspec < XSPEC > logfile.xspec1")
        
        f = open('logfile.xspec1','r')
        flux=f.readlines()
        for j in range(90,len(flux)):
            if len(flux[j].split())==11 and flux[j].split()[9]=='2.5000':
                flux_dbb[0].append(float(flux[j].split()[4][1:]))
            if len(flux[j].split())==11 and flux[j].split()[9]=='4.5000':
                flux_dbb[1].append(float(flux[j].split()[4][1:]))
            if len(flux[j].split())==11 and flux[j].split()[9]=='10.000':
                flux_dbb[2].append(float(flux[j].split()[4][1:]))
    
    
    os.chdir(folder+'fakeit_dbbpo2/')
    flux_po=[[],[],[]]
    
    for i in PhotIndex:
        with open("XSPEC","w") as fout:
            fout.write("setplot energy\n")
            fout.write("query yes\n")
            fout.write("mo tbabs*(diskbb+po)\n")
            fout.write("1.45 -1\n")
            fout.write("1.5 -1\n")
            fout.write("1. \n")
            fout.write(str(i)+"\n")
            fout.write("1.\n")
            fout.write("energies 0.3 10.0 1000\n")
            fout.write("flux 0.3 10.0")
        os.system("xspec < XSPEC > logfile.xspec")
        
        f = open('logfile.xspec','r')
        flux=f.readlines()
        for j in range(len(flux)):
            if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
                x=float(flux[j].split()[4][1:])
        
        #norm=0.000637488218111/x
        
        with open("XSPEC","w") as fout:
            fout.write('setplot energy\n')
            fout.write('query yes\n')
            fout.write("mo tbabs*(diskbb+po)\n")
            fout.write("1.45 -1\n")
            fout.write("1.5 -1\n")
            fout.write("1. \n")
            fout.write(str(i)+"\n")
            fout.write("1.\n")
            fout.write('energies 0.3 10.0 1000\n')
            fout.write('flux 0.3 10.0\n')
            fout.write('new 3 '+str(norm)+'\n')
            fout.write('energies reset\n')
            fout.write('fakeit none\n')
            fout.write(glob.glob('*wt*.rmf')[0]+'\n')
            fout.write(glob.glob('*wt_exp.arf')[0]+'\n')
            fout.write('y\n')
            fout.write('fake\n')
            fout.write('po_'+str(i)+'.fak\n')
            fout.write('512\n')
            fout.write('statistic cstat\n')
            fout.write('statistic test pchi\n')
            fout.write('ignore 0.0-0.3,10.0-**\n')
            fout.write('fit\n')
            fout.write('new 1 0\n')
            fout.write('flux 0.6 2.5\n')
            fout.write('flux 2.5 4.5\n')
            fout.write('flux 4.5 10.0')
        os.system("xspec < XSPEC > logfile.xspec1")
        
        f = open('logfile.xspec1','r')
        flux=f.readlines()
        for j in range(90,len(flux)):
            if len(flux[j].split())==11 and flux[j].split()[9]=='2.5000':
                flux_po[0].append(float(flux[j].split()[4][1:]))
            if len(flux[j].split())==11 and flux[j].split()[9]=='4.5000':
                flux_po[1].append(float(flux[j].split()[4][1:]))
            if len(flux[j].split())==11 and flux[j].split()[9]=='10.000':
                flux_po[2].append(float(flux[j].split()[4][1:]))
    
    flux_dbb=np.array(flux_dbb)
    flux_po=np.array(flux_po)
    
    soft=[flux_dbb[1]/flux_dbb[0],flux_po[1]/flux_po[0]]
    hard=[flux_dbb[2]/flux_dbb[1],flux_po[2]/flux_po[1]]
    
    dat=['soft0.5 hard0.5 soft1.5 hard1.5']
    for i in range(len(soft[1])):
        dat.append(str(soft[0][i])+' '+str(hard[0][i])+' '+str(soft[1][i])+' '+str(hard[1][i]))        
    np.savetxt(folder+'fakeit_swiftdbpo.tsv',dat,fmt='%s')