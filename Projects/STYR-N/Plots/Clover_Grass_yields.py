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
from pydaisy.Daisy import *
import os


MotherFolder='h:\Documents\PyDaisy\Projects\STYR-N\RunDaisy'

items = os.walk(MotherFolder)

for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
        df2= pd.DataFrame([rg, wc]).T
        df2.columns =['Ryegrass', 'Wclover']
        df2.index = df2.index.strftime("%Y")

        fig, ax = plt.subplots(nrows=3, ncols=2)
        for row in ax:
            for col in row:
                col.plot(df2)
        plt.show()

        # plt.plot.bar( 


#        df2.plot.bar(stacked = True,figsize= (30,5))
    
