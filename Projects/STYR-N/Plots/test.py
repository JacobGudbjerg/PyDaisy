# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:01:28 2018

@author: tqc268
"""


sys.path.append(r'h:\Documents\PyDaisy')

from pydaisy.Daisy import *
dlf = DaisyDlf(r'h:\Documents\PyDaisy\Projects\STYR-N\IND_2_4\DailyP-harvest.dlf')

df = dlf.Data  

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#