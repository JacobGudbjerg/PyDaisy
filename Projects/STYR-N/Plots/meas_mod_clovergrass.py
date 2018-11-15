# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 09:41:03 2018

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
# plt.figure(figsize = (10,20))
        plt.scatter(df2.index, df2['Ryegrass'],s=10, marker='x', c='b', label='ryegrass_sim')
        plt.scatter(df2.index, df2['Wclover'],s=10, marker='x', c='r', label='clover_sim')
        plt.title(d, position = (0.9, 0.9), fontweight="bold")
        plt.ylabel('t DM/ha')
        plt.scatter       
# plot målt DM udbytte ved x  grassDM, cloverDM, grassN, cloverN
        for i in range(0,len(xl)):
            if xl['id'][i]==d:    #skal sættes ind ovenpå søjlen der passer med id=d
                plt.scatter(xl.index[i], xl['grassDM'][i], s=10, c='b', label='ryegrass')
                plt.scatter(xl.index[i], xl['cloverDM'][i], s=10, c='r', label='clover')
plt.tight_layout()

MotherFolder='..\RunDaisy'
items = os.walk(MotherFolder)
index=1
fig = plt.figure(figsize=(18, 18))
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data         
# summere og plot af udbytte i N               
        Nharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
        N =Nharv.groupby('crop')
        rg = N.get_group('Ryegrass').sum(axis=1)
        wc = N.get_group('Wclover').sum(axis=1)
 # Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        plt.subplot(3,2,index)
        index+=1
        df33= pd.DataFrame([rg, wc]).T
        df33.columns =['Ryegrass', 'Wclover']
        df3 =df33.loc['2006-1-1':'2011-1-1',:]      
# plt.figure(figsize = (10,20))
        
        plt.scatter(df3.index, df3['Ryegrass'],s=10, marker='x', c='b', label='ryegrass_sim')
        plt.scatter(df3.index, df3['Wclover'],s=10, marker='x', c='r', label='clover_sim')
        plt.title(d, position = (0.9, 0.9), fontweight="bold")
        plt.ylabel('kg N/ha')
        plt.scatter       
# plot målt DM udbytte ved x  grassDM, cloverDM, grassN, cloverN
        for i in range(0,len(xl)):
            if xl['id'][i]==d:    #skal sættes ind ovenpå søjlen der passer med id=d
                plt.scatter(xl.index[i], xl['grassN'][i], s=10, c='b', label='ryegrass')
                plt.scatter(xl.index[i], xl['cloverN'][i], s=10, c='r', label='clover')
plt.tight_layout()
        
