# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:28:01 2018

@author: tqc268
"""


import sys
import pandas as pd
import os
import copy

sys.path.append(r'../../../pydaisy')

from Daisy import *
if __name__ =='__main__':
    xl = pd.read_excel(r'Treat4_S1_S3.xlsx', None)
    for sheet in xl.items():
        df=sheet[1]
        template = DaisyModel(r'Foulum94-10_v3.dai')
        i=0
        unique_name = sheet[0]
        newfile= copy.deepcopy(template)    
        block = newfile.Input['defaction'][1]
            
        for i in range(0,len(df)):
            block.Children.append(DaisyEntry('wait_mm_dd', [str(df['date'][i].month), str(df['date'][i].day)]))
            
            if df['action'][i]=='sow':
                for crop in df['what'][i].split(','):
                        sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
                        block.Children.append(sow)  
            elif df['action'][i]=='harvest' or df['action'][i]=='cut' :
                for crop in df['what'][i].split(','):
                        harvest = DaisyEntry(df['action'][i], ['"' + crop.strip() +'"'])
                        harvest.Children.append(DaisyEntry('stub', ['7 [cm]']))
                        block.Children.append(harvest)  
            elif df['action'][i]=='fertilize':
                fert = DaisyEntry('fertilize',[])
                fert.Children.append(DaisyEntry('"' + df['what'][i]+'"',[]))
                fert.Children.append(DaisyEntry('equivalent_weight',[ str(df['amount'][i]) , '[kg N/ha]']))
                fert.Children.append(DaisyEntry('from', ['-5', '[cm]']))
                fert.Children.append(DaisyEntry('to', ['-15', '[cm]']))
                block.Children.append(fert)
            elif df['action'][i]== 'irrigate':
                irri= DaisyEntry('irrigate_overhead', [str(df['amount'][i]), '[mm/h]'])
                block.Children.append(irri)
            else:
                block.Children.append(DaisyEntry(df['action'][i],[]))
            
        filename = os.path.join(unique_name, 'setup.dai')
        newfile.save_as(filename)
    
    run_sub_folders(r'.','setup.dai')

