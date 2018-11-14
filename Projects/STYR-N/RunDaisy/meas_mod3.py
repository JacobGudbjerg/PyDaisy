# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:41:29 2018

@author: tqc268
"""
import pandas as pd
import matplotlib.pyplot as plt


xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

#xl.index = xl.index.strftime("%Y-%M-%D")
plt.scatter(xl.index, xl['grassDM'], s=20, c='b', label='rygrass')

plt.plot(xl.grassDM, color='b') # plot kun ryegrass

plt.plot(xl.date, xl.grass+xl.cloverDM, color=o) # plotter total DM_a = df[cond].dropna()

# rg_mea = xl['grassN'].dropna()

plt.scatter(subset_b.col1, subset_b.col2, s=60, c='r', label='col3 <= 300') 
p        
        
