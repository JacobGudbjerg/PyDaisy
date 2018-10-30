# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:52:27 2018

@author: jpq949
"""

import sys
import pandas as pd
import os

sys.path.append(r'../../pydaisy')
from Daisy import *

df = pd.read_excel(r'Test_S1-S3_4.xlsx', sheet_name='Sheet1')

template = DaisyModel(r'S1_test1.dai')

for i in range(0,len(df)):
    unique_name = df['Block'][i] +'_' + df['Field'][i]+'_' + str(df['Treatment'][i])
    
    filename = os.path.join(unique_name, 'setup.dai')
    template.save_as(filename)

# run_sub_folders(r'./columns', 'setup.dai')