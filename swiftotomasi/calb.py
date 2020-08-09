#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALIBRATION PROCESS
xrtpipeline

@author: fahmi
"""
import os,shutil,glob,time

os.environ['HEADASPROMPT'] = '/dev/null'
def xrtpipeline(folder,obj,obsid,ra,dec):
    __PATH1__=folder+obj+'/'
    __PATH2__=folder+obj+'/outdir/'+obsid
    print('XRTPIPELINE BEGIN')
    print(time.ctime(time.time()))
    t1=time.time()
    with open("pipeline","w") as fout:
        a=2
        os.system('xrtpipeline indir='+__PATH1__+obsid+
        ' outdir='+__PATH2__+' steminputs=sw'+obsid+
        ' stemoutputs=DEFAULT createexpomap=yes cleanup=no srcra='+str(ra)+' srcdec='+str(dec)+' < pipeline > xrtpipeline.log')
    t2=time.time()
    t=t2-t1
    print('Xrtpipeline is finished for %.2f' % t,'seconds.')
    try:
        for m in range(len(glob.glob(__PATH2__+'/*po_cl.evt'))):
            shutil.copy2(glob.glob(__PATH2__+'/*po_cl.evt')[m],__PATH1__+obsid+'/xrt/event/')
        print(' ')
        print('po_cl.evt file(s) succesfully copied to directory')
    except:
        pass
        print('Error copying clean event files')
    
