# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:21:14 2018

@author: tqc268
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
# import datetime as datetime 

sys.path.append(r'h:\Documents\PyDaisy')

from pydaisy.Daisy import *
dlf = DaisyDlf(r'h:\Documents\PyDaisy\Projects\STYR-N\IND_2_4\DailyP-harvest.dlf')

df = dlf.Data  

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# JACOBs kodebid
DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
DMG =DMharv.groupby('crop')
# DMG.get_group('Ryegrass').plot()

# def zero_to_nan(values):
 #   """Replace every 0 with 'nan' and return a copy."""
 #   return [float('nan') if x==0 else x for x in values]
rg = DMG.get_group('Ryegrass').sum(axis=1)
wc = DMG.get_group('Wclover').sum(axis=1)
df2= pd.DataFrame([rg, wc]).T
df2.columns =['Ryegrass', 'Wclover']

# df2.index = df2.index.normalize()



# df2.index = df2.index.floor(df2)
# df2.mdates.DateFormatter('%Y-%m-%d')
# Bar plot with ryegrass and clovergrass
df2.plot.bar(stacked = True,figsize= (30,5))
#plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('Harvest', fontsize=20,color='black')
plt.ylabel('t DM /ha', fontsize=20)

#plt.xaxis.set_xticks(df2.index)
#plt.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
#plt.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m-%d"))
#_=plt.xticks(rotation=90) 
# plt.legend(handles=lines, fontsize=20)

# fig, ax = plt.subplots()
#