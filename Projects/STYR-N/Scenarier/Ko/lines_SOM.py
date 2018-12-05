# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:31:39 2018

@author: tqc268
"""

import sys
import pandas as pd
import os
sys.path.append(r'../../../pydaisy')

from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
sys.path.append(r'..\..\..\.')

from pydaisy.Daisy import *

# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram

MotherFolder='..\Ko'
items = os.walk(MotherFolder)

index=1
fig = plt.figure(figsize=(15, 8))
#fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        om=DaisyDlf(os.path.join(root, d, "DailyP-Annual-OM.dlf"))
        df=om.Data
# summere og plot af udbytte i tørstof DM       
        soc=df['SOM1-C', 'SOM2-C', 'SOM3-C','SMB1-C','SMB2-C','SM3-C','AOM1-C','AOM2-C', 'AOM3-C']
        son=df['SOM1-N', 'SOM2-N', 'SOM3-N','SMB1-N','SMB2-N','SM3-N','AOM1-N','AOM2-N', 'AOM3-N']
        tot.soc=soc.sum(axis=1)        
        tot.son=son.sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        #ax=plt.subplot(3,2,index)
        #index+=1
        plt.lines(soc.index, soc.tot.soc)
        #df2 = df22.loc['1997-1-1':'2017-1-1',:]   
        #df2.index = df2.index.strftime("%Y-%m")
        #p1=plt.bar(df2.index, df2['Ryegrass'])
        #p2=plt.bar(df2.index, df2['Wclover'])
        #Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        #ax.set(ylabel=('simulated (t DM/ha)')) 
        plt.legend(d+'-soc')
        #plt.title(d+'-DM', position = (0.6, 0.9), fontweight="bold", fontsize=8)
        #ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        #ax.figure.autofmt_xdate()
        #ax.xaxis.set_major_locator()
        #ax.xaxis.set_major_formatter()
        plt.show()
        plt.tight_layout()
fig.savefig("K5-9_SOM.pdf", bbox_inches='tight')      
        #plt.scatter(df2.index, df2['Ryegrass'],s=20, marker='x', c='b', label='ryegrass_sim')
        #plt.scatter(df2.index, df2['Wclover'],s=20, marker='x', c='r', label='clover_sim')
        #plt.title(d)
        #plt.ylabel('t DM/ha')
