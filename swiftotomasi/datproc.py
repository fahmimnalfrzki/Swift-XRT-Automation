# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:18:24 2019

@author: ASUS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

obj=[]
ob=[]

file=open('obj.txt','r')
txt=file.readlines()

for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        obj.append(txt[i].split('\t')[0][1:-1])
        ob.append(txt[i].split('\t')[1])

fake=pd.read_csv('G:/data/CygX-1/fakeit_swift.tsv',delimiter=' ')

fig=pl.figure(0)
f=fig.add_subplot(111)
f.plot(fake['softbb'],fake['hardbb'],label='diskbb',zorder=1)
f.plot(fake['softpo'],fake['hardpo']+0.25,label='powerlaw',zorder=1)
for z in range(len(obj)):
    fol='G:/data/'+obj[z]+'/Swift/'
    #fake=pd.read_csv('G:/data/'+obj[z]+'/fakeit_swift.tsv',delimiter=' ')
    data=pd.read_excel('G:/data/'+obj[z]+' nH free.xlsx')

    ha=data[data['rcs']<=2].reset_index()
    has=data[data['err1 Tin']!=0]
#    fig=pl.figure(0)
#    f=fig.add_subplot(111)
    f.errorbar(soft,hard,xerr=errsoft,yerr=errhard,fmt='.',color='grey',zorder=2,alpha=0.3)
    f.errorbar(ha['Soft'],ha['Hard'],xerr=ha['err Soft'],yerr=ha['err Hard'],fmt='.',label=ob[z],zorder=3)
#    f.plot(fake['softbb'],fake['hardbb'],label='diskbb')
#    f.plot(fake['softpo']*1.3,fake['hardpo']+0.6,label='powerlaw')
    #f.scatter(soft,hard)
    f.set_xlim(0,1)
    f.set_ylim(0,2.5)
    f.set_xlabel('Soft')
    f.set_ylabel('Hard')
    
    fig1=pl.figure(1)
    f1=fig1.add_subplot(111)
    f.errorbar
f.legend(loc=9,bbox_to_anchor=(1.18,1.03))