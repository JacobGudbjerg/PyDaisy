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

df = pd.read_excel(r'DateTest_S1-S3_4.xlsx', sheet_name='Sheet1')

template = DaisyModel(r'S1_test1.dai')


for i in range(0,len(df)):
    if df['Year'][i]==1993:
        unique_name = df['Block'][i] +'_' + df['Field'][i]+'_' + str(df['Treatment'][i])
        newfile= template.copy()    
        block = newfile.Input['defaction'][1]
        
        
    if str(df['Sow_crop1'][i]) !='nan':
        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Plowing'][i].month), str(df['Plowing'][i].day)]))
        
        block.Children.append(DaisyEntry('plowing', []))
        
        if str(df['Fertil_date1'][i] != 'NaT'):
            if df['Fertil_date1'][i]>df['Seeding1'][i]:
                block.Children.append(DaisyEntry('fertilize', []))
        
        block.Children.append(DaisyEntry('seed_bed_preparation', []))
        
        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Seeding1'][i].month), str(df['Seeding1'][i].day)]))
        for crop in df['Sow_crop1'][i].split(','):
            sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
            block.Children.append(sow)

            
        if str(df['Seeding2'][i] != 'NaT'):
            if df['Seeding2'][i]<df['Harvest1'][i]: 
                if str(df['Fertil_date2'][i] != 'NaT'):
                    if df['Seeding2'][i]<df['Fertil_date2'][i]:
                        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Seeding2'][i].month), str(df['Seeding2'][i].day)]))
                        for crop in df['Sow_crop2'][i].split(','):
                              sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
                              block.Children.append(sow)
                    else:   
                        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Fertil_date2'][i].month), str(df['Fertil_date2'][i].day)]))
                        block.Children.append(DaisyEntry('fertilize2', []))
            else:
                block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Harvest1'][i].month), str(df['Harvest1'][i].day)]))
                for crop in df['Harvest_crop1'][i].split(','):
                    harvest = DaisyEntry('harvest', ['"' + crop.strip() +'"'])
                    block.Children.append(harvest)
             
                if str(df['Fertil_date2'][i] != 'NaT'):
                    if df['Seeding2'][i]>df['Fertil_date2'][i]:
                        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Seeding2'][i].month), str(df['Seeding2'][i].day)]))
                        if str(df['Sow_crop2'][i]) !='nan':
                          for crop in df['Sow_crop2'][i].split(','):
                              sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
                              block.Children.append(sow)
                    else:
                        block.Children.append(DaisyEntry('wait_mm_dd', [str(df['Fertil_date2'][i].month), str(df['Fertil_date2'][i].day)])) 
        
       # if str(df['Sow_crop2'][i]) !='nan':
        #    for crop in df['Sow_crop2'][i].split(','):
         #       sow = DaisyEntry('sow', ['"' + crop.strip() +'"'])
          #      block.Children.append(sow)      

    if df['Year'][i]==2010:    
        filename = os.path.join(unique_name, 'setup.dai')
        newfile.save_as(filename)

# run_sub_folders(r'./columns', 'setup.dai')