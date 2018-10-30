# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:52:27 2018

@author: jpq949
"""

import sys
import pandas as pd

sys.path.append(r'../../pydaisy')
from Daisy import *

df = pd.read_excel(r'..\Soil\jord fordelt på kommuner.xlsx', sheet_name='Ark1')

template = DaisyModel(r'setup_template.dai')

for i in range(0,len(df)):

    template.save_as(r'./columns/setup.dai')

run_sub_folders(r'./columns', 'setup.dai')