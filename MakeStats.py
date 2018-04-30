# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:33:16 2018

@author: cbn978
"""
    
import numpy as np

def Stats(SingleYearLeaching, moleculename):
       
    BFF_d =  1063/24 # hourly base flow FOCUS in L/h/ha
    BFC = 86.4/24  # hourly base flow UCPH in L/h/ha   
    S_pest_upland = 20 #ha
    S_drain_upland = 100 #ha
    Baseflow =BFC*S_drain_upland
    Baseflow_BFF =BFF_d*S_drain_upland
    S_field = 1 #ha
    S_pest_model = (S_pest_upland + S_field)*10**6 #ha*10**6
    S_drain_model = (S_drain_upland + S_field)*10**4 #m2    

    #Limits in µg/l
    lims = {'meso':[ 1.28, 0.128, 0.0128], 'iodo':[1.08, 0.108, 0.0108], 'mets':[0.57, 0.057, 0.0057]}

    NoOfLimits=len(lims[moleculename[0]])
    NoOfMolecules =len(moleculename)
    
    chem_weights = {'meso':1, 'iodo':1, 'mets':1}

    #initialize arrays
    max_conc=[0]*NoOfMolecules
    max_conc_BFF=[0]*NoOfMolecules
    max_conc_drains=[0]*NoOfMolecules
    pest_acc=[0]*NoOfMolecules
    water_acc=0

    CurrentMaxEvent=[0]*NoOfLimits 
    CurrentInterval=[0]*NoOfLimits
    MinInterval=[9999999]*NoOfLimits
    longest_event=[0]*NoOfLimits
    nb_events=[0]*NoOfLimits
       
 #Loop all timesteps
    for j in np.arange(0, len(SingleYearLeaching)):
        #sum the total drain flow
        water_acc = water_acc+SingleYearLeaching[j,0]
        #Calculate the flow in the stream
        q=SingleYearLeaching[j,0]
        q_BFC = q*S_drain_model +  Baseflow# L/h
        q_BFF = q*S_drain_model +  Baseflow_BFF# L/h
       
        scaled_conc=[0]*NoOfLimits

#Loop all the pesticides
        for l in np.arange(0, NoOfMolecules):
            #sum the total accumulated pesticide
            I=max(0,SingleYearLeaching[j,1+l])
            pest_acc[l] +=I
            #Calculate the concentration in the stream
            conc_pest_stream_BFC = I*S_pest_model/q_BFC
            conc_pest_stream_BFF = I*S_pest_model/q_BFF
            #Store the max concentration
            max_conc[l] = max(max_conc[l], conc_pest_stream_BFC)
            max_conc_BFF[l] = max(max_conc_BFF[l], conc_pest_stream_BFF)
            max_conc_drains[l] = max(max_conc_drains[l], I/q)
            #Scale concentration with limit       
            for i in np.arange(0, NoOfLimits):#Loop all the limits
                scaled_conc[i] += conc_pest_stream_BFC/lims[moleculename[l]][i] * chem_weights[moleculename[l]] 
        
        for i in np.arange(0, NoOfLimits):#Loop all the limits
            if scaled_conc[i] >=1: #Check if we are above the toxicity limit
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

#Check if we were in an event                    
    for i in np.arange(0, NoOfLimits):#Loop all the limits
      CurrentInterval[i]=CurrentInterval[i]+1
      if(CurrentMaxEvent[i]>0):
          nb_events[i]=nb_events[i]+1
          longest_event[i] = max(longest_event[i], CurrentMaxEvent[i])
          CurrentMaxEvent[i] = 0
          
    #Now print
    toreturn ={'Accumulated_water': water_acc}
    for l in np.arange(0, len(moleculename)):
        toreturn['MaxConcentration_BCF'+moleculename[l]] = max_conc[l]
        toreturn['Accumulated_leaching'+moleculename[l]] = pest_acc[l]
        toreturn['MaxConcentration_BFF'+moleculename[l]] = max_conc_BFF[l]
    
    for i in np.arange(0, NoOfLimits):
        toreturn['nb_events_' + str(i) ]=nb_events[i]
        toreturn['longest_event_' + str(i) ]=longest_event[i]
        toreturn['shortest_interval_' + str(i) ]=MinInterval[i]
    
    return toreturn

