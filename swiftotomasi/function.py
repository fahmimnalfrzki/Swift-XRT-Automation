#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MENDEFINISIKAN FUNGSI-FUNGSI

@author: fahmi
"""

import os,sys
import subprocess as sub

os.environ['HEADASPROMPT'] = '/dev/null'

def skrip(call,filelog):
        with sub.Popen(call, stdout=sub.PIPE, stderr=sub.STDOUT,
                       bufsize=1) as p, \
            open(filelog, 'wb') as file:
                for line in p.stdout: # b'\n'-sepaRated lines
                    sys.stdout.write(line.decode(sys.stdout.encoding)) # pass bytes as is
                    file.write(line)
                    
def region(name,mode,Ra,Dec):
    if mode == 'wt' or mode == 'WT':
        with open(name+"_src_wt.reg","w") as fout:
            fout.write("# Region file format: DS9 version 7.2\n")
            fout.write("global color=green dashlist=8 3 width=1 font='helvetica 10 normal roman' ")
            fout.write("select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
            fout.write("fk5\n")
            fout.write("circle("+str(Ra)+','+str(Dec)+","+str(47.2)+'")')
        with open(name+"_bkg_wt.reg","w") as fout:
            fout.write("# Region file format: DS9 version 7.2\n")
            fout.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" ")
            fout.write("select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
            fout.write("fk5\n")
            fout.write("circle("+str(Ra)+','+str(Dec)+","+str(188.8)+'")\n')
            fout.write("circle("+str(Ra)+','+str(Dec)+","+str(283.2)+'")')
        print('Windowed timing region file is made successfully!')
    if mode == 'pc' or mode == 'PC':
        with open(name+"_src_pc.reg","w") as fout:
            fout.write("# Region file format: DS9 version 7.2\n")
            fout.write("global color=green dashlist=8 3 width=1 font='helvetica 10 normal roman' ")
            fout.write("select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
            fout.write("fk5\n")
            fout.write("circle("+str(Ra)+','+str(Dec)+","+str(47)+'")')
            #fout.write("annulus("+str(Ra)+','+str(Dec)+","+str(rin)+'"'+","+str(47)+'")')
        with open(name+"_bkg_pc.reg","w") as fout:
            fout.write("# Region file format: DS9 version 7.2\n")
            fout.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" ")
            fout.write("select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
            fout.write("fk5\n")
            fout.write("circle("+str(Ra+ (1/1500)*Ra)+','+str(Dec+ (1/1500)*Dec)+","+str(3*47)+'")')
        print('Photon counting region file is made successfully!')
