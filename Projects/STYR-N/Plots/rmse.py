# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 11:35:42 2018

@author: tqc268
"""
""
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

def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())
def 
# læser målt data og giver id som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']
# Collects the simulation results
MotherFolder='..\RunDaisy'
items = os.walk(MotherFolder)
#index=1
#fig = plt.figure(figsize=(18, 18))
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
#        plt.subplot(3,2,index)
#        index+=1
        df22= pd.DataFrame([rg, wc]).T
        df22.columns =['Ryegrass', 'Wclover']
        df2 =copy.deepcopy(df22.loc['2006-1-1':'2011-1-1',:])
        df22['date']=df22.index[0]   
        s=pd.concat([measdf, df22], axis=1, ignore_index=True)
# Vil gerne plott målt mod simuleret output - først et plot for hver id - og så alle samlet.
        #Udvælger en ny dataframe med data hvor ID = d. Det samme som tidligere blec gjort i loop
        s1=xl.loc[xl['id']==d]
        #Group og tag gennemsnit
        meas_rg =s1.groupby(s1.index)['grassDM'].mean()
        measdf=pd.DataFrame(meas_rg)
        text_file = open("meas_rg.txt", "w")
        text_file.write(stuff)
        text_file.close()
        np.savetxt('results.csv', (col1_array, col2_array, col3_array), delimiter=',')
        #measdf['date']=measdf.index
# Samler en dataframe med målt og simulert
        dat=pd.merge(measdf, df2, on=measdf.index, how='left')
        i = measdf.index.intersection(df2.index)
        dat_rg= measdf.loc[i, ['grassDM']].add(df2.loc[i, ['Ryegrass']]).div(1)
        dat_rg.columns=['obs', 'pred']
        rmse_val = rmse(np.array(dat['obs']), np.array(dat['pred']))