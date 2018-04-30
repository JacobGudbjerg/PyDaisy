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
       
    BFF =  1063/24 # hourly base flow FOCUS in L/h/ha
    BFC = 86.4/24  # hourly base flow UCPH in L/h/ha   
    S_pest_upland = 20
    S_drain_upland = 100
    S_field = 1
    S_pest_model = (S_pest_upland + S_field)*10**6 #ha*10**6
    S_drain_model = (S_drain_upland + S_field)*10**4 #ha*10**4    

    lims = {'meso':[1.28, 0.128, 0.0128], 'iodo':[1.08, 0.108, 0.0108], 'mets':[0.57, 0.057, 0.0057]}
    
    highest_conc=0
    pest_acc=0

    CurrentMaxEvent=[] 
    CurrentInterval=[]
    MinInterval=[]
    longest_event=[]
    nb_events=[]
    
    limitlist = lims[moleculename.lower()[0:4]]
    for i in np.arange(0, len(limitlist)):
        CurrentMaxEvent.append(0)
        CurrentInterval.append(0)
        MinInterval.append(9999999)
        longest_event.append(0)
        nb_events.append(0)
    

    #Calculate the concentration in the stream
    for j in np.arange(0, len(SingleYearLeaching)):
        pest_acc = pest_acc+SingleYearLeaching.iat[j,1] # ug/m**2
                                         
        I = max(0,SingleYearLeaching.iat[j,1]*S_pest_model)# ug/h 
        I_drains = max(0,SingleYearLeaching.iat[j,1])                  
        q_BFC = SingleYearLeaching.iat[j,0]*S_drain_model + BFC*S_drain_upland # L/h
        q_BFF = SingleYearLeaching.iat[j,0]*S_drain_model + BFF*S_drain_upland # L/h
        q_drains = SingleYearLeaching.iat[j,0]

        # we want to save the concentration in the stream BFC, BFF and drains for one of the app date

        conc_pest_stream_BFC = I/q_BFC
        conc_pest_stream_BFF = I/q_BFF
        conc_pest_drains = I_drains/q_drains
        
        highest_conc_BFF = max(highest_conc, conc_pest_stream_BFF)
        highest_conc_BFC = max(highest_conc, conc_pest_stream_BFC)
        highest_conc_drains = max(highest_conc, conc_pest_drains)
        
        for i in np.arange(0, len(limitlist)):#Loop all the limits
            if conc_pest_stream_BFC > limitlist[i]:
                if CurrentMaxEvent[i]==0: #Add the first timestep
                    if nb_events[i]>0: #Second event, we have an interval
                        MinInterval[i] = min(MinInterval[i], CurrentInterval[i])
                    CurrentInterval[i]=0
                CurrentMaxEvent[i]=CurrentMaxEvent[i]+1
            else:
                CurrentInterval[i]=CurrentInterval[i]+1
                if(CurrentMaxEvent[i]>0):
                    nb_events[i]=nb_events[i]+1
                    longest_event[i] = max(longest_event[i], CurrentMaxEvent[i])
                    CurrentMaxEvent[i]=0    
    
    toreturn ={'MaxConcentration_drains':highest_conc_drains,'MaxConcentration_BFC':highest_conc_BFC,'MaxConcentration_BFF':highest_conc_BFF, 'Accumulated_leaching': pest_acc}
    for i in np.arange(0, len(limitlist)):
        toreturn['nb_events_' + str(i) ]=nb_events[i]
        toreturn['longest_event_' + str(i) ]=longest_event[i]
        toreturn['shortest_interval_' + str(i) ]=MinInterval[i]
    
    return toreturn

