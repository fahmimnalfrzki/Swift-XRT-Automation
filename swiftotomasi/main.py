#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 19:45:56 2019

@author: fahmi
"""

import os,glob,time,function
#from tqdm import tqdm
from astropy.coordinates import SkyCoord
import calb,reduc,extrct
import pandas as pd

file=open('obj.txt','r')
txt=file.readlines()
fol=[]
objek=[]
ra=[]
dec=[]
error_mssg=[]
success=[]

for i in range(len(txt)):
    if txt[i][0]!='\n' and txt[i][0]!='#' and txt[i][0]!='/':
        fol.append(txt[i].split('\t')[0][1:-1])
        objek.append(txt[i].split('\t')[1])
        ra.append(txt[i].split('\t')[2])
        dec.append(txt[i].split('\t')[3][:-1])
    if txt[i][0]=='/':
        folder=txt[i][:-1]

print('=========================================================================')
print('Swift XRT Data Processing Automation v2.0 Created by Fahmi Iman Alfarizki')
print(time.ctime(1566380948.887494))
print('Please read README.txt')
print('=========================================================================')
print(' ')
print(' ')
print(' ')
time.sleep(0.3)

print('DATA PROCESSING BEGIN at',time.ctime(time.time()))
time.sleep(0.5)

ti=time.time()
for i in range(len(fol)):
    tii=time.time()
    print(' ')
    try:
        cor_icrs=SkyCoord.from_name(objek[i])
        cor=cor_icrs.transform_to('fk5')
        RA=cor.ra.deg
        DEC=cor.dec.deg
        print(i+1,':',objek[i])
        print('Rigt Ascention:',RA)
        print('Declination:',DEC)
        print('Coordinate is found by Astropy from Simbad/Vizier.')
    except:
        pass
        print('Astropy cannot find the object coordinate from vizier or simbad')
        print('Try to find out the obj.txt')
        
        try:
            RA=float(ra[i])
            DEC=float(dec[i])
            print(i+1,':',objek[i])
            print('Rigt Ascention:',RA)
            print('Declination:',DEC)
        except:
            pass
            error_mssg.append('Astropy cannot find '+objek[i]+' coordinate and the script cannot find coordinate in obj.txt')
            print(objek[i],"Doesn't have RA and Dec. Please provide it to obj.txt")
            continue
    print(' ')
    print(' ')
    

    os.chdir(folder+fol[i])
    obs_id=glob.glob('00*')
    
#    for z in tqdm(range(10),desc='Loading '):
#        time.sleep(0.1)

    print(objek[i],'has',len(obs_id),'obsID(s) and ready to process')
    print('=========================================================================')
    
    for j in range(len(obs_id)):
        print(' ')
        os.chdir(folder+fol[i]+'/'+obs_id[j]+'/xrt/event/')
        print(str(j+1)+'/'+str(len(obs_id)),objek[i],'-',obs_id[j])
        try:
            calb.xrtpipeline(folder,fol[i],obs_id[j],RA,DEC)
        except:
            pass
            print('Error while running xrtpipeline or copying the clean event files. Please check xrtpipeline.log')
            error_mssg.append(objek[i]+'-'+obs_id[j]+' error while running xrtpipeline. Please check the xrtpipeline.log in /outdir/obs_id/')
            continue
        
#        for p in range(len(da)):
#            if da['obsid'][p]==obs_id[j]:
#                rin=da['rin'][p]

        wt=glob.glob('*wt*po_cl.evt')
        pc=glob.glob('*pc*po_cl.evt')
        
        if len(glob.glob('*grp.pha'))>0:
            print(objek[i],'-',obs_id[j],'has been proceed.')
            print(' ')
        else:
###=============   WINDOWED TIMING AND PHOTON COUNTING   =============    
            if len(wt)>0 and len(pc)>0:
                print(' ')
                print(' ')
                print('<>',objek[i],'-',obs_id[j],'has Windowed Timing and Photon Counting mode','<>')
    
                ##Windowed Timing
                print(' ')
                print('Creating source and background region file for Windowed Timing mode')
                print(' ')
                try:
                    function.region(obs_id[j],'WT',RA,DEC)
                except:
                    pass
                    print('Region file is not created')
                    error_mssg('Region file is not created')
                    continue
                
                time.sleep(0.3)
                print(' ')
                try:
                    try:
                        extrct.Xsel(folder,fol[i],obs_id[j],'WT','xsel_wt.log')
                    except:
                        pass
                        print('Error while running xselect. Please check the xsel_wt.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running xselect. Please check the xsel_wt.log')
                        continue
                    
                    try:
                        reduc.coprmf(folder,'WT',fol[i],obs_id[j])
                        print(' ')
                        print('Rmf file is successfully copied from caldb')
                    except:
                        pass
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while copying rmf. Please check the rmf file in caldb')
                        continue
        
                    print(' ')
                    print('Creating expomap file')
                    try:
                        
                        reduc.Expomap('WT',folder,fol[i],obs_id[j],glob.glob('*xwt*po_cl.evt')[0],'expomap_wt.log')
                    except:
                        pass
                        print('Error while creating expomap file. Please check expomap_wt.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating expomap file. Please check expomap_wt.log')
                        continue
                    
                    print(' ')
                    print('Creating Arf file')
                    try:
                        reduc.Xrtmkarf(glob.glob('*xwt*_ex.img')[0],'src'+obs_id[j]+'_wt.pi',
                                 obs_id[j]+'_wt_exp.arf',glob.glob('*wt*.rmf')[0],'arfwt.log')
                    except:
                        pass
                        print('Error while creating arf file. Please check arfwt.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating arf file. Please check arfwt.log')
                        continue
                    
                    print(' ')
                    print('Creating group pha file')
                    try:
                        reduc.grppha(folder,'WT',fol[i],obs_id[j],glob.glob('*wt*.rmf')[0],20)
                    except:
                        pass
                        print('Error while running grppha. Please check WT grpspek logfile.')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running grppha. Please check WT grpspek logfile')
                        continue            
                except:
                    pass
                    print('Windowed timing mode data processing unsuccessful')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+'Windowed timing mode data processing unsuccessful')
                    continue
                
                ##Photon Counting
                print(' ')
                print(' ')
                print('Creating source and background region file for Photon Counting mode')
                try:
                    function.region(obs_id[j],'PC',RA,DEC)
                    print('Region file is created successfully')
                except:
                    pass
                    print('Region file is not created')
                    error_mssg('Region file is not created')
                time.sleep(0.3)
                print(' ')
                
                try:
                    try:
                        extrct.Xsel(folder,fol[i],obs_id[j],'PC','xsel_pc.log')
                    except:
                        pass
                        print('Error while running xselect. Please check the xsel_pc.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running xselect. Please check the xsel_pc.log')
                        continue
                    
                    try:
                        reduc.coprmf(folder,'PC',fol[i],obs_id[j])
                        print(' ')
                        print('Rmf file is successfully copied from caldb')
                    except:
                        pass
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while copying rmf. Please check the rmf file in caldb')
                        continue
        
                    print(' ')
                    print('Creating expomap file')
                    try:
                        
                        reduc.Expomap('PC',folder,fol[i],obs_id[j],glob.glob('*xpc*po_cl.evt')[0],'expomap_pc.log')
                    except:
                        pass
                        print('Error while creating expomap file. Please check expomap_pc.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating expomap file. Please check expomap_pc.log')
                        continue
                    
                    print(' ')
                    print('Creating Arf file')
                    try:
                        reduc.Xrtmkarf(glob.glob('*xpc*_ex.img')[0],'src'+obs_id[j]+'_pc.pi',
                                 obs_id[j]+'_pc_exp.arf',glob.glob('*pc*.rmf')[0],'arfpc.log')
                    except:
                        pass
                        print('Error while creating arf file. Please check arfpc.log')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating arf file. Please check arfpc.log')
                        continue
                    
                    print(' ')
                    print('Creating group pha file')
                    try:
                        reduc.grppha(folder,'PC',fol[i],obs_id[j],glob.glob('*pc*.rmf')[0],20)
                        print('Grouppha is success!')
                    except:
                        pass
                        print('Error while running grppha. Please check PC grpspek logfile.')
                        error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running grppha. Please check PC grpspek logfile')
                        continue
                except:
                    pass
                    print('Windowed timing mode data processing unsuccessful')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+'Windowed timing mode data processing unsuccessful')
                    continue
                
                print('')
                print(fol[i],'-',obs_id[j],'successfully Processed')
                os.chdir(folder+fol[i])
        
###=============   WINDOWED TIMING   =============            
            elif len(wt)>0 and len(pc)==0:
                print(' ')
                print(' ')
                print('<>',objek[i],'-',obs_id[j],'has only Windowed Timing mode','<>')
                print(' ')
                print('Creating source and background region file for Windowed Timing mode')
                try:
                    function.region(obs_id[j],'WT',RA,DEC)
                    print('Region file is created successfully')
                except:
                    pass
                    print('Region file is not created')
                    error_mssg('Region file is not created')
                    continue
                time.sleep(0.3)
                print(' ')
                
                try:
                    extrct.Xsel(folder,fol[i],obs_id[j],'WT','xsel_wt.log')
                except:
                    pass
                    print('Error while running xselect. Please check the xsel_wt.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running xselect. Please check the xsel_wt.log')
                    continue
                
                try:
                    reduc.coprmf(folder,'WT',fol[i],obs_id[j])
                    print(' ')
                    print('Rmf file is successfully copied from caldb')
                except:
                    pass
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while copying rmf. Please check the rmf file in caldb')
                    continue
    
                print(' ')
                print('Creating expomap file')
                try:
                    
                    reduc.Expomap('WT',folder,fol[i],obs_id[j],glob.glob('*xwt*po_cl.evt')[0],'expomap_wt.log')
                except:
                    pass
                    print('Error while creating expomap file. Please check expomap_wt.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating expomap file. Please check expomap_wt.log')
                    continue
                
                print(' ')
                print('Creating Arf file')
                try:
                    reduc.Xrtmkarf(glob.glob('*xwt*_ex.img')[0],'src'+obs_id[j]+'_wt.pi',
                             obs_id[j]+'_wt_exp.arf',glob.glob('*wt*.rmf')[0],'arfwt.log')
                except:
                    pass
                    print('Error while creating arf file. Please check arfwt.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating arf file. Please check arfwt.log')
                    continue
                
                print(' ')
                print('Creating group pha file')
                try:
                    reduc.grppha(folder,'WT',fol[i],obs_id[j],glob.glob('*wt*.rmf')[0],20)
                    print('Grouppha is success!')
                except:
                    pass
                    print('Error while running grppha. Please check WT grpspek logfile.')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running grppha. Please check WT grpspek logfile')
                    continue
                reduc.grppha(folder,'WT',fol[i],obs_id[j],glob.glob('*wt*.rmf')[0],20)
                os.chdir(folder+fol[i])
                
                
    
    ###=============   PHOTON COUNTING   =============           
            elif len(wt)==0 and len(pc)>0:
                print(' ')
                print(' ')
                print('<>',objek[i],'-',obs_id[j],'has only Photon Counting mode','<>')
                print(' ')
                print('Creating source and background region file for Photon Counting mode')
                try:
                    function.region(obs_id[j],'PC',RA,DEC)
                    print('Region file is created successfully')
                except:
                    pass
                    print('Region file is not created')
                    error_mssg('Region file is not created')
                    continue
                
                time.sleep(0.3)
                print(' ')
                
                try:
                    extrct.Xsel(folder,fol[i],obs_id[j],'PC','xsel_pc.log')
                except:
                    pass
                    print('Error while running xselect. Please check the xsel_pc.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running xselect. Please check the xsel_pc.log')
                    continue
                
                try:
                    reduc.coprmf(folder,'PC',fol[i],obs_id[j])
                    print(' ')
                    print('Rmf file is successfully copied from caldb')
                except:
                    pass
                    print('Error while copying rmf file from caldb')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while copying rmf. Please check the rmf file in caldb')
                    continue
    
                print(' ')
                print('Creating expomap file')
                try:
                    
                    reduc.Expomap('PC',folder,fol[i],obs_id[j],glob.glob('*xpc*po_cl.evt')[0],'expomap_pc.log')
                except:
                    pass
                    print('Error while creating expomap file. Please check expomap_pc.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating expomap file. Please check expomap_pc.log')
                    continue
                
                print(' ')
                print('Creating Arf file')
                try:
                    reduc.Xrtmkarf(glob.glob('*xpc*_ex.img')[0],'src'+obs_id[j]+'_pc.pi',
                             obs_id[j]+'_pc_exp.arf',glob.glob('*pc*.rmf')[0],'arfpc.log')
                except:
                    pass
                    print('Error while creating arf file. Please check arfpc.log')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while creating arf file. Please check arfpc.log')
                    continue
                
                print(' ')
                print('Creating group pha file')
                try:
                    reduc.grppha(folder,'PC',fol[i],obs_id[j],glob.glob('*pc*.rmf')[0],20)
                    print('Grouppha is success!')
                except:
                    pass
                    print('Error while running grppha. Please check PC grpspek logfile.')
                    error_mssg.append(fol[i]+'-'+obs_id[j]+' error while running grppha. Please check PC grpspek logfile')
                    continue
            
                tff=time.time()
                tt=tff-tii
                print(' ')
                print(fol[i],'-',obs_id[j],'successfully Processed for %.2f' % tt,'seconds.')
                success.append(fol[i]+'-'+obs_id[j]+' successfully Processed for %.2f seconds.' % tt)
                os.chdir(folder+fol[i])
        print(' ')
        print(' ')
    tf=time.time()
    ttt=tf-ti
    print(' ')
    print(' ')
    print('All obsID of',objek[i],'are reduced and spend time about %.2f' % ttt,'seconds.')
    print('Please check',fol[i]+'_summary.log','to see your data processing summary for this object.')
    print(' ')
    print(' ')
    if i+1 < len(objek):
        print('Processing next object')
    else:
        print('All objects are reduced. Yeay you got clean spectrum! and ready to fit using XSPEC.')
    
    suma=open(folder+fol[i]+fol[i]+'_summary.log','w')
    suma.write('===========================================\n')
    suma.write("SWIFT XRT DATA PROCESSING SUMMARY LOGFILE\n")
    suma.write("OBJECT:  "+objek[i]+'\n')
    suma.write("RA    :  "+str(RA)+'\n')
    suma.write("DEC   :  "+str(DEC)+'\n')
    suma.write('===========================================\n')
    suma.write(" \n")
    suma.write(" \n")
    suma.write("===========Successful ObsID log ("+str(len(success))+'/'+str(len(obs_id))+")============\n")
    for w in range(len(success)):
        suma.write(success[w]+'\n')
    suma.write(" \n")
    suma.write("===========  Failed ObsID log  ============\n")
    for w in range(len(error_mssg)):
        suma.write(error_mssg[w]+'\n')
    suma.close()
