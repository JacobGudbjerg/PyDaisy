# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:33:16 2018

@author: cbn978
"""

import pandas as pd
import numpy as np
import os
import csv
import MakeStats as ms
from Daisy import MultiDaisy, DaisyDlf

mdaisy = MultiDaisy(r'C:\GitHub\PyDaisy\Bayer\BigSim\opt_ror_set_up_WW.dai')
dlffilename = 'SB SpraySB_drain_data.dlf'

hours = 300*24 #The number of hours we are looking ahead. Should we use timespans?

AllResults=[]

pestnames =[]
for i in np.arange(1,22):
    pestnames.append({'SprayName':'iodo-'+str(i),'PestName':'iodo-'+str(i)})
    pestnames.append({'SprayName':'iodo-'+str(i),'PestName':'mets-'+str(i)})


#Loop the directories with daisy results
for d in mdaisy.ResultsDirLoop():
    print(d)
    pesticide = DaisyDlf(os.path.join(d, dlffilename)).Data

    times=[]
    drain_fs = []
    pests = []       
    spray=False
    HoursSinceSpray=0
    
    MatrixWaterIndex = pesticide.columns.get_loc('Matrix water')
    BioporeWaterIndex = pesticide.columns.get_loc('Biopore water')
    

    for pest_name in pestnames:
        PesticideSprayIndex =pesticide.columns.get_loc('Spray-' + pest_name['SprayName'])
        PesticideMatrixIndex =pesticide.columns.get_loc('Soil-' + pest_name['PestName'])
        PesticideBioporesIndex =pesticide.columns.get_loc('Biopores-' + pest_name['PestName'])
        
        #Now loop the timesteps in the current simulation
        for j in np.arange(0, len(pesticide)):
            if spray==False:
                if pesticide.iat[j, PesticideSprayIndex]>0:
                    spray=True
                    Appdate =pesticide.index[j]
            if(spray):
                drainwater = pesticide.iat[j,MatrixWaterIndex] + pesticide.iat[j,BioporeWaterIndex]
                if HoursSinceSpray<hours and drainwater>10**-4:      
                    times.append(pesticide.index[j])
                    drain_fs.append(drainwater)
                    pest = (pesticide.iat[j, PesticideMatrixIndex] + pesticide.iat[j, PesticideBioporesIndex])*10**2 # ug/m**2
                    pests.append(pest)                    
                else: #Now store the results
                    storethis = pd.DataFrame({'Drain':drain_fs, 'Pesticide': pests}, index=times)
                    results = ms.Stats(storethis, pest_name['PestName'])
                    results['AppDate'] = Appdate
                    results['PestName'] = pest_name['PestName']
                    results['PestType'] = pest_name['PestName'][0:4]
                    AllResults.append(results)
                    print(results)
                    #Reset the variables
                    HoursSinceSpray=0
                    drain_fs = []
                    pests = []
                    times=[]
                    spray=False
                HoursSinceSpray=HoursSinceSpray+1


with open(r'mycsvfile.csv', 'w') as f  :  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, AllResults[0].keys())
    w.writeheader()
    w.writerows(AllResults)