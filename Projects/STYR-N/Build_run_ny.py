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
i=0
unique_name = str(df['block'][i]) +'_' + df['field'][i]+'_' + str(df['treatment'][i])
newfile= copy.deepcopy(template)    
block = newfile.Input['defaction'][1]

for i in range(0,len(df)):
    block.Children.append(DaisyEntry('wait_mm_dd', [str(df['date'][i].month), str(df['date'][i].day)]))
    action =DaisyEntry(df['action'][i], [])
    
    if df['action'][i]=='sow':
        action.Children.extend(df['what'])
    elif df['action'][i]=='harvest':
        action.Children.extend(df['what'])
    #elif df['action'][i]=='fertilize':
     #   action.Children.append
    
    block.Children.append(action)
filename = os.path.join(unique_name, 'setup.dai')
newfile.save_as(filename)
