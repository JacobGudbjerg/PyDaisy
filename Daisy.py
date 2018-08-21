"""
Various helper classes to read and manipulate Daisy input and output files.
"""
import subprocess
import platform
import sys
import pandas as pd
import csv
import os
import zipfile
from enum import Enum
from datetime import datetime, timedelta
from multiprocessing import Pool

daisyexecutable = r'C:\Program Files\Daisy 5.64\bin\Daisy.exe'
if platform.system()=='Linux':
    daisyexecutable = r'/home/projects/cu_10095/apps/daisy/obj/daisy'

class DaisyDlf(object):
    """
    Reads a Daisy .dlf- or .dwf-file.
    Can read directly from a zipped archive
    """
    def __init__(self, DlfFileName, ZipFileName=''):
        self.DlfFileName = DlfFileName
        self.Description=''
        self.HeaderItems={}
        self.__starttimeset=False
        filename, file_extension = os.path.splitext(DlfFileName)

        if ZipFileName!='':
            with zipfile.ZipFile(ZipFileName,'r') as z:
                with z.open(DlfFileName) as f:
                    self.__readfromfilestream(f, True)
        else:
            #Read the file line by line.
            with open(self.DlfFileName, 'rU') as f:
                self.__readfromfilestream(f)

    def __readfromfilestream(self, f, IsZip=False):
        """
        Read the data line by line. If it is from a zipped archived, data are read as bytes and converted to string using utf-8
        """
        SectionIndex=0
        DateTimeIndex=3
        raw=[]
        TimeSteps = []

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
                self.ColumnUnits=line.split('\t')[DateTimeIndex:]
                SectionIndex=SectionIndex+1
                continue
            elif (SectionIndex == 4 and line): #Data
                try:
                    splitted = line.split() #Splits on space and tab
                    if DateTimeIndex == 1: #Time is in a single column
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
                    raw.append(map(self.__converter , splitted[DateTimeIndex:]))
                except:
                    pass

        if len(raw)>0:
            #Create a dataframe to hold the data 
            self.Data = pd.DataFrame(raw, columns=ColumnHeaders[DateTimeIndex:], index=TimeSteps)
            #A trick to remove duplicate columns. Based on the header
            self.Data = self.Data.loc[:,~self.Data.columns.duplicated()]

    def __setStartTime(self):
        """
        Sets starttime and timestep if times are equidistant
        """
        self.startTime = self.Data.index[0]
        self.timestep = self.Data.index[1]- self.Data.index[0]

        for i in range(1, len(self.Data.index)):
            if self.timestep != self.Data.index[i]- self.Data.index[i-1]:
                self.timestep=None
                break
        self.__starttimeset =True

    def getIndex(self, Timestep):
        """
        Gets the index of a timestep. This method is fast if the timesteps are equidistant
        """
        if not self.__starttimeset:
            self.__setStartTime()

        if self.timestep != None:
            return int( (Timestep-self.startTime).total_seconds()/self.timestep.total_seconds())
        else:
            return self.Data.index.get_loc(Timestep)


    def getYCoordinates(self):
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

    def getXCoordinates(self):
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
        self.__setStartTime()
        self.HeaderItems['Begin']=self.Data.index[0].strftime('%Y-%m-%d')
        self.HeaderItems['End']=self.Data.index[len(self.Data.index)-1].strftime('%Y-%m-%d')
        self.HeaderItems['Timestep']= str(self.timestep.components.hours) + ' hours'
        
#        with codecs.open(FileName, encoding='utf-8', mode='w') as f:
        with open(FileName, 'w') as f:
            f.write(self.HeadLine)
            f.write('\n')
            #Write the header section
            for key,value in self.HeaderItems.items():
                f.write(key + ': ' + value + '\n')

            f.write('------------------------------------------------------------------------------\n')
            f.write('Year\tMonth\tDay')
            if(self.timestep==pd.to_timedelta(1, unit="H")):
                f.write('\tHour')
            
            for cu in self.Data.columns:
                f.write('\t')
                f.write(cu)
            f.write('\n')

            f.write('year\tmonth\tmday')
            if(self.timestep==pd.to_timedelta(1, unit="H")):
                f.write('\thour')

            for cu in self.ColumnUnits:
                f.write('\t')
                f.write(cu)
            f.write('\n')

            date_format='%Y\t%m\t%d'
            if(self.timestep==pd.to_timedelta(1, unit="H")):
                date_format='%Y\t%m\t%d\t%H'
            
            
            #Now write the weather data
            self.Data.to_csv(f, header=False, sep='\t', date_format=date_format, float_format='%.2f', encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar=" ")

    def __converter(self, value):
        try:
            return float(value)
        except:
            return value
                
class DaisyEntry(object):
    def __init__(self, Keyword, Words):
        self.Keyword = Keyword
        self.Words = Words
        self.AfterWords = []
        self.Children =[]
        self.Comment = []
        
    def __str__(self):
        return self.Keyword
    
    def Read(self, sr):
        keywordread = False
        self.Keyword = ''
        InCitation=False
        while True:
            nextchar = sr.read(1)
            if(not nextchar):
                break
            if (nextchar == '(' and not InCitation):
                child = DaisyEntry('',[])
                child.Read(sr)
                self.Children.append(child)
            elif (nextchar == ')' and not InCitation):
                return
            elif (nextchar == ';' and not InCitation):
                self.Comment.append( (len(self.Children), sr.readline()))
            elif (nextchar !='\n') :
                if(nextchar == '"'):
                    InCitation= not InCitation                               
                if (not keywordread):
                    if (nextchar!=' '):
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
                    else:
                        CurrentWord[len(CurrentWord) - 1] += nextchar

    def __getitem__(self, index):
        """
        Returns the first i'th item or the first item with that Keyword. Index should be string or integer
        """
        if type(index) is str:
            itere = list(c for c in self.Children if c.Keyword==index)
            if(len(itere)==1):
                return itere[0]
            return itere
        else:
            return self.Children[index]

                    
    def getvalue(self, index=0):
        """
        Returns the i'th value as integer, float or string. Default index value is 0
        """
        return self.__tryCast(self.Words[index])

    def __tryCast(self, ToReturn):
        try:
            ToReturn = int(ToReturn)
        except ValueError:
            try:
                ToReturn = float(ToReturn)
            except ValueError:
                pass
        finally:              
            return ToReturn


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
    
    def write(self, sr, tab):
        """
        Writes the entry to a stream. Recursive
        """
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
    def __init__(self, DaisyInputfile):
        self.DaisyInputfile =DaisyInputfile
        self.Input = DaisyEntry('',[])
        with open(self.DaisyInputfile,'r') as f:
            self.Input.Read(f)
        #now a small section that makes the start and end of the simulation visible    
        top=self.Input
        if any (c.Keyword=='defprogram' for c in top.Children):
            top=(top['defprogram'])
        if any (c.Keyword=='time' for c in top.Children):
            self.starttime = DaisyTime((top['time']))
        if any (c.Keyword=='stop' for c in top.Children):
            self.endtime = DaisyTime(top['stop'])
            

    
    def SaveAs(self, DaisyInputFile):
        """
        Saves the file to a new filename
        """
        self.DaisyInputfile = DaisyInputFile
        self.Save()
               
    def Save(self):
        """
        Saves the Dai-file. Comments will be lost
        """
        with open(self.DaisyInputfile, 'w') as f:
            self.Input.write(f, '')
    
    def Run(self):
        """
        Calls the Daisy executable and runs the simulation.
        Remember to save first    
        """
        if platform.system()=='Linux':
            sys.stdout.flush()
            subprocess.call([daisyexecutable, '-q', self.DaisyInputfile, '-p'], cwd = os.path.abspath(self.DaisyInputfile))
        else:
            CREATE_NO_WINDOW = 0x08000000
            subprocess.call([daisyexecutable, os.path.abspath(self.DaisyInputfile)], creationflags=CREATE_NO_WINDOW)

class DaisyModelStatus(Enum):
    NotRun =1
    Queue=2
    Running =3
    Done = 4
    
class MultiDaisy(object):
    """
    A class that helps running daisy in parallel.
    """
    def __init__(self, DaisyInputfile=''):
        if DaisyInputfile !='':
            self.ChildModels =[]    
            self.ParentModel = DaisyModel(DaisyInputfile)
            Motherdir = os.path.dirname(self.ParentModel.DaisyInputfile)
            self.workdir = os.path.join(Motherdir, 'MultiDaisy')
            self.starttime = self.ParentModel.starttime.time
            self.endtime = self.ParentModel.endtime.time
        
    def Split(self, NumberOfModels, NumberOfSimYears, NumberOfWarmUpYears, overwrite=True):
        """
        Splits a simulation into smaller time steps by creating new Daisy Input files in individual directories 
        """
        if overwrite:
            import shutil
            try:
                shutil.rmtree(self.workdir) #Delete the working directory
            except OSError:
                pass
        os.mkdir(self.__workdir)
        for i in range(0,NumberOfModels):
            currentdir =os.path.join(self.workdir,str(i))
            os.mkdir(currentdir)
            self.ParentModel.starttime.time = self.starttime.replace(year=self.starttime.year +i*NumberOfSimYears) 
            self.ParentModel.endtime.time = self.starttime.replace(year=self.starttime.year +(i+1)*NumberOfSimYears+ NumberOfWarmUpYears)
            self.ParentModel.Input['defprogram']['activate_output']['after'].setvalue(self.starttime.year +i*NumberOfSimYears +NumberOfWarmUpYears)
            self.ParentModel.SaveAs(os.path.join(currentdir, 'DaisyModel.dai'))

        self.SetModelStatus(DaisyModelStatus.NotRun)
    
    def SetModelStatus(self, status):
        """
        Set model status for all sub models
        """
        for root, dirs, filenames in os.walk(self.workdir):
            for d in dirs:
                for file in DaisyModelStatus:
                    try:
                        os.remove(os.path.join(root,d,file.name))
                    except OSError:
                        pass
                open(os.path.join(root,d, status.name), 'a').close()

    def ConcatenateResults(self, DlfFileName, Columns=[]):
        """
        Concatenates the results stored in DlfFileName in to one DaisyDlf
        """
        ToReturn=[]
        for dlf in self.ResultsDirLoop():
            if len(Columns)==0:
                ToReturn.append(DaisyDlf(os.path.join(dlf, DlfFileName)).Data)
            else:
                ToReturn.append(DaisyDlf(os.path.join(dlf, DlfFileName)).Data[Columns])
        temp= pd.concat( [x for x in ToReturn]).sort_index()
        #Remove duplicate entries on index
        return temp[~temp.index.duplicated(keep='first')]
    
    def DirLoop(self):
        """
        Iterates through all the multi daisy directories
        """
        for root, dirs, filenames in os.walk(self.workdir):
            for d in dirs:
                yield os.path.join(root, d)

    def ResultsDirLoop(self):
        """
        Iterates through all the multi daisy directories where the model is running og done
        """
        for d in self.DirLoop():
            if not os.path.isfile(os.path.join(d, DaisyModelStatus.NotRun.name)): #Do not take files that needs to be run
                yield d

    def RunSingle(self, FileNames):
        """
        Run a single simulation. This method should only be used by RunMany from this class.
        """        
        workdir = os.path.dirname(FileNames[0])

        try:
            if len(FileNames)>1:
                os.rename(os.path.join(workdir, FileNames[1]), os.path.join(workdir, FileNames[2]))
            dm = DaisyModel(FileNames[0])
            dm.Run()
            modelrun=1
            if len(FileNames)>1:
                os.rename(os.path.join(workdir,FileNames[2]), os.path.join(workdir, FileNames[3] ))
        except OSError: 
           modelrun=0
           pass    
        return modelrun

    def RunMany(self, DaisyFiles, NumberOfProcesses=6, Queue='', Running= DaisyModelStatus.Running.name, Done=DaisyModelStatus.Done.name):
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
        pp.map(self.RunSingle, FileNamesList)
        pp.terminate
    
    def RunSubFolders(self, MotherFolder, DaisyFileName, MaxBatchSize=5000, NumberOfProcesses=6, UseStatusFiles=False, recursive=False):
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
                        if UseStatusFiles: #This will fail if the "NotRun" file is not there
                            Notrun=os.path.join(workdir, DaisyModelStatus.NotRun.name)
                            InQueue =os.path.join(workdir,DaisyModelStatus.Queue.name)
                            os.rename(Notrun,InQueue)
                        if DaisyFile not in Alreadyrun and os.path.isfile(DaisyFile):
                            DaisyFiles.append(os.path.join(workdir, DaisyFileName)) #Add the directory to the list of directories that needs to be simulated
                    except OSError: 
                        pass
                    if len(DaisyFiles)==MaxBatchSize:
                        self.RunMany(DaisyFiles, NumberOfProcesses=NumberOfProcesses)
                        if not UseStatusFiles:
                            Alreadyrun.extend(DaisyFiles)
                        DaisyFiles=[]
                        Continue=True #After the simulation have finished look for more
        self.RunMany(DaisyFiles, NumberOfProcesses=NumberOfProcesses)


        

