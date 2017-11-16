
import subprocess
import pandas as pd

daisyexecutable = 'C:/Program Files/Daisy 5.37/bin/Daisy.exe'

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
                        TimeSteps.append(pd.Timestamp(timedata[0],timedata[1],timedata[2]))
                    elif DateTimeIndex == 4:   
                        TimeSteps.append(pd.Timestamp(timedata[0],timedata[1],timedata[2],timedata[3]))
                    elif DateTimeIndex == 5:
                        TimeSteps.append(pd.Timestamp(timedata[0],timedata[1],timedata[2],timedata[3],timedata[4]))


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
        except:
            try:
                ToReturn = float(ToReturn)
            except:
                ToReturn2=1
        finally:              
            return ToReturn
        
    #Sets the value
    def setvalue(self, value, index=0):
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
      

class DaisyModel(object):
    def __init__(self, DaisyInputfile):
        self.DaisyInputfile =DaisyInputfile
        self.Input = DaisyEntry('',[])
        self.Output =[]
        with open(self.DaisyInputfile,'r') as f:
            self.Input.Read(f)
    
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
        subprocess.call([daisyexecutable, self.DaisyInputfile])
        
#    def LoadOutput(self):
#        indir = os.path.dirname(os.path.abspath(self.DaisyInputfile))
#        for root, dirs, filenames in os.walk(indir):
#            for f in filenames:
#               print(f)



