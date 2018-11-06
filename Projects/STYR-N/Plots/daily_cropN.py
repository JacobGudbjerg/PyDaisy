# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:14:10 2018

@author: sdf945
"""

import sys
sys.path.append(r'h:\Documents\PyDaisy')
from pydaisy.Daisy import *
# from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
import matplotlib.dates as mdates

# dlf = DaisyDlf(r'h:\Documents\StyrN\Clovergrass\Foulum\CG_1970-2000\DailyP-harvest.dlf')

#dm= DaisyModel (r'H:\Documents\StyrN\Clovergrass\Foulum\CG_1970-2000\DailyP-Ryegrass.dlf')

folder = r'H:\Documents\StyrN\Clovergrass\Foulumgaard\Run5'

#Diflufenican leaching
#result_cropN_day = DaisyDlf(folder+'\DailyP-Daily-CropProduction.dlf')
result_cropN_day = DaisyDlf(folder+'\DailyP-Ryegrass.dlf')
# sum daily values of plant N in leaf, stem and sorg
N_rg = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

result_cropN_day = DaisyDlf(folder+'\DailyP-Wclover.dlf')
N_wc = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

result_cropN_day = DaisyDlf(folder+'\DailyP-SB.dlf')
N_sb = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

#result_cropN_day = DaisyDlf(folder+'\DailyP-SB.dlf')
#N_sb = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]


lines=[]
plt.figure(figsize=(20,5))
line1, =plt.plot(result_cropN_day.Data.index, N_rg, color='purple', label='Ryegrass')
line2, =plt.plot(result_cropN_day.Data.index, N_wc, color='green', label='White clover')
line3, =plt.plot(result_cropN_day.Data.index, N_sb, color='crimson', label='Spring Barley')

lines.append(line1)
lines.append(line2)
lines.append(line3)
   
#plt.axhline(0.01, color="red", linewidth=2, linestyle="--")
plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('Daily crop production N', fontsize=20,color='black')
plt.ylabel('kg N /ha', fontsize=20)
plt.legend(handles=lines, fontsize=20)

plt.tick_params(labelsize=20, axis='both', which='major')
plt.axvline(result_dif.Data.index[174], color="red", linewidth=2)
plt.axvline(result_dif.Data.index[204], color="red", linewidth=2)
plt.xlim(left=result_dif.Data.index[173], right=result_dif.Data.index[311]) 
plt.ylim(0, 0.2)
