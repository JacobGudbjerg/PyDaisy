# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:22:04 2017

@author: jpq949
"""

from Daisy import MultiDaisy
m= MultiDaisy(r'/home/projects/cu_10095/data/Git/PyDaisy/Bayer/WW_early/opt_flak_set_up.dai')

files=['WW_Early_iodoA_hourly', 'WW_Early_iodoS_hourly',
       'WW_Early_meso_hourly', 'WW_Early_metsA_hourly',
       'WW_Early_metsS_hourly', 'WW_Early_surfacewaterbalance', 'WW_Early_WW_drain_data']


for f in files:
    m.CollectResults(f + '.dlf').to_pickle(f+'.pkl')
