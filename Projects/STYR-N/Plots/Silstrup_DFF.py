# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:14:10 2018

@author: sdf945
"""

from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime

dm= DaisyModel (r'I:\SCIENCE-PLEN-PESTCAST\1_Validation track\DFF\Silstrup\1\Water_Field_Weekly.dlf')


sys.path.append(r'h:\Documents\PyDaisy')

from pydaisy.Daisy import *
dlf = DaisyDlf(r'h:\Documents\PyDaisy\Projects\STYR-N\IND_2_4\DailyP-harvest.dlf')

folder = r'I:\SCIENCE-PLEN-PESTCAST\1_Validation track\DFF\Silstrup\6'

#Diflufenican leaching
result_df_week = DaisyDlf(folder+'\Water_Field_Weekly.dlf')
result_dif = DaisyDlf(folder+'\weekly_soil_diflufenican.dlf')

matrixflow = result_df_week.Data.values[:,6]
bioporeflow = result_df_week.Data.values[:,7]
drainflow = matrixflow + bioporeflow

matrixleaching = result_dif.Data.values[:,7]
bioporeleaching = result_dif.Data.values[:,8]
totalleaching = matrixleaching + bioporeleaching

dif_conc_l = []

for j in np.arange(0, len(drainflow)):
    if drainflow[j]> 0:
        pest_conc = (totalleaching[j])*100/drainflow[j]
        dif_conc_l.append(pest_conc)
    else:    
        pest_conc = 0
        dif_conc_l.append(pest_conc)

lines=[]
plt.figure(figsize=(20,5))
line1, =plt.plot(result_dif.Data.index, dif_conc_l, color='purple', label='Weekly diflufenican leaching')
line2, =plt.plot(datetime.datetime(2012, 4, 25, 0, 0), 0.12, 'ro', color='crimson', label='Maxmimum detected concentration, PLAP')
#line3, =plt.plot(result_dif.Data.index, matrixleaching, color='purple', label='matrix leaching')
#line4, =plt.plot(result_dif.Data.index, bioporeleaching, color='green', label='biopore leaching')

lines.append(line1)
lines.append(line2)
#lines.append(line3)
#lines.append(line4)
   
#plt.axhline(0.01, color="red", linewidth=2, linestyle="--")
plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('Diflufenican leaching', fontsize=20,color='black')
plt.ylabel('g/ha', fontsize=20)
plt.legend(handles=lines, fontsize=20)
plt.tick_params(labelsize=20, axis='both', which='major')
plt.axvline(result_dif.Data.index[174], color="red", linewidth=2)
plt.axvline(result_dif.Data.index[204], color="red", linewidth=2)
plt.xlim(left=result_dif.Data.index[173], right=result_dif.Data.index[311]) 
plt.ylim(0, 0.2)

# plot dif med drænflow
#lines=[]
#plt.rcParams['font.size'] = 20
#fig, ax1 = plt.subplots(figsize=(20,5))
#ax1.plot(result_dif.Data.index, dif_conc_l, color='purple')
#ax1.plot(result_PLAP_dif.Data.index, result_PLAP_dif.Data.values[:,0], 'ro', color='crimson')
## Make the y-axis label, ticks and tick labels match the line color.
#ax1.set_ylabel('Diflufenican, ug/l', color='purple')
##ax1.tick_params('y', colors='b')
#
#ax2 = ax1.twinx()
#ax2.plot(result_dif.Data.index, drainflow, color='skyblue')
#ax2.set_ylabel('drainflow, mm/week', color='skyblue')
#ax1.set_xlim(left=result_dif.Data.index[44], right=result_dif.Data.index[70]) 
#ax1.set_ylim(0, 1)
#ax2.set_ylim(0, 50)
#plt.title('Diflufenican concentration in drain, Vamdrup precipitation')
#plt.show()


#AE-B107137leaching
result_AE_B = DaisyDlf(folder+'\weekly_soil_AE-B107137.dlf')
#result_test_20 = DaisyDlf(r'I:\SCIENCE-PLEN-PESTCAST\1_Validation track\DFF\Silstrup\5\weekly_soil_AE-B107137.dlf')
#result_test_20_df = DaisyDlf(r'I:\SCIENCE-PLEN-PESTCAST\1_Validation track\DFF\Silstrup\5\Water_Field_Weekly.dlf')

matrixleaching = result_AE_B.Data.values[:,7]
bioporeleaching = result_AE_B.Data.values[:,8]
totalleaching = matrixleaching + bioporeleaching

#matrixleaching_20 = result_test_20.Data.values[:,7]
#bioporeleaching_20 = result_test_20.Data.values[:,8]
#totalleaching_20 = matrixleaching_20 + bioporeleaching_20

#matrixflow_20 = result_test_20_df.Data.values[:,6]
#bioporeflow_20 = result_test_20_df.Data.values[:,7]
#drainflow_20 = matrixflow_20 + bioporeflow_20

AE_B_conc_l = []

for j in np.arange(0, len(drainflow)):
    if drainflow[j]> 0:
        pest_conc = (totalleaching[j])*100/drainflow[j]
        AE_B_conc_l.append(pest_conc)
    else:    
        pest_conc = 0
        AE_B_conc_l.append(pest_conc)

#AE_B_conc_20_l = []        
#for j in np.arange(0, len(drainflow_20)):
#    if drainflow_20[j]> 0:
#        pest_conc_20 = (totalleaching_20[j])*100/drainflow_20[j]
#        AE_B_conc_20_l.append(pest_conc_20)
#    else:    
#        pest_conc_20 = 0
#        AE_B_conc_20_l.append(pest_conc_20)


lines=[]
plt.figure(figsize=(20,5))
line1, =plt.plot(result_AE_B.Data.index, AE_B_conc_l, color='purple', label='Weekly AE-B107137 leaching, standard')
line2, =plt.plot(datetime.datetime(2012, 5, 2, 0, 0), 0.13, 'ro', color='crimson', label='Maximum detected concentration, PLAP')
#line3, =plt.plot(result_AE_B.Data.index, matrixleaching, color='green', label='matrix leaching')
#line4, =plt.plot(result_AE_B.Data.index, bioporeleaching, color='crimson', label='biopore leaching')
#line5, =plt.plot(result_AE_B.Data.index, AE_B_conc_20_l, color='green', label='Weekly AE-B107137 leaching, sprayed')
#line6, = plt.plot(result_AE_B.Data.index, totalleaching, color='purple', label='totalleaching g/ha') 

lines.append(line1)
#lines.append(line5)
lines.append(line2)
#lines.append(line3)
#lines.append(line4)
#lines.append(line6)
   
plt.axhline(0.01, color="red", linewidth=2, linestyle="--")
plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('AE-B107137 concentration in stream', fontsize=20,color='black')
plt.ylabel('ug/L', fontsize=20)
plt.legend(handles=lines, fontsize=20)
plt.tick_params(labelsize=20, axis='both', which='major')
plt.axvline(result_dif.Data.index[174], color="red", linewidth=2)
plt.axvline(result_dif.Data.index[204], color="red", linewidth=2)
plt.xlim(left=result_dif.Data.index[173], right=result_dif.Data.index[311]) 
plt.ylim(0, 0.2)

#AE-05422291 leaching 
result_AE = DaisyDlf(folder+'\weekly_soil_AE-05422291.dlf')

matrixleaching = result_AE.Data.values[:,7]
bioporeleaching = result_AE.Data.values[:,8]
totalleaching = matrixleaching + bioporeleaching

AE_conc_l = []

for j in np.arange(0, len(drainflow)):
    if drainflow[j]> 0.01:
        pest_conc = (totalleaching[j])*100/drainflow[j]
        AE_conc_l.append(pest_conc)
    else:    
        pest_conc = 0
        AE_conc_l.append(pest_conc)
   
lines=[]
plt.figure(figsize=(20,5))     
line1, =plt.plot(result_AE.Data.index, AE_conc_l, color='purple', label='Weekly AE-05422291 leaching')
#line3, =plt.plot(result_AE.Data.index, matrixleaching, color='green', label='matrix leaching')
#line4, =plt.plot(result_AE.Data.index, bioporeleaching, color='crimson', label='biopore leaching')

lines.append(line1)
#lines.append(line3)
#lines.append(line4)
   
plt.axhline(0.01, color="red", linewidth=2, linestyle="--")
plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('AE-05422291 concentration in drain', fontsize=20,color='black')
plt.ylabel('ug/L', fontsize=20)
plt.legend(handles=lines, fontsize=20)
plt.tick_params(labelsize=20, axis='both', which='major')
plt.axvline(result_dif.Data.index[174], color="red", linewidth=2)
plt.axvline(result_dif.Data.index[204], color="red", linewidth=2)
plt.xlim(left=result_dif.Data.index[173], right=result_dif.Data.index[311]) 
plt.ylim(0, 0.3)