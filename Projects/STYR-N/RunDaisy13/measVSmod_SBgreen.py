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

xl = pd.read_excel(r'..\SB_green2.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

MotherFolder='..\RunDaisy13'
items = os.walk(MotherFolder)

index=1
fig = plt.figure(figsize=(8, 5))
#fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
# summere og plot af udbytte i tørstof DM       
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        Nharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
        DMG =DMharv.groupby('crop')
        sb_greenDM = DMG.get_group('SB').sum(axis=1)
        NG = Nharv.groupby('crop')
        sb_greenN = NG.get_group('SB').sum(axis=1)
        
        #lupin = DMG.get_group('Aert').sum(axis=1)
        #majs = DMG.get_group('Silomajs').sum(axis=1)
        #SB_pea = DMG.get_group('Pea').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        #ax=plt.subplot(2,1,index)
        #index+=1
        df22= pd.DataFrame([sb_greenDM, sb_greenN]).T
        df22.columns =['SB_greenDM', 'SB_greenN']
        df2 =df22.loc['2006-1-1':'2011-1-1',:]         
        #df2.index = df2.index.strftime("%Y-%m")
        s1=xl.loc[xl['id']==d]
        meas =(s1.groupby(s1.index)['DM_greenSB'].mean(),s1.groupby(s1.index)['N_greenSB'].mean())
        # Samler en dataframe med målt og simulert
        ms=df2.join(meas[0]) 
        ms =ms.join(meas[1])
        #plt.scatter(ms['DM_greenSB'], ms['SB_greenDM'], marker='x', c='black', s=15)
        plt.plot([0, 100], [0, 100], transform=ax.transAxes, c='black', linestyle ='--')
        plt.scatter(ms['N_greenSB'], ms['SB_greenN'], marker='x', c='black', s=15)
        #plt.title(d+'-Clover', position = (0.8, 0.9), fontweight="bold", fontsize=8)
        
        #p2=plt.plot(ms.index, ms['DM_greenSB'])
        #Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        ax.set(ylabel=('simulated (t DM/ha)')) 
        #plt.legend((p1[0], p2[0]), ('Sim', 'meas'))
        #plt.title(d+'-DM', position = (0.5, 0.1), fontweight="bold", fontsize=8)
    
        #plt.show()
        #plt.tight_layout()
#fig.savefig("SB_green_hhj.pdf", bbox_inches='tight')      
   #         
# summere og plot af udbytte i N               
#
#        DMG =DMharv.groupby('crop')
#        rg = DMG.get_group('Ryegrass').sum(axis=1)
#        wc = DMG.get_group('Wclover').sum(axis=1)
#        df3= pd.DataFrame([rg, wc]).T
#        df3.columns =['Ryegrass', 'Wclover']
#        df3.index = df3.index.strftime("%Y")
#        df3.plot.bar(stacked = True)
#        plt.title(d)
#        plt.ylabel('kg N/ha')