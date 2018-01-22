# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:46:34 2017

@author: jpq949
"""

from multiprocessing import Pool
import time
import os
import subprocess
import sys
import platform


daisyexecutable = r'C:\Program Files\Daisy 5.54\bin\Daisy'

if platform.system()=='Linux':
    daisyexecutable = r'/home/projects/cu_10095/apps/daisy/obj/daisy'


DaisyFileName='DaisyModel.dai'
workdir=r'/home/projects/cu_10095/data/Git/PyDaisy/Bayer/WW_Late'
#workdir=r'/home/jgudbjerg/DaisyProjects/Bayer/Roerrendegaard/MultiDaisy'
NumberOfProcesses=32
MaxNumberOfDirectories=5000


#Runs a single daisy simulation and renames the "Running" file to "Done"
def RunSingle(workdir):
    print('Running ' + workdir)
    os.rename(os.path.join(workdir,"InQueue"), os.path.join(workdir,"Running"))
    if platform.system()=='Linux':
        sys.stdout.flush()
        subprocess.call([daisyexecutable, '-q', os.path.join(workdir, DaisyFileName), '-p', 'MySim'], cwd = workdir)
    else:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call([daisyexecutable, os.path.join(workdir,DaisyFileName)], creationflags=CREATE_NO_WINDOW)
    os.rename(os.path.join(workdir,"Running"), os.path.join(workdir,"Done"))
    modelrun=1
    return modelrun

#Runs all the daisy-simulations in the list of workdirs in parallel.
def RunMany(workdirs):
        print('Running ' + str (len(workdirs)) + ' directories on ' + str(NumberOfProcesses) + ' parallel processes')
        pp= Pool(NumberOfProcesses)
        pp.map(RunSingle, workdirs)
        pp.terminate
                

if __name__ == '__main__':
    start = time.time()
    workdirs=[]
    Continue=True
    while (Continue):
        Continue=False
        for root, dirs, filenames in os.walk(workdir):
            for d in dirs:
                try: #This will fail if the "NotRun" file is not there
                    workdir =os.path.join(root, d)
                    os.rename(os.path.join(workdir,"NotRun"),os.path.join(workdir,"InQueue"))
                    workdirs.append(workdir) #Add the directory to the list of directories that needs to be simulated
                    Continue=True
                except OSError: 
                    pass
                if len(workdirs)==MaxNumberOfDirectories:
                    RunMany(workdirs)
                    workdirs=[]
    RunMany(workdirs)
    
    print("Time used = {0:.5f} s".format(time.time() - start))
