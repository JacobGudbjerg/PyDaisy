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

def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())

def extract(crop_name, filnavn, output):
    harvest=DaisyDlf(filnavn)
    df=harvest.Data
    # summere og plot af udbytte i tørstof DM       
    harv= df[['crop', 'leaf_'+output, 'stem_'+output,'sorg_'+output]]
    DMG =harv.groupby('crop')
    rg = DMG.get_group(crop_name).sum(axis=1)
    return(rg)
        
def opti(crop_name, m_cropname, output='DM', makeplots=False):
    
    MotherFolder='..\RunDaisy15opt'
    items = os.walk(MotherFolder)
    
    rmse_val=0
    index=1
    for root, dirs, filenames in items:
        for d in dirs:    
            rg=extract(crop_name, os.path.join(root, d, "DailyP-harvest.dlf"), output)
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
        return(rmse_val)
    
def func(pars):
    

        cropdai=DaisyModel('./hhj.v2-wclover.dai')
        cropdai.Input['defcrop']['Prod']['LfDR'][2].setvalue(pars[0])
        cropdai.Input['defcrop']['Prod']['LfDR'][3].setvalue(pars[1])
        cropdai.Input['defcrop']['Prod']['RtDR'][2].setvalue(pars[2])
        cropdai.Input['defcrop']['Prod']['RtDR'][3].setvalue(pars[3])
        cropdai.Input['defcrop']['LeafPhot']['Fm'].setvalue(pars[4])
        cropdai.save()       
#       
        cropdai=DaisyModel('./hhj-ryegrass.dai')
        cropdai.Input['defcrop']['LeafPhot']['Fm'].setvalue(pars[5])
        #cropdai.Input['defAOM']['C_per_N'].setvalue(pars[3])
        cropdai.save()
        
        
        run_sub_folders(r'.','setup.dai')
        print('Simulations done')
        r=opti('Wclover','cloverDM')
        r+=opti('Ryegrass','grassDM')
        r+=0.035*opti('Ryegrass','grassN','N')
        r+=0.035*opti('Wclover','cloverN','N')
        f = open("myfile4.txt", "a")
        f.write(str(pars) + " " + str(r) +"\n")
        f.close()
        return r

def progress_print(x):
    print (x)

if __name__ =='__main__':
    x0 =[0.12, 0.18, 0.12, 0.18, 2, 2 ] 
    res = minimize(func, x0, method='Nelder-Mead', callback=progress_print,  options={'disp':True, 'maxiter':100})

