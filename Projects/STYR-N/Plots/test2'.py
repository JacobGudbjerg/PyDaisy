# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:03:37 2018

@author: tqc268
"""

from scipy.interpolate import*
 


# læser målt data og giver id som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

meas= (xl.groupby(['id', xl.index])['grassDM'].mean(), 
       xl.groupby(['id', xl.index])['cloverDM'].mean(),
       xl.groupby(['id', xl.index])['grassN'].mean(),
       xl.groupby(['id', xl.index])['cloverDM'].mean())
#converts tuple into dataframes
pf3=pd.DataFrame(meas, columns=['grassN'])

me=pd.DataFrame({'grassDM':sf.index, 'list':sf.values})
df3 = meas.unstack(level='id')
df3.columns = df3.columns.droplevel()
meas.reset_index(inplace=True)

for i in range(0,len(xl)):
    if xl['id'][i]==d & xl.index[]:    #skal sættes ind ovenpå søjlen der passer med id=d
                plt.scatter(xl['grassDM'][i], df2 s=10, c='b', label='ryegrass')
                plt.scatter(xl.index[i], xl['cloverDM'][i], s=10, c='r', label='clover')