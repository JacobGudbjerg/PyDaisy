# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:01:28 2018

@author: tqc268
"""


import os

for filename in os.listdir('h:\Documents\PyDaisy\Projects\STYR-N\RunDaisy\..\'):
    if filename("DailyP-harvest.dlf"): 
        # print(os.path.join(directory, filename))
        continue
    else:
        continue


sys.path.append(r'h:\Documents\PyDaisy\Projects\STYR-N')

sys.path.append(r'h:\Documents\PyDaisy')
from pydaisy.Daisy import *
#dlf = DaisyDlf(r'H:\Documents\PyDaisy\Projects\STYR-N\RunDaisy\DailyP-harvest.dlf')


folder = r'H:\Documents\PyDaisy\Projects\STYR-N\RunDaisy\RunDaisy\IND_1_4'
result_cropN_day = DaisyDlf(folder+'\DailyP-Ryegrass.dlf')

# sum daily values of plant N in leaf, stem and sorg
N_rg = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

result_cropN_day = DaisyDlf(folder+'\DailyP-Wclover.dlf')
N_wc = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

result_cropN_day = DaisyDlf(folder+'\DailyP-SB.dlf')
N_sb = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]



#from pydaisy.Daisy import *
#dlf = DaisyDlf(r'h:\Documents\PyDaisy\Projects\STYR-N\IND_2_4\DailyP-harvest.dlf')

#df = dlf.Data  

#