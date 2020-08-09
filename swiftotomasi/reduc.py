#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPECTRA REDUCTION
expomap, xrtmkrf, rmf selection, grppha

@author: fahmi
"""
import os,glob,shutil,function
from astropy.io import fits

rmfdir='/usr/local/src/heasoft-6.26.1/caldb/data/swift/xrt/cpf/rmf/'
lisrmf=os.listdir(rmfdir)

def coprmf(folder,mode,obj,obsid):
    if mode == 'WT' or mode == 'wt':
        file=glob.glob(folder+obj+'/'+obsid+'/xrt/event/*wt*cl.evt')[0]
        hdul=fits.open(file)
        mjd_obs=hdul[0].header['MJD-OBS']
        if(mjd_obs < 54101.): #2007Jan01 - 00:00:00
            rmf= "swxwt0to2s0_20010101v012.rmf"
        elif(mjd_obs < 54343.): #2007Ags31 - 00:00:00
            rmf="swxwt0to2s0_20070101v012.rmf"
        elif(mjd_obs < 54832.): #2009Jan01 - 00:00:00
            rmf="swxwt0to2s6_20010101v015.rmf"
        elif(mjd_obs < 55562.): #2011Jan01 - 00:00:00
            rmf="swxwt0to2s6_20090101v015.rmf"
        elif(mjd_obs < 56293.): #2013Jan01 - 00:00:00
            rmf="swxwt0to2s6_20110101v015.rmf"
        elif(mjd_obs < 56638.): #2013Des12 - 00:00:00
            rmf="swxwt0to2s6_20130101v015.rmf"
        else:
            rmf="swxwt0to2s6_20131212v015.rmf" 
        shutil.copy2(rmfdir+rmf,folder+obj+'/'+obsid+'/xrt/event/')
        return(rmf)
    
    if mode == 'PC' or mode == 'pc':
        file=glob.glob(folder+obj+'/'+obsid+'/xrt/event/*pc*cl.evt')[0]
        hdul=fits.open(file)
        mjd_obs=hdul[0].header['MJD-OBS']
        if(mjd_obs < 54101.): #2007Jan01 - 00:00:00
            rmf="swxpc0to12s0_20010101v012.rmf"
        elif(mjd_obs < 54343.): #2007Ags31 - 00:00:00
             rmf="swxpc0to12s0_20070101v012.rmf"
        elif(mjd_obs < 54832.): #2009Jan01 - 00:00:00
             rmf="swxpc0to12s6_20010101v014.rmf"
        elif(mjd_obs < 55562.): #2011Jan01 - 00:00:00
             rmf="swxpc0to12s6_20090101v014.rmf"
        elif(mjd_obs < 56293.): #2013Jan01 - 00:00:00
             rmf="swxpc0to12s6_20110101v014.rmf"
        else:
             rmf="swxpc0to12s6_20130101v014.rmf" 
        shutil.copy2(rmfdir+rmf,folder+obj+'/'+obsid+'/xrt/event/')
        return(rmf)

def Expomap(mode,folder,obj,obsid,infile,logfile):
    if mode == 'WT' or mode == 'wt':
        hdul=fits.open(glob.glob('*xwt*po_cl.evt')[0])
        attflag=hdul[0].header['ATTFLAG']
                
        if attflag=='100':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*sat*')[0]
        elif attflag=='110':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*pat*')[0]
        elif attflag=='101' or attflag=='111':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*uat*')[0]
        
        with open("expomap","w") as fout:
            hdfile=glob.glob(folder+obj+'/'+obsid+'/xrt/hk/'+'*hd*')[0]
        os.system("xrtexpomap infile="+infile+" attfile="+attfile+" hdfile="+hdfile+" clobber=yes outdir=./ < expomap > "+logfile)  
        print('Exposure map is successfully created')
    
    if mode == 'PC' or mode == 'pc':
        hdul=fits.open(glob.glob('*xpc*po_cl.evt')[0])
        attflag=hdul[0].header['ATTFLAG']
                
        if attflag=='100':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*sat*')[0]
        elif attflag=='110':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*pat*')[0]
        elif attflag=='101' or attflag=='111':
            attfile=glob.glob(folder+obj+'/'+obsid+'/auxil/'+'*uat*')[0]
        
        with open("expomap","w") as fout:
            hdfile=glob.glob(folder+obj+'/'+obsid+'/xrt/hk/'+'*hd*')[0]
        os.system("xrtexpomap infile="+infile+" attfile="+attfile+" hdfile="+hdfile+" clobber=yes outdir=./ < expomap > "+logfile)  
        print('Exposure map is successfully created')
    print(' ')
    
def Xrtmkarf(expfile,srcspec,outarf,rmf,logfile):
    with open("xrtmkarfile","w") as fout:
        a=1    
        os.system("xrtmkarf phafile="+srcspec+" outfile="+outarf+" expofile="+expfile+" psfflag=yes srcx=-1 srcy=-1 clobber=yes rmffile="+rmf+" < xrtmkarfile > "+logfile)
        print('Arf file is successfully created!')

def grppha(folder,mode,obj,obsid,rmf,groupmin):
    if mode == 'WT' or mode == 'wt':
        grp=['grppha',
             'bkg'+obsid+'_wt.pi',
             'bkg'+obsid+'_wt_grp.pha',
             'chatter=0',
             'comm=bad 0-29&sys_err 0.01& group min '+str(groupmin)+'&chkey respfile '
             +rmf+'&chkey ancrfile '+obsid
             +'_wt_exp.arf&chkey backscal 0.0697&exit']      #BACKGROUND
        function.skrip(grp,'grpspek_wt_bkg.log')
        
        grp=['grppha',
             'src'+obsid+'_wt.pi',
             obsid+'_wt_grp.pha',
             'chatter=0',
             'comm=bad 0-29&sys_err 0.01& group min '+str(groupmin)+'&chkey respfile '
             +rmf+'&chkey backfile bkg'+obsid+'_wt_grp.pha&chkey ancrfile '
             +obsid+'_wt_exp.arf&chkey backscal 0.003489&exit']
        function.skrip(grp,'grpspek_wt.log')
    if mode == 'PC' or mode == 'pc':
        grp=['grppha',
             'bkg'+obsid+'_pc.pi',
             'bkg'+obsid+'_pc_grp.pha',
             'chatter=0',
             'comm=bad 0-29&sys_err 0.01& group min '+str(groupmin)+'&chkey respfile '
             +rmf+'&chkey ancrfile '+obsid+'_pc_exp.arf&exit']
        function.skrip(grp,'grpspek_pc_bkg.log')
                    
        grp=['grppha',
             'src'+obsid+'_pc.pi',
             obsid+'_pc_grp.pha',
             'chatter=0',
             'comm=bad 0-29&sys_err 0.01& group min '+str(groupmin)+'&chkey respfile '
             +rmf+'&chkey backfile bkg'+obsid+'_pc_grp.pha&chkey ancrfile '+obsid+'_pc_exp.arf&exit']
        function.skrip(grp,'grpspek_pc.log')
