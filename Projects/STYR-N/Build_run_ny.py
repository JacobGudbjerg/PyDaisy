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

#xls = pd.ExcelFile(r'S1-3_1993_2010_UD4.xlsx')
xl = pd.read_excel(r'S1-3_1993_2010_UD4.xlsx', None)
for sheet in xl.items():
    df=sheet[1]

    template = DaisyModel(r'S1_test2.dai')
    i=0
    unique_name = str(df['block'][i]) +'_' + df['field'][i]+'_' + str(df['treatment'][i])
    newfile= copy.deepcopy(template)    
    block = newfile.Input['defaction'][1]
    
    #for i in range(1,len(df, sheet_name)):
        
    for i in range(0,len(df)):
        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['date'][i].month), str(df['date'][i].day)]))
        
        if df['action'][i]=='sow':
            for crop in df['what'][i].split(','):
                    sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
                    block.Children.append(sow)  
        elif df['action'][i]=='harvest':
            for crop in df['what'][i].split(','):
                    harvest = DaisyEntry('harvest', ['"' + crop.strip() +'"'])
                    block.Children.append(harvest)  
        elif df['action'][i]=='fertilize':
            fert = DaisyEntry('fertilize',[])
            fert.Children.append(DaisyEntry('"' + df['what'][i]+'"',[]))
            fert.Children.append(DaisyEntry('equivalent_weight',[ str(df['amount'][i]) , '[kg N/ha]']))
            fert.Children.append(DaisyEntry('from', ['-5', '[cm]']))
            fert.Children.append(DaisyEntry('to', ['-15', '[cm]']))
            block.Children.append(fert)        
        else:
             block.Children.append(DaisyEntry(df['action'][i],[]))
        
    filename = os.path.join(unique_name, 'setup.dai')
    newfile.save_as(filename)


run_sub_folders(r'H:\Documents\PyDaisy\Projects\STYR-N','setup.dai')

