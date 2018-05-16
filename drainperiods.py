# -*- coding: utf-8 -*-
"""
Created on Wed May 16 11:06:43 2018

@author: jpq949
"""

import pandas as pd
from datetime import datetime

drain = pd.read_csv(r'c:\test\Flakiodo1.csv')
drain[~drain.index.duplicated(keep='first')]
dates = (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in drain.index.values)
frame =pd.DataFrame(drain['Matrix water'], index=dates)

values = drain.values

InEvent=False
localcount=0
currentdrain =0
currentstart=None

date=[]
drains=[]

t=0

for i in range(0,len(frame) ):
    if values[i, 0] > 0.001: #We got drain flow
        if not InEvent:
            currentstart = frame.index[i]
        currentdrain += values[i,0]
        localcount += 1;
        InEvent=True
    else:
        if InEvent:
            if t>24:
                averagedrain = currentdrain/localcount
                date.append(currentstart)
                date.append(drain.index[i-t])
                drains.append(averagedrain)
                drains.append(averagedrain)
                currentdrain=0
                localcount=0
                InEvent=False
                t=0
            else:
                t=t+1