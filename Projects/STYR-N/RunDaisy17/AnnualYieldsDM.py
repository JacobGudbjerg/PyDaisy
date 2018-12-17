# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:53:20 2018

@author: tqc268
"""

import sys
import pandas as pd
import os
sys.path.append(r'../../../pydaisy/')

from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
sys.path.append(r'..\..\..\.')

from pydaisy.Daisy import *

xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']
xl['yr'] = xl['date'].map(lambda x: x.year)

# xl.set_index('date', inplace=True)

anyield = xl.groupby(['id', 'Parc nr', 'yr'])
#N_ann = anyield.get_group('Ntot_kg').sum(axis=1)
#DM_ann = anyield.get_group('DMtot_kg')

#df1.colums = ['yr', 'id', 'Ntot_rep1', 'Ntot_rep2', 'Ntot_mean', 'DMtot_rep1', 'DMtot_rep2', 'DMtot_mean']


def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())

MotherFolder='..\RunDaisy17'
items = os.walk(MotherFolder)
index=1

for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        df2= pd.DataFrame([rg, wc]).T
        df2.columns =['Ryegrass', 'Wclover']
        #df2['sim-totalDM']=df22['Ryegrass']+df22['Wclover']
        #df2 = df22.loc['2006-1-1':'2011-1-1',:]
        
        for y in range(2006, 2010):
            parc_sum={}
            sum=0
            for index, row in xl.iterrows():
                if row['id']==d and row['date'].year==y:
                    if row['Parc nr'] not in parc_sum:
                        parc_sum[row['Parc nr']]=0
                    parc_sum[row['Parc nr']]+=row['Ntot_kg']
                    sum=sum +row['Ntot_kg']
                
            print(parc_sum)

