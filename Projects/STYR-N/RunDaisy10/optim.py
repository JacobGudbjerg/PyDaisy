# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:34:37 2018

@author: tqc268
"""
import sys
import pandas as pd
import os
sys.path.append(r'../../../pydaisy')
from Daisy import DaisyDlf, DaisyModel, run_sub_folders
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
from scipy.optimize import minimize
sys.path.append(r'..\..\..\.')


# læser målt data og giver id som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

#converts tuple into dataframes - HER GÅR DET galt...
#pf3=pd.DataFrame(meas, columns=['grassN'])
def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())
# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram

def opti(crop_name, m_cropname, output='DM', makeplots=False):
    
    MotherFolder='..\RunDaisy3'
    items = os.walk(MotherFolder)
    
    rmse_val=0
    
    index=1
   # fig = plt.figure(figsize=(8, 8))
    # fig, axes = plt.subplots(nrows=2, ncols=3)
    for root, dirs, filenames in items:
        for d in dirs:
            print(d)
            harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
            df=harvest.Data
    # summere og plot af udbytte i tørstof DM       
            DMharv= df[['crop', 'leaf_'+output, 'stem_'+output,'sorg_'+output]]
            DMG =DMharv.groupby('crop')
            rg = DMG.get_group(crop_name).sum(axis=1)
          # Laver et subplot, som derefter bliver det aktive som de næste plt virker på
            ax=plt.subplot(3,2,index)
            index+=1
            df22= pd.DataFrame([rg]).T
            df22.columns =[crop_name]
            df2 =df22.loc['2006-1-1':'2011-1-1',:]                 
    # Vil gerne plott målt mod simuleret output - først et plot for hver id - og så alle samlet.
    #Udvælger en ny dataframe med data hvor ID = d. Det samme som tidligere blev gjort i loop
    #Group og tag gennemsnit
            s1=xl.loc[xl['id']==d]
            meas =(s1.groupby(s1.index)['grassDM'].mean(),s1.groupby(s1.index)['cloverDM'].mean(),
                   s1.groupby(s1.index)['grassN'].mean(),s1.groupby(s1.index)['cloverN'].mean())
            # Samler en dataframe med målt og simulert
            ms=df2.join(meas[0]) 
            ms=ms.join(meas[1]) 
            ms=ms.join(meas[2]) 
            ms=ms.join(meas[3])
            rmse_val += rmse(ms[m_cropname],ms[crop_name])
            rs=str(round(rmse_val, 2))
            eva= ('RMSE ='+(rs))
            if makeplots:
                plt.scatter(ms[m_cropname], ms[crop_name], marker='x', c='black', s=15)
                plt.title(d+'-Clover', position = (0.6, 0.9), fontweight="bold", fontsize=8)
                ax.set(ylabel=('simulated (t DM/ha)'), xlabel= 'measured')
                #ax.set(xlim=(0,4), ylim=(0,4))
                ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
                plt.text(0.1,3.5, eva)
                plt.tight_layout()
    if makeplots:
        fig.savefig("Clover_DM.pdf", bbox_inches='tight')
    return(rmse_val)
    
def func(pars):
        cropdai=DaisyModel('..\common\SB-ryegrass.dai')
        cropdai.Input['defcrop']['LeafPhot']['Fm'].setvalue(pars[0])
        cropdai.Input['defAOM']['C_per_N'].setvalue(pars[0])
        cropdai.save()
               
        cropdai=DaisyModel('..\common\SB-wclover.dai')
        cropdai.Input['defcrop']['LeafPhot']['Fm'].setvalue(pars[0])
        cropdai.Input['defAOM']['C_per_N'].setvalue(pars[0])
        cropdai.save()
        
        
        run_sub_folders(r'.','setup.dai')
        print('Simulations done')
        r=opti('Wclover','cloverDM')
        r+=opti('Ryegrass','grassDM')
        r+=0.035*opti('Ryegrass','grassN','N')
        r+=0.035*opti('Wclover','cloverN','N')
        return r

if __name__ =='__main__':
    x0 =[4]
    res = minimize(func, x0)

