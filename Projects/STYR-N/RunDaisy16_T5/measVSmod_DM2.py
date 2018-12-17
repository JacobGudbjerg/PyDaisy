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

xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())

MotherFolder='..\RunDaisy16_T5'
items = os.walk(MotherFolder)
index=1
fig = plt.figure(figsize=(10, 10))

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
        ax=plt.subplot(5,4,index)
        index+=1
        df22= pd.DataFrame([rg, wc]).T
        df22.columns =['Ryegrass', 'Wclover']
        df22['sim-totalDM']=df22['Ryegrass']+df22['Wclover']
        df2 = df22.loc['2006-1-1':'2011-1-1',:]                 
        s1=xl.loc[xl['id']==d]
        meas =(s1.groupby(s1.index)['grassDM'].mean(),s1.groupby(s1.index)['cloverDM'].mean(),
               s1.groupby(s1.index)['grassN'].mean(),s1.groupby(s1.index)['cloverN'].mean())
        # Samler en dataframe med målt og simulert
        ms=df2.join(meas[0]) 
        ms=ms.join(meas[1])
        ms['total-DM']=ms['cloverDM']+ms['grassDM']
        
        plt.scatter(ms['total-DM'], ms['sim-totalDM'], marker='x', c='black', s=15)
        plt.title(d+'-Total', position = (0.3, 0.85), fontweight="bold", fontsize=8)
        ax.set(ylabel=('simulated (t DM/ha)'), xlabel= 'measured')
        ax.set(xlim=(0,6), ylim=(0,6))
        ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
        rmse_val = rmse(ms['total-DM'],ms['sim-totalDM'])
        rs=str(round(rmse_val, 2))
        eva= ('RMSE ='+(rs))
        plt.text(3,0.2, eva)
        rs+=rs
        r1=rs
        
        ax=plt.subplot(5,4,index)
        index+=1
        plt.scatter(ms['cloverDM'], ms['Wclover'], marker='x', c='black', s=15)
        plt.title(d+'-Clover', position = (0.3, 0.85), fontweight="bold", fontsize=8)
        ax.set(ylabel=('simulated (t DM/ha)'), xlabel= 'measured')
        ax.set(xlim=(0,6), ylim=(0,6))
        ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
        rmse_val = rmse(ms['cloverDM'],ms['Wclover'])
        rs=str(round(rmse_val, 2))
        eva= ('RMSE ='+(rs))
        plt.text(3,0.2, eva)
        rs+=rs
        r2=rs
        
        ax=plt.subplot(5,4,index)
        index+=1
        plt.scatter(ms['grassDM'], ms['Ryegrass'], marker='x', c='black', s=15)
        plt.title(d+'-Grass', position = (0.3, 0.85), fontweight="bold", fontsize=8)
        ax.set(ylabel=('simulated (t DM/ha)'), xlabel= 'measured')
        ax.set(xlim=(0,6), ylim=(0,6))
        ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
        rmse_val = rmse(ms['grassDM'],ms['Ryegrass'])
        rs=str(round(rmse_val, 2))
        eva= ('RMSE ='+(rs))
        plt.text(3,0.2, eva)
        plt.tight_layout()
        rs+=rs
        r4=rs
       

rmse_tot=r2+r4
#rCG= ('RMSE_CG ='+(rs1))
#rclo= ('RMSE_Clover ='+(rs2))
#rgras= ('RMSE_Grass ='+(rs4))
rtotal= ('RMSE_Total ='+(rmse_tot))

#ax=plt.subplot(5,4)
#plt.text(3,0.2, rCG)
#plt.text(3,0.5, rclo)
#plt.text(3,0.7, rgras)
plt.text(3,0.9, rtotal)
        
fig.savefig("DM_hhj2.pdf", bbox_inches='tight')       
            