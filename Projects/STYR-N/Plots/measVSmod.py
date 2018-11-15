# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:34:37 2018

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

# læser målt data og giver id som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

# beregne gennemsnit af de to replikater for hver dato og id
meas= (xl.groupby(['id', xl.index])['grassDM'].mean(), 
       xl.groupby(['id', xl.index])['cloverDM'].mean(),
       xl.groupby(['id', xl.index])['grassN'].mean(),
       xl.groupby(['id', xl.index])['cloverDM'].mean())
#converts tuple into dataframes - HER GÅR DET galt...
pf3=pd.DataFrame(meas, columns=['grassN'])

# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram
MotherFolder='..\RunDaisy'
items = os.walk(MotherFolder)

index=1
fig = plt.figure(figsize=(18, 18))
# fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
# summere og plot af udbytte i tørstof DM       
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        plt.subplot(3,2,index)
        index+=1
        df22= pd.DataFrame([rg, wc]).T
        df22.columns =['Ryegrass', 'Wclover']
        df2 =df22.loc['2006-1-1':'2011-1-1',:]                 
      # Vil gerne plott målt mod simuleret output - først et plot for hver id - og så alle samlet.
        for i in range(0,len(xl)):
            if xl['id'][i]==d & xl.index[]:    
                plt.scatter(xl['grassDM'][i], df2['Ryegrass'] s=10, c='b', label='ryegrass')
                plt.scatter(df2.index, df2['Ryegrass'],s=10, marker='x', c='b', label='ryegrass_sim')
       
        plt.title(d, position = (0.9, 0.9), fontweight="bold")
        plt.ylabel('t DM/ha')
        plt.scatter
plt.tight_layout()
