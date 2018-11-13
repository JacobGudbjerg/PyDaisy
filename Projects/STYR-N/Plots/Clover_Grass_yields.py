# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:31:39 2018

@author: tqc268
"""

from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import datetime as datetime
sys.path.append(r'h:\Documents\PyDaisy')
#sys.path.append(r'../../../pydaisy')
from pydaisy.Daisy import *
import os

# læser målt data og giver ID som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
# FEJL - sæt på unikt id af form  T+'treatment'+_+S+'block+_+'field (fx. T4_S1_IND)
xl['id']= xl.treatment+xl.field)

# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram
MotherFolder='h:\Documents\PyDaisy\Projects\STYR-N\RunDaisy'
items = os.walk(MotherFolder)
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
        df2= pd.DataFrame([rg, wc]).T
        df2.columns =['Ryegrass', 'Wclover']
        df2.index = df2.index.strftime("%Y")
        df2.plot.bar(stacked = True)
        plt.title(d)
        plt.ylabel('t DM/ha')
# plot målt DM udbytte ved x  grassDM, cloverDM, grassN, cloverN
        for i in range(0,len(xl)):
        if xl['id'][i]=='d':    #skal sættes ind ovenpå søjlen der passer med id=d
            plt.plot(xl.date, xl.grassDM, color='b') # plot kun ryegrass
            plt.plot(xl.date, xl.grass+xl.cloverDM, color=o) # plotter total DM
            
# summere og plot af udbytte i N               
#        Nharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
#        DMG =DMharv.groupby('crop')
#        rg = DMG.get_group('Ryegrass').sum(axis=1)
#        wc = DMG.get_group('Wclover').sum(axis=1)
#        df3= pd.DataFrame([rg, wc]).T
#        df3.columns =['Ryegrass', 'Wclover']
#        df3.index = df3.index.strftime("%Y")
#        df3.plot.bar(stacked = True)
#        plt.title(d)
#        plt.ylabel('kg N/ha')