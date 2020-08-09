#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMAGE, SPECTRA, AND LIGHT CURVE EXTRACTION
xselect
@author: fahmi
"""

import os,glob,time


def Xsel(folder,obj,obsid,mode,logfile):
    print('Extract Image, Spectra, and Light Curve')
    time.sleep(0.5)
    if mode == 'wt' or mode == 'WT':
        print('Windowed Time Mode XRT Data Extraction Begin -',time.ctime(time.time()))
        t1=time.time()
        with open("xselectinputspec","w") as fout:
            fout.write("xsel\n")
            fout.write("no\n")
            fout.write("read events "+glob.glob('*xwt*po_cl.evt')[0]+'\n')
            fout.write("./\n")
            fout.write("yes\n")
            fout.write("extract image\n")
            fout.write("save image "+obsid+"_wt.img\n")
            fout.write("filter region "+obsid+"_src_wt.reg\n")
            fout.write("extract all\n")
            fout.write("save spectrum "+'src'+obsid+'_wt.pi\n')
            fout.write("save curve "+'src'+obsid+'_wt.lc\n')
            fout.write("clear region\n")
            fout.write("filter region "+obsid+"_bkg_wt.reg\n")
            fout.write("extract all\n")
            fout.write("save spectrum "+'bkg'+obsid+'_wt.pi\n')
            fout.write("save curve "+'bkg'+obsid+'_wt.lc\n')
            fout.write("clear region\n")
            fout.write("exit\n")
            fout.write("no\n")
        os.system("xselect < xselectinputspec > "+logfile)
        t2=time.time()
        t=t2-t1
        print('Windowed Timing Mode Data Have Been Extracted For %.2f' % t,'seconds')
    if mode == 'pc'or mode == 'PC':
        print('Photon Counting Mode XRT Data Extraction Begin -',time.ctime(time.time()))
        t1=time.time()
        with open("xselectinputspec","w") as fout:
            fout.write("xsel\n")
            fout.write("no\n")
            fout.write("read events "+glob.glob('*xpc*po_cl.evt')[0]+'\n')
            fout.write("./\n")
            fout.write("yes\n")
            fout.write("extract image\n")
            fout.write("save image "+obsid+"_pc.img\n")
            fout.write("filter region "+obsid+"_src_pc.reg\n")
            fout.write("extract all\n")
            fout.write("save spectrum "+'src'+obsid+'_pc.pi\n')
            fout.write("save curve "+'src'+obsid+'_pc.lc\n')
            fout.write("clear region\n")
            fout.write("filter region "+obsid+"_bkg_pc.reg\n")
            fout.write("extract all\n")
            fout.write("save spectrum "+'bkg'+obsid+'_pc.pi\n')
            fout.write("save curve "+'bkg'+obsid+'_pc.lc\n')
            fout.write("clear region\n")
            fout.write("exit\n")
            fout.write("no\n")
        os.system("xselect < xselectinputspec > "+logfile)
        t2=time.time()
        t=t2-t1
        print('Photon Counting Mode Data Have Been Extracted For %.2f' % t,'seconds')