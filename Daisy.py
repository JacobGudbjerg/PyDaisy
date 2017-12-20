
import subprocess
import pandas as pd
import numpy as np 
import os
from enum import Enum

daisyexecutable = r'C:\Program Files\Daisy 5.49\bin\Daisy.exe'

class DaisyDlf(object):
    def __init__(self, DlfFileName):
        self.DlfFileName = DlfFileName
        self.Description=''
        self.HeaderItems=[]
        
        SectionIndex=0
        DateTimeIndex=3
        raw=[]
        TimeSteps = []
    
    #Read the file line by line.
        with open(self.DlfFileName, 'rU') as f:
            for line in f:
                line =line.rstrip()      
                if(SectionIndex == 0 and line): #Headline
                    self.HeadLine=line
                    SectionIndex=SectionIndex+1
                    continue
                if(SectionIndex==1 and line):#File Header section (Key, value)
                    if (line.startswith('--------------------')): #We have come to the start of the data section
                        SectionIndex=SectionIndex+1
                        continue
                    else:
                        split = line.split(':',1)
                        self.HeaderItems.append( (split[0], split[1].lstrip()) )
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
                    SectionIndex=SectionIndex+1
                    continue
                elif (SectionIndex == 3): #Column units. This may be an empty line 
                    self.ColumnUnits=line.split('\t')[DateTimeIndex:]
                    SectionIndex=SectionIndex+1
                    continue
                elif (SectionIndex == 4 and line): #Data
                    raw.append(map(float, line.split('\t')[DateTimeIndex:]))
                    timedata = list(map(int, line.split('\t')[0:DateTimeIndex]))
                    if DateTimeIndex == 3:
                        TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2]))
                    elif DateTimeIndex == 4:   
                        TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2],timedata[3]))
                    elif DateTimeIndex == 5:
                        TimeSteps.append(pd.datetime(timedata[0],timedata[1],timedata[2],timedata[3],timedata[4]))


        #Create a dataframe to hold the data 
        self.Data = pd.DataFrame(raw, columns=ColumnHeaders[DateTimeIndex:], index=TimeSteps)

    def getYCoordinates(self):
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
        #Check if we got coordinates
        if '@' in self.Data.columns[0]:
            #Check if we got 2 coordinates
            if '(' in self.Data.columns[0].split('@')[1]:
                l= list(set(map(lambda s: float(s.split('@')[1].strip().split()[1][:-1]), self.Data.columns)))
                l.sort()
                return l
        return



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
            elif (nextchar == ';'):
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
                    if (nextchar== ' ' or nextchar== '\t'):
                        if ( CurrentWord[len(CurrentWord) - 1]):
                            CurrentWord.append('')
                    else:
                        CurrentWord[len(CurrentWord) - 1] += nextchar

    def __getitem__(self, index):
        if type(index) is str:
            return next(c for c in self.Children if c.Keyword==index)
        else:
            return self.Children[index]

                    
    #Returns the value as integer, float or string   
    def getvalue(self, index=0):
        ToReturn =self.Words[index]
        try:
            ToReturn = int(ToReturn)
        except ValueError:
            try:
                ToReturn = float(ToReturn)
            except ValueError:
                pass
        finally:              
            return ToReturn
        
    #Sets the value
    def setvalue(self, value, index=0):
        while len(self.Words)<index+1:
            self.Words.append('')
        
        self.Words[index] = str(value)
    
    def write(self, sr, tab):
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
    def __init__(self, DaisyTimeEntry):
        self.DaisyTimeEntry =DaisyTimeEntry

    @property
    def time(self):
        c = self.DaisyTimeEntry        
        return pd.datetime(c.getvalue(0),c.getvalue(1),c.getvalue(2))

    @time.setter
    def time(self, time):
        c = self.DaisyTimeEntry
        c.setvalue(time.year,0)
        c.setvalue(time.month,1)
        c.setvalue(time.day,2)

      

class DaisyModel(object):
    def __init__(self, DaisyInputfile):
        self.DaisyInputfile =DaisyInputfile
        self.Input = DaisyEntry('',[])
        self.Output =[]
        with open(self.DaisyInputfile,'r') as f:
            self.Input.Read(f)
        self.starttime = DaisyTime(self.Input['defprogram']['time'])
        self.endtime = DaisyTime(self.Input['defprogram']['stop'])
            

    #Saves the file to a new filename
    def SaveAs(self, DaisyInputFile):
        self.DaisyInputfile = DaisyInputFile
        self.Save()
            
    #Saves the Dai-file. Comments will be lost    
    def Save(self):
        with open(self.DaisyInputfile, 'w') as f:
            self.Input.write(f, '')
    
    #Calls the Daisy executable and runs the simulation.
    #Remember to save first    
    def Run(self):
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call([daisyexecutable, self.DaisyInputfile], creationflags=CREATE_NO_WINDOW)

        
#    def LoadOutput(self):
#        indir = os.path.dirname(os.path.abspath(self.DaisyInputfile))
#        for root, dirs, filenames in os.walk(indir):
#            for f in filenames:
#               print(f)


class MultiDaisy(object):
    def __init__(self, DaisyInputfile):
        self.ChildModels =[]    
        self.ParentModel = DaisyModel(DaisyInputfile)
        Motherdir = os.path.dirname(self.ParentModel.DaisyInputfile)
        self.workdir = os.path.join(Motherdir, 'MultiDaisy')
        self.starttime = self.ParentModel.starttime.time
        self.endtime = self.ParentModel.endtime.time
        
    def Split(self, NumberOfModels, NumberOfSimYears, NumberOfWarmUpYears, overwrite=True):
        if overwrite:
            import shutil
            try:
                shutil.rmtree(self.workdir) #Delete the working directory
            except OSError:
                pass
        os.mkdir(self.workdir)
        for i in range(0,NumberOfModels):
            currentdir =os.path.join(self.workdir,str(i))
            os.mkdir(currentdir)
            self.ParentModel.starttime.time = self.starttime.replace(year=self.starttime.year +i*NumberOfSimYears) 
            self.ParentModel.endtime.time = self.starttime.replace(year=self.starttime.year +(i+1)*NumberOfSimYears+ NumberOfWarmUpYears)
            self.ParentModel.Input['defprogram']['activate_output']['after'].setvalue(self.starttime.year +i*NumberOfSimYears +NumberOfWarmUpYears)
            self.ParentModel.SaveAs(os.path.join(currentdir, 'DaisyModel.dai'))
        self.SetModelStatus(DaisyModelStatus.NotRun)
    
    def SetModelStatus(self, status):
        for root, dirs, filenames in os.walk(self.workdir):
            for d in dirs:
                for file in DaisyModelStatus:
                    try:
                        os.remove(os.path.join(root,d,file.name))
                    except OSError:
                        pass
                open(os.path.join(root,d, status.name), 'a').close()

    def CollectResults(self, DlfFileName):
        ToReturn=[]
        for root, dirs, filenames in os.walk(self.workdir):
            for d in dirs:
                if not os.path.isfile(os.path.join(root, d, DaisyModelStatus.NotRun.name)): #Do not take files that needs to be run
                    try:
                        ToReturn.append(DaisyDlf(os.path.join(root, d, DlfFileName)))
                    except:
                        pass
        return pd.concat( [x.Data for x in ToReturn]).sort_index()
            

class DaisyModelStatus(Enum):
    NotRun =1
    Running =2
    Done = 3

        

