# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:33:16 2018

@author: cbn978
"""


# Step 1 - for 1 molecule and 1 soil on 1 crop: 
    # - Read outputs from daisy on super computer: analyze all application dates 
    # - Make a dataframe per application date showing the hourly molecule concentration in the stream with BF-UCPH according over 300 days every year
    
import numpy as np

def Stats(SingleYearLeaching, moleculename):
       
    #BFF_d =  1063/24 # hourly base flow FOCUS in L/h/ha
    BFC = 86.4/24  # hourly base flow UCPH in L/h/ha   
    S_pest_upland = 20
    S_drain_upland = 100
    S_field = 1
    S_pest_model = S_pest_upland + S_field #ha
    S_drain_model = S_drain_upland + S_field #ha    

    lims = {'meso':0.128 , 'iodo':0.108, 'mets':0.057}
    
    conc_drains=[]
    conc_pest_streams_BFC=[]     
    CurrentMaxEvent=0 
    MaxEvents=[]
    highest_conc=0
    pest_acc=0
    t_thrs=[]

    CurrentInterval=0
    MinInterval=9999999
    longest_event=0

    #Calculate the concentration in the stream
    for j in np.arange(0, len(SingleYearLeaching)):
        pest_acc = pest_acc+SingleYearLeaching.iloc[j,1]
        
        if SingleYearLeaching.iloc[j,0] >= 10**-4: 
            conc_drain = SingleYearLeaching.iloc[j,1]/SingleYearLeaching.iloc[j,0] # ug/L
            conc_drains.append(conc_drain)                    
        else:
            conc_drain = 0 # ug/L
            conc_drains.append(conc_drain)
                                 
        I = max(0,SingleYearLeaching.iloc[j,1]*S_pest_model*10**6)# ug/h                   
        q_BFC = SingleYearLeaching.iloc[j,0]*S_drain_model*10**4 + BFC*S_drain_upland # L/h
        conc_pest_stream_BFC = I/q_BFC
        conc_pest_streams_BFC.append(conc_pest_stream_BFC)
        highest_conc = max(highest_conc, conc_pest_stream_BFC)
        
        if conc_pest_stream_BFC> lims[moleculename.lower()[0:4]]:
            if CurrentMaxEvent==0: #Add the first timestep
                t_thrs.append(SingleYearLeaching.index[j])
                if len(t_thrs)>1: #Second event, we have an interval
                    MinInterval = min(MinInterval, CurrentInterval)
                CurrentInterval=0
            CurrentMaxEvent=CurrentMaxEvent+1
        else:
            CurrentInterval=CurrentInterval+1
            if(CurrentMaxEvent>0):
                MaxEvents.append(CurrentMaxEvent)
                CurrentMaxEvent=0
    
    nb_events=len(MaxEvents)
        
    if nb_events>0:
        longest_event = np.max(MaxEvents) # list with longest event duration each year 

    return {'MaxConcentration':highest_conc, 'Accumulated_leaching': pest_acc,  'nb_events' : nb_events, 'longest_event':longest_event, 'shortest_interval':MinInterval}

