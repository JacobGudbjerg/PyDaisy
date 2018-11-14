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

dat =xl.groupby(['treatment','block','field'])
 
xl['id']=xl.apply('treatment', axis =1) 
+_S_+'block+'_'+'field') 



xl = np.vectorize(xl)
xl['id']=xl(str(xl['treatment']),'field')


for col in xl():
        m=xl.set_index(['treatment','field'])
        
        
        xl.index = xl.index.strftime("%Y-%M-%D")
s1ind =plot(dat.get_group((4,1,'IND'))['date'], dat.get_group((4,1,'IND'))['grassDM']/100,'x')]

s1ind = [(DMG.get_group((4,1,'IND'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
s2ind = [(DMG.get_group((4,2,'IND'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
s3ind = [(DMG.get_group((4,3,'IND'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
s1ud = [(DMG.get_group((4,1,'UD'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
s2ud = [(DMG.get_group((4,2,'UD'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
s3ud = [(DMG.get_group((4,3,'UD'))['harvest'], DMG.get_group((4,1,'IND'))['grassDM']/100,'x')]
 