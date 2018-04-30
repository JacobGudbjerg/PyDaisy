# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:46:34 2017

@author: jpq949
"""

from multiprocessing import Pool
import time
import os
import csv
import MakeStats as ms
import pandas as pd
import numpy as np
from Daisy import MultiDaisy, DaisyDlf

place ='flak'
crop ='barley'
outputfilename =place + '_' + crop + '.csv'
Daisyfile=r'/home/projects/cu_10095/data/Git/PyDaisy/Bayer/'+ place + '_' + crop + r'/DaisyModel.dai'

NumberOfProcesses=32


class BayerExtract(object):
    
    def __init__(self, place, crop):
        self.pestnames =[]
        if(crop=='barley'):
          for i in np.arange(1,22):
              self.pestnames.append({'SprayName':'iodo-'+str(i),'PestNames':['iodo-'+str(i), 'mets-'+str(i)]})
        else:
          for i in np.arange(1,77):
              self.pestnames.append({'SprayName':'iodo-'+str(i),'PestNames':['iodo-autumn-'+str(i), 'mets-autumn-'+str(i)]})
          for i in np.arange(1,17):
              self.pestnames.append({'SprayName':'iodo-autumn-'+str(i),'PestNames':['iodo-autumn-'+str(i), 'mets-autumn-'+str(i), 'meso-'+str(i)]})
    
    def RunSingle(self, workdir):
        print('Running ' + workdir)
        dlffilename = 'WW SprayWW_drain_data.dlf'
        sprayfilename ='Flak_SB_spray.dlf'
        if(crop=='barley'):
          dlffilename = 'SB SpraySB_drain_data.dlf'
       
        pesticide = DaisyDlf(os.path.join(workdir, dlffilename)).Data
        sprayfile =DaisyDlf(os.path.join(workdir, sprayfilename))
        return (pesticide, sprayfile)
    
    
    def Extract(self, pesticide, sprayfile):        
        hours = 300*24 #The number of hours we are looking ahead. Should we use timespans?
    
        #Use the numpy array instead of pandas
        PestArray = pesticide.values
        Results=[]
        
        MatrixWaterIndex = pesticide.columns.get_loc('Matrix water') #get the index of the matrix water
        BioporeWaterIndex = pesticide.columns.get_loc('Biopore water')  #get the index of the biopore water
    
        #Loop the 
        for pest_name in self.pestnames:
            sprayname ='Spray-' + pest_name['SprayName']
            spraydates = sprayfile.Data[sprayname][sprayfile.Data[sprayname]>0].index[:-1]
            
            PesticideMatrixIndex=[]
            PesticideBioporesIndex=[]
            for molecule in pest_name['PestNames']:
                PesticideMatrixIndex.append(pesticide.columns.get_loc('Soil-' + molecule))
                PesticideBioporesIndex.append(pesticide.columns.get_loc('Biopores-' + molecule))
            
            molrange=range(0, len(PesticideMatrixIndex))
            
            for Appdate in spraydates:
                data = []
                start = pesticide.index.get_loc(Appdate)            
                #Now loop the timesteps in the current simulation
                for j in np.arange(start, start+hours):
                    drainwater = PestArray[j, MatrixWaterIndex]+PestArray[j, BioporeWaterIndex]
                    if drainwater>1e-10:
                        temp=[]
                        temp.append(drainwater)
                        for k in molrange:
                            bioporepest =PestArray[j, PesticideBioporesIndex[k]]
                            pest = PestArray[j, PesticideMatrixIndex[k]] + bioporepest
                            temp.append(pest)
                        data.append(temp)
    
                if len(data)>0: #no drain flow! Really?
                    print(Appdate)
                    print(pest_name)
                    result = ms.Stats(np.array(data).T,[item[0:4] for item in pest_name['PestNames']])
                    result['AppDate'] = Appdate
                    result['PestType'] = pest_name['SprayName'][0:4]
                    if  'autumn' in pest_name['SprayName']: #Look for autumn in name
                        result['Season'] = 'autumn'
                    else:
                        result['Season'] = 'spring'
                    Results.append(result)
    
        return Results

#Runs all the daisy-simulations in the list of workdirs in parallel.
def RunMany(workdirs):
    np=min(len(workdirs),NumberOfProcesses)
    print('Running ' + str (len(workdirs)) + ' directories on ' + str(np) + ' parallel processes')
    pp= Pool(np)
    AllResults=pp.map(RunSingle, workdirs)
    pp.terminate
    print(str(len(AllResults)))
    with open(outputfilename, 'wb') as f  :  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, AllResults[0][0].keys())
        w.writeheader()
        for result in AllResults:
            w.writerows(result)
                

if __name__ == '__main__':
    start = time.time()
    MD = MultiDaisy(Daisyfile)
    workdirs=[]
    for d in MD.ResultsDirLoop:
        workdirs.append(d)
    RunMany(workdirs)
    
    print("Time used = {0:.5f} s".format(time.time() - start))
