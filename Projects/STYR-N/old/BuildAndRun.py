# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:52:27 2018

@author: jpq949
"""

import sys
import pandas as pd
import os
import copy

sys.path.append(r'../../pydaisy')
from Daisy import *

df = pd.read_excel(r'Test_S1-S3_4.xlsx', sheet_name='Sheet1')

template = DaisyModel(r'S1_test1.dai')


for i in range(0,len(df)):
    if df['Year'][i]==1994:
        unique_name = df['Block'][i] +'_' + df['Field'][i]+'_' + str(df['Treatment'][i])
        newfile= copy.deepcopy(template)
        
    block = copy.deepcopy(template.Input['defaction'][1])
    if str(df['Plowing'][i]) =='NaT':
        block.Children.remove(block['plowing'][0])
        block.Children.remove(block['seed_bed_preparation'][0])
    else:
        block['wait_mm_dd'][0].setvalue(df['Plowing'][i].month, 0)
        block['wait_mm_dd'][0].setvalue(df['Plowing'][i].day, 1)
        block['wait_mm_dd'][1].setvalue(df['Seeding'][i].month, 0)
        block['wait_mm_dd'][1].setvalue(df['Seeding'][i].day, 1)

    
    
    newfile.Input['defaction'][1].Children.extend(block.Children)

    if df['Year'][i]==2010:    
        filename = os.path.join(unique_name, 'setup.dai')
        newfile.save_as(filename)

# run_sub_folders(r'./columns', 'setup.dai')