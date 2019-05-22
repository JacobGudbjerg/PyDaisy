"""
Various helper classes to read and manipulate Daisy input and output files.
"""
from __future__ import print_function
from __future__ import division
import subprocess
import platform
import sys
import pandas as pd
import numpy as np
import csv
import errno
import os
import zipfile
import copy
from enum import Enum
from datetime import datetime, timedelta
from multiprocessing import Pool, Value
import uuid


def try_cast_number(value):
    """
    Tries to convert to an int, then float and otherwise just returns the value
    """
    try:
        return int(value)
    except ValueError:
        return try_cast_float(value)

def try_cast_float(value):
    """
    Tries to convert to a float. Otherwise just returns the value
    """
    try:
        return float(value)
    except ValueError:
        return value

def is_number(value):
    """
    returns true if value can be cast to a float otherwise false
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if directory!='':
        if not os.path.exists(directory):
            os.makedirs(directory)



class FixedTimeStepIndexer(object):

    def __init__(self, time_steps):
        self.time_steps = time_steps
        self.__starttimeset =False
        self._timestep=None

    def __setStartTime(self):
        """
        Sets starttime and timestep if times are equidistant
        """
        if isinstance(self.time_steps[0], pd.Period):
            self.startTime = self.time_steps[0].start_time.to_pydatetime()
            self._timestep = self.time_steps[1].start_time.to_pydatetime() - self.startTime
        else:
            self.startTime = self.time_steps[0]
            self._timestep = self.time_steps[1]- self.time_steps[0]
        self.__starttimeset =True

    def get_index(self, Timestep):
        """
        Gets the index of a timestep. This method is fast if the timesteps are equidistant
        """
        if not self.__starttimeset:
            self.__setStartTime()

        if self.timestep != None:
            return int(round( (Timestep-self.startTime).total_seconds()/self.timestep.total_seconds(),0))
        else:
            return self.time_steps.get_loc(Timestep)

    @property 
    def timestep(self):
        if not self.__starttimeset:
            self.__setStartTime()
        return self._timestep 


    def validate(self):
        """
        Validates that all the time steps have the same distance
        """
        for i in range(1, len(self.time_steps)):
            if self.timestep != self.time_steps[i]- self.time_steps[i-1]:
                self._timestep = None
                return False
        return True

class DaisyDlf(object):
    """
    Reads a Daisy .dlf- or .dwf-file.
    Can read directly from a zipped archive
    """
    def __init__(self, DlfFileName, ZipFileName='', FixedTimeStep=False):
        self.DlfFileName = DlfFileName
        self.Description=''
        self.HeaderItems={}
        self.__numpydata = np.array([])
        self.__tab_and_space_delimiter=True
        self.Data = pd.DataFrame()
        filename, file_extension = os.path.splitext(DlfFileName)

        if ZipFileName!='':
            with zipfile.ZipFile(ZipFileName,'r') as z:
                with z.open(DlfFileName) as f:
                    self.__readfromfilestream(f, True, FixedTimeStep=FixedTimeStep)
        else:
            #Read the file line by line.
            with open(self.DlfFileName) as f:
                self.__readfromfilestream(f, FixedTimeStep=FixedTimeStep)

    def __readfromfilestream(self, f, IsZip=False, FixedTimeStep=False):
        """
        Read the data line by line. If it is from a zipped archived, data are read as bytes and converted to string using utf-8
        """
        SectionIndex=0
        DateTimeIndex=3
        raw=[]
        TimeSteps = []
        FirstEntry = True
        DataIndex=0

        #Loop the data line by line
        for line in f:
            if IsZip:
                line=line.decode("utf-8") #Decode byte arrays from zipped files
            line =line.rstrip()      
            if(SectionIndex == 0 and line): #Headline
                self.HeadLine=line
                SectionIndex=SectionIndex+1
                continue
            elif(SectionIndex==1 and line):#File Header section (Key, value)
                if (line.startswith('--------')): #We have come to the start of the data section
                    SectionIndex=SectionIndex+1
                    continue
                elif (line.startswith('#')):
                        continue                    
                else:
                    split = line.split(':',1)
                    self.HeaderItems[split[0]] = split[1].lstrip()
                    if(split[0]=='LOG'):
                        self.Description += split[1]
                    elif (split[0]=='SIMFILE'):
                        self.SimFile = split[1].strip()
            elif SectionIndex == 2: #Column names
                ColumnHeaders=line.split('\t')
                if 'minute' in ColumnHeaders:
                    DateTimeIndex=5
                elif 'hour' in ColumnHeaders:
                    DateTimeIndex=4
                elif 'Date' in ColumnHeaders:
                    DateTimeIndex=1
                SectionIndex=SectionIndex+1
                continue
            elif (SectionIndex == 3): #Column units. This may be an empty line 
                self.column_units= dict(zip(ColumnHeaders[DateTimeIndex:], line.split('\t')[DateTimeIndex:]))
                SectionIndex=SectionIndex+1
                continue
            elif (SectionIndex == 4 and line): #Data
                try:
                    #Guess the delimiter based on the number of ColumnHeaders.
                    if FirstEntry:
                        if len(line.split()) != len(ColumnHeaders):
                            self.__tab_and_space_delimiter = False
                    if self.__tab_and_space_delimiter:
                        splitted = line.split() #Splits on space and tab
                    else:
                        splitted = line.split('\t') #Splits on tab. This is necessary if one of the strings has spaces in it

#                    if len(splitted)==len(ColumnHeaders): #We need to make sure the line is complete
                    if len(splitted)>DateTimeIndex: #We need to make sure the line is complete
                        if DateTimeIndex == 1: #Time is in a single column
                            if FixedTimeStep:
                                if DataIndex==0:
                                    self.startTime = datetime.strptime(splitted[0], '%Y-%m-%dT%H:%M:%S')
                                    TimeSteps.append(self.startTime)
                                elif DataIndex==1:
                                    TimeSteps.append(datetime.strptime(splitted[0], '%Y-%m-%dT%H:%M:%S'))
                                    self.timestep = TimeSteps[1]- TimeSteps[0]
                                    self.__starttimeset=True
#                                else:
#                                    TimeSteps.append(self.startTime + self.timestep*DataIndex)
                            else:
                                TimeSteps.append(datetime.strptime(splitted[0], '%Y-%m-%dT%H:%M:%S'))
                        else: #Time is in multiple columns
                            timedata = list(map(int, splitted[0:DateTimeIndex])) #First columns are time data
                            if DateTimeIndex == 3:
                                TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2]))
                            elif DateTimeIndex == 4:   
                                TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2],timedata[3]))
                            elif DateTimeIndex == 5:
                                TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2],timedata[3],timedata[4]))
                        #Now data        
                        raw.append(map(try_cast_float , splitted[DateTimeIndex:]))
                        DataIndex+=1
                except:
                    pass

        if len(raw)>0:
            #Create a dataframe to hold the data 
           if FixedTimeStep:
               self.Data = pd.DataFrame(raw,  index=pd.period_range(self.startTime, self.startTime + self.timestep*(len(raw)-1), freq= 'h'))
           else:
               self.Data = pd.DataFrame(raw,  index=TimeSteps)
           self.Data.columns=ColumnHeaders[DateTimeIndex:DateTimeIndex+len(self.Data.columns)]
            #A trick to remove duplicate columns. Based on the header
           self.Data = self.Data.loc[:,~self.Data.columns.duplicated()]
           self._time_indexer = FixedTimeStepIndexer(self.Data.index)


    def get_index(self, Timestep):
        """
        Gets the index of a timestep. This method is fast if the timesteps are equidistant
        """
        return self._time_indexer.get_index(Timestep)


    @property
    def numpydata(self):
        """
        Returns the data as a numpy data set.
        """
        if self.__numpydata.size==0:
            self.__numpydata = self.Data.values
        return self.__numpydata


    def get_y_coordinates(self):
        """
        Returns the y-coordinates if it is a 2d file
        """
        #Check if we got coordinates
        if '@' in self.Data.columns[0]:
            #Check if we got 2 coordinates
            if '(' in self.Data.columns[0].split('@')[1]:
                l= list(set(map(lambda s: float(s.split('@')[1].strip().split()[0][1:]), self.Data.columns)))
                l.sort(reverse=True)
                return l
            else:
                return list(map(lambda s: float(s.split('@')[1]), self.Data.columns))
        return

    def get_x_coordinates(self):
        """
        Returns the x-coordinates if there are any. Splits on "@"
        """

        #Check if we got coordinates
        if '@' in self.Data.columns[0]:
            #Check if we got 2 coordinates
            if '(' in self.Data.columns[0].split('@')[1]:
                l= list(set(map(lambda s: float(s.split('@')[1].strip().split()[1][:-1]), self.Data.columns)))
                l.sort()
                return l
        return
    

    def save(self, FileName):
        """
        Writes the data to a file. Use this method to write Daisy Weather files
        Only writes daily and hourly values
        """        
        #Make sure timestep is set
        self.HeaderItems['Begin']=self.Data.index[0].strftime('%Y-%m-%d')
        self.HeaderItems['End']=self.Data.index[len(self.Data.index)-1].strftime('%Y-%m-%d')
        self.HeaderItems['Timestep']= str(self._time_indexer.timestep.total_seconds () / 3600.0) + ' hours'
        
#        with codecs.open(FileName, encoding='utf-8', mode='w') as f:
        with open(FileName, 'w') as f:
            f.write(self.HeadLine)
            f.write('\n')
            #Write the header section
            for key,value in self.HeaderItems.items():
                f.write(key + ': ' + value + '\n')

            f.write('------------------------------------------------------------------------------\n')
            f.write('Year\tMonth\tDay')
            if(self._time_indexer.timestep==pd.to_timedelta(1, unit="H")):
                f.write('\tHour')
            
            for cu in self.Data.columns:
                f.write('\t')
                f.write(cu)
            f.write('\n')

            f.write('year\tmonth\tmday')
            if(self._time_indexer.timestep==pd.to_timedelta(1, unit="H")):
                f.write('\thour')

            for k,v in self.column_units.items():
                f.write('\t')
                f.write(v)
            f.write('\n')

            date_format='%Y\t%m\t%d'
            if(self._time_indexer.timestep==pd.to_timedelta(1, unit="H")):
                date_format='%Y\t%m\t%d\t%H'
            
            
            #Now write the weather data
            self.Data.to_csv(f, header=False, sep='\t', date_format=date_format, float_format='%.2f', encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar=" ")


                

            
class DaisyEntry(object):
    def __init__(self, Keyword, Words):
        self.Keyword = Keyword
        self.Words = Words
        self.AfterWords = []
        self.Children =[]
        self.Comment = []
        self.keyword_description=''
        
    def __str__(self):
        return self.Keyword

    def __repr__(self):
        return 'DaisyEntry ('+ self.Keyword +')'
    
    def read(self, sr):
        keywordread = False
        self.Keyword = ''
        InCitation=False
        while True:
            nextchar = sr.read(1)
            if(not nextchar):
                break
            if (nextchar == '(' and not InCitation):
                child = DaisyEntry('',[])
                child.read(sr)
                self.Children.append(child)
            elif (nextchar == ')' and not InCitation):
                return
            elif (nextchar == ';' and not InCitation):
                self.Comment.append( (len(self.Children), sr.readline()))
            elif (nextchar !='\n') :
                if(nextchar == '"'):
                    InCitation= not InCitation                               
                if (not keywordread):
                    if (nextchar!=' ' and nextchar != '\t'):
                        self.Keyword += nextchar
                    else:
                         keywordread = True
                         self.Words.append('')              
                else:
                    if(len(self.Children)==0):
                        CurrentWord =self.Words
                    else:
                        CurrentWord =self.AfterWords
                        if(len(CurrentWord)==0):
                            CurrentWord.append('')
                    if ((nextchar== ' ' or nextchar== '\t') and not InCitation):
                        if ( CurrentWord[len(CurrentWord) - 1]):
                            CurrentWord.append('')
                    elif(nextchar== '[' and is_number( CurrentWord[len(CurrentWord) - 1])):
                            CurrentWord.append('[')
                    else:
                        CurrentWord[len(CurrentWord) - 1] += nextchar

    def __getitem__(self, index):
        """
        Returns the first i'th item or the first item with that Keyword. Index should be string or integer
        """
        if type(index) is str:
            itere = list(c for c in self.Children if c.Keyword==index)
            if len(itere)==0:
                return None
            elif len(itere)==1:
                return itere[0]
            else:
                return itere
        else:
            return self.Children[index]

                    
    def getvalue(self, index=0):
        """
        Returns the i'th value as integer, float or string. Default index value is 0
        """
        return try_cast_number(self.Words[index])


    def getvalues(self):
        """
        Returns a list with all values. Integer, float or string
        """
        for w in self.Words:
            yield self.__tryCast(w)

        
    def setvalue(self, value, index=0):
        """
        sets the i'th value. Default index value is 0
        """
        while len(self.Words)<index+1:
            self.Words.append('')
        
        self.Words[index] = str(value)

    def copy(self):
        """
        Returns a deep copy of this entry. This should be used when you want to insert this entry in another entry
        """
        return copy.deepcopy(self)
    
    def write(self, sr, tab):
        """
        Writes the entry to a stream. Recursive
        """
        if self.keyword_description != '':
            sr.write(';' +         self.keyword_description + '\n') 
            
        sr.write(self.Keyword)
        for w in self.Words:
            sr.write(' ')
            sr.write(w)
        
        tab =tab + "  "
        for c in self.Children:
            sr.write('\n' +tab)
            sr.write('(')
            c.write(sr, tab)
            sr.write(')')

        #Now write the words that appear after the children
        for w in self.AfterWords:
            sr.write(' ')
            sr.write(w)

class DaisyTime(object):
    """
    class wrapping a Daisy time
    """
    def __init__(self, DaisyTimeEntry):
        self.DaisyTimeEntry =DaisyTimeEntry
    
    def __str__(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    def __eq__(self, Other):
        """
        Two DaisyTimes are equal if the underlying timesteps are equal
        """
        return isinstance(Other, DaisyTime) and self.time.__eq__(Other.time)

    @property
    def time(self):
        c = self.DaisyTimeEntry
        time = pd.datetime(c.getvalue(0),c.getvalue(1),c.getvalue(2))
        if(len(c.Words)>3):
            time+=pd.to_timedelta(c.getvalue(3), unit='h')
        if(len(c.Words)>4):
            time.minute=c.getvalue(4)
        if(len(c.Words)>5):
            time.second=c.getvalue(5)

        return time

    @time.setter
    def time(self, time):
        c = self.DaisyTimeEntry
        c.setvalue(time.year,0)
        c.setvalue(time.month,1)
        c.setvalue(time.day,2)
        if(time.hour != 0 or time.minute !=0 or time.second!=0):
            c.setvalue(time.hour, 3)
        if(time.minute !=0 or time.second!=0):
            c.setvalue(time.minute, 4)
        if(time.second!=0):
            c.setvalue(time.second, 5)
     
class DaisyModel(object):
    """
    A class that reads a daisy input file (.dai-file)
    """
    path_to_daisy_executable = r'C:\Program Files (x86)\Daisy 5.83\bin\Daisy.exe'


    def __init__(self, DaisyInputfile):
        self._input=None
        self._starttime=None
        self._endtime=None
        self.DaisyInputfile =DaisyInputfile


    @property 
    def Input(self): 
        if not self._input: 
            self._input = DaisyEntry('',[])
            with open(self.DaisyInputfile,'r') as f:
                self._input.read(f)
        return self._input
        
    @property
    def starttime(self):
        if not self._starttime:
            self.__readtime()
        return self._starttime

    @property
    def endtime(self):
        if not self._endtime:
            self.__readtime()
        return self._endtime

    def __readtime(self):
        """
        #now a small section that makes the start and end of the simulation visible    
        """
        top=self.Input
        if any (c.Keyword=='defprogram' for c in top.Children):
            top=(top['defprogram'])
        if any (c.Keyword=='time' for c in top.Children):
            self._starttime = DaisyTime((top['time']))
        if any (c.Keyword=='stop' for c in top.Children):
            self._endtime = DaisyTime(top['stop'])



    def save_as(self, DaisyInputFile):
        """
        Saves the file to a new filename
        """
        self.DaisyInputfile = DaisyInputFile
        self.save()
               
    def save(self):
        """
        Saves the Dai-file. Comments will be lost
        """
        ensure_dir(self.DaisyInputfile)
        with open(self.DaisyInputfile, 'w') as f:
            self.Input.write(f, '')

    def copy(self):
        """
        Returns a deep copy of this entry. This should be used when you want to insert this entry in another entry
        """
        return copy.deepcopy(self)    


    def daisy_installed(self):
        """
        Returns true if it can find the daisy executable
        """
        return os.path.isfile(DaisyModel.path_to_daisy_executable)



    def run(self, timeout=None):
        """
        Calls the Daisy executable and runs the simulation.
        Remember to save first
        timeout is in seconds
        """
        if not self.daisy_installed():
            raise Exception('Daisy could not be found at: ' + self.path_to_daisy_executable)

        try:
            if platform.system()=='Linux':
                sys.stdout.flush()
                return subprocess.call([DaisyModel.path_to_daisy_executable, '-q', self.DaisyInputfile, '-p', self.Input['run'].getvalue().replace('"','')], timeout=timeout, cwd = os.path.dirname(self.DaisyInputfile))
            else:
                if  sys.version_info >= (3, 0):
                    return subprocess.run([DaisyModel.path_to_daisy_executable, os.path.split(self.DaisyInputfile)[1]], timeout=timeout, cwd= os.path.dirname(self.DaisyInputfile), shell=False)
                else:
                    return subprocess.call([DaisyModel.path_to_daisy_executable, os.path.split(self.DaisyInputfile)[1]], timeout=timeout, cwd= os.path.dirname(self.DaisyInputfile), shell=False)
        except subprocess.TimeoutExpired:
            return -1


class DaisyModelStatus(Enum):
    NotRun =1
    Queue=2
    Running =3
    Done = 4
    Failed = 5
    

def run_single(FileNames):
    """
    Run a single simulation. This method should only be used by the run_many() function
    """        
    workdir = os.path.dirname(FileNames[0])

    uniquelogfilename = os.path.join(workdir, 'run_' + str(uuid.uuid4()) + '.log')
    with open(uniquelogfilename, "w") as text_file:
        text_file.write(str(datetime.now()) + ': model run started\n')

    try:
        if len(FileNames)>1:
            f1 = os.path.join(workdir, FileNames[1])
            f2 = os.path.join(workdir, FileNames[2])
            os.rename(f1, f2)
        dm = DaisyModel(FileNames[0])
        if not dm.daisy_installed():
            with open(uniquelogfilename, "w") as text_file:
                text_file.write(str(datetime.now()) + ': Could not find Daisy at: '+ DaisyModel.path_to_daisy_executable + '\n')

        modelrun=dm.run()
        with open(uniquelogfilename, "a") as text_file:
            text_file.write(str(datetime.now()) + ': model run finished with return code: ' + str(modelrun)+'\n')
        if len(FileNames)>1:
            if modelrun==0:
                os.rename(f2, os.path.join(workdir, FileNames[3] ))
            else:
                os.rename(f2, os.path.join(workdir, DaisyModelStatus.Failed.name ))
    except: 
        if len(FileNames)>1:
            os.rename(f2, os.path.join(workdir,  DaisyModelStatus.Failed.name ))
        modelrun=1
        with open(uniquelogfilename, "a") as text_file:
            text_file.write(str(datetime.now()) + ': model run failed\n')
        pass    
    return modelrun

def run_many(DaisyFiles, NumberOfProcesses=6, Queue='', Running= DaisyModelStatus.Running.name, Done=DaisyModelStatus.Done.name):
    """
    Runs all the daisy-simulations in the list of Daisyfiles in parallel. Can use renaming of files to indicate status
    """
    print('Running ' + str (len(DaisyFiles)) + ' directories on ' + str(NumberOfProcesses) + ' parallel processes')
    
    pp= Pool(NumberOfProcesses)
        
    FileNamesList=[]
    for f in DaisyFiles:
        if Queue!='':
            FileNamesList.append([f, Queue, Running, Done])
        else:
            FileNamesList.append([f])
    pp.map(run_single, FileNamesList)
    pp.terminate()

def run_sub_folders2(MotherFolder, DaisyFileName, DaisyExecutabl, NumberOfProcesses=6, recursive=False):
    """
    Runs all the Daisy simulations found below the MotherFolder
    """
    pp = Pool(NumberOfProcesses)
    input=[]
    for i in range(NumberOfProcesses):
        input.append( (MotherFolder, DaisyFileName, DaisyExecutabl, i, recursive, None)  )
    pp.starmap(run_single2, input)
    pp.terminate()


def set_model_run_status(workdir, status):
    for file in DaisyModelStatus:
        try:
            os.remove(os.path.join(workdir,file.name))
        except OSError:
            pass
    open(os.path.join(workdir, status.name), 'a').close()



def run_single2(MotherFolder, DaisyFileName, DaisyExecutablePath, delay = 0, recursive=False, timeout=None):
    """
    Runs a single simulation and continues until there are no more with status NotRun. The delay is used only once and should be set to avoid race conditions.
    """
    Continue=True
    import time
    time.sleep(delay)
    
    while (Continue):
        Continue=False
        if recursive:
            items = os.walk(MotherFolder)
        else:
            items = [next(os.walk(MotherFolder))]

        for root, dirs, filenames in items:
            for d in dirs:
                try: 
                    workdir = os.path.join(root, d)
                    DaisyFile = os.path.join(workdir, DaisyFileName)
                    Notrun = os.path.join(workdir, DaisyModelStatus.NotRun.name)
                    Running = os.path.join(workdir, DaisyModelStatus.Running.name)
                    #This will fail if the "NotRun" file is not there
                    os.rename(Notrun, Running)

                    uniquelogfilename = os.path.join(workdir, 'run_' + str(uuid.uuid4()) + '.log')
                    with open(uniquelogfilename, "w") as text_file:
                        text_file.write(str(datetime.now()) + ': model run started\n')

                    DaisyModel.path_to_daisy_executable = DaisyExecutablePath
                    dm = DaisyModel(DaisyFile)
                    if not dm.daisy_installed():
                        with open(uniquelogfilename, "a") as text_file:
                            text_file.write(str(datetime.now()) + ': Could not find Daisy at: '+ DaisyModel.path_to_daisy_executable + '\n')
                    modelrun=dm.run(timeout)
                    with open(uniquelogfilename, "a") as text_file:
                        text_file.write(str(datetime.now()) + ': model run finished with return code: ' + str(modelrun)+'\n')
                    if modelrun.returncode==0:
                        os.rename(Running, os.path.join(workdir, DaisyModelStatus.Done.name ))
                    else:
                        with open(uniquelogfilename, "a") as text_file:
                            text_file.write(str(datetime.now()) + ': model run failed\n')
                        os.rename(Running, os.path.join(workdir, DaisyModelStatus.Failed.name))
                    Continue=True #After the simulation have finished loop all dirs once more
                except OSError: 
                    pass
    
def run_sub_folders(MotherFolder, DaisyFileName, MaxBatchSize=5000, NumberOfProcesses=6, UseStatusFiles=False, recursive=False):
    """
    Runs all the Daisy simulations found below the MotherFolder
    """

    DaisyFiles=[]
    Continue=True
    Alreadyrun=[]
           
    while (Continue):
        Continue=False
        if recursive:
            items = os.walk(MotherFolder)
        else:
            items = [next(os.walk(MotherFolder))]

        for root, dirs, filenames in items:
            for d in dirs:
                try: 
                    workdir = os.path.join(root, d)
                    DaisyFile = os.path.join(workdir, DaisyFileName)
                    if UseStatusFiles: 
                        Notrun = os.path.join(workdir, DaisyModelStatus.NotRun.name)
                        InQueue = os.path.join(workdir, DaisyModelStatus.Queue.name)
                        #This will fail if the "NotRun" file is not there
                        os.rename(Notrun, InQueue)
                    if DaisyFile not in Alreadyrun and os.path.isfile(DaisyFile):
                        DaisyFiles.append(os.path.join(workdir, DaisyFileName)) #Add the directory to the list of directories that needs to be simulated
                except OSError: 
                    pass
                if len(DaisyFiles)==MaxBatchSize:
                    if UseStatusFiles:
                        run_many(DaisyFiles, NumberOfProcesses=NumberOfProcesses, Queue = DaisyModelStatus.Queue.name)
                    else:
                        run_many(DaisyFiles, NumberOfProcesses=NumberOfProcesses)
                        Alreadyrun.extend(DaisyFiles)
                    DaisyFiles=[]
                    Continue=True #After the simulation have finished look for more
    if UseStatusFiles:
        run_many(DaisyFiles, NumberOfProcesses=NumberOfProcesses, Queue = DaisyModelStatus.Queue.name)
    else:
        run_many(DaisyFiles, NumberOfProcesses=NumberOfProcesses)

