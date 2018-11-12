# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:41:29 2018

@author: tqc268
"""
import pandas as pd
import matplotlib.pyplot as plt


xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
DMG =xl.groupby(['treatment','block','field'])    

plt.plot(DMG.get_group((4,1,'IND'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM'],'x')