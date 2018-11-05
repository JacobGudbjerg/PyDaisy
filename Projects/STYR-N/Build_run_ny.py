# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:28:01 2018

@author: tqc268
"""


import sys
import pandas as pd
import os
import copy

sys.path.append(r'../../pydaisy')
from Daisy import *

df = pd.read_excel(r'S1-3_1993_2010_UD4.xlsx', sheet_name='S1')

template = DaisyModel(r'S1_test2.dai')


for i in range(0,len(df)):
    if df['Year'][i]==1994:
        unique_name = df['block'][i] +'_' + df['field'][i]+'_' + str(df['treatment'][i])
        newfile= copy.deepcopy(template)    
        block = newfile.Input['defaction'][1]
        
    if str(df['Sow_crop1'][i]) !='nan':
        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Plowing'][i].month), str(df['Plowing'][i].day)]))
        block.Children.append(DaisyEntry('plowing', []))
