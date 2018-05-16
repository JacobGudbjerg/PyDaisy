import unittest
from datetime import datetime

from Daisy import *


class Test_DaisyTest(unittest.TestCase):
    def test_daisyModel(self):
        """
        Test on reading the Exercise01.dai file distributed with Daisy
        """
        d= DaisyModel(r'./TestData/Exercise01.dai')
        self.assertEqual(17, len(d.Input.Children))
        self.assertEqual(1993, d.starttime.time.year)
        d.SaveAs(r'./TestData/Exercise01_saved.dai')
        d_saved = DaisyModel(r'.\TestData\Exercise01_saved.dai')
        self.assertEqual(d.endtime, d_saved.endtime)


    #Taastrup weather file
    def test_daisyweatherfile(self):
        """
        Test on Taastrup weather file distributed with Daisy
        """
        dwf = DaisyDlf(r'.\TestData\Taastrup6201.dwf')
        self.assertEqual(14435, len(dwf.Data.index))
        self.assertEqual('GlobRad', dwf.Data.columns[0])
        self.assertEqual('AirTemp', dwf.Data.columns[1])
        self.assertEqual('Precip', dwf.Data.columns[2])
        self.assertEqual('RefEvap', dwf.Data.columns[3])

        dwf2 = DaisyDlf(r'.\TestData\Withdates.dwf')
        self.assertEqual(48, len(dwf2.Data.index))

        self.assertEqual(24, dwf2.getIndex(datetime(1962,1,2)))
        self.assertEqual(0, dwf2.getIndex(datetime(1962,1,1)))
        self.assertEqual(1, dwf2.getIndex(datetime(1962,1,1,1)))
        dwf2.timestep=None
        self.assertEqual(24, dwf2.getIndex(datetime(1962,1,2)))
        self.assertEqual(0, dwf2.getIndex(datetime(1962,1,1)))
        self.assertEqual(1, dwf2.getIndex(datetime(1962,1,1,1)))

    def test_daisyDlfFile(self):
        """
        Test on a 2d dlf file with soil water content
        """
        dlf = DaisyDlf(r'.\TestData\soil_water_content.dlf')

        dlz = DaisyDlf('Flak_SB_spray.dlf', r'.\TestData\daisy.log0.zip')

        self.assertEqual(7490, len(dlz.Data.index))

        


    def test_multiDaisy(self):
        """
        Test of the Multi Daisy functionality.
        """
        m=MultiDaisy(r'.\TestData\DaisyModel.dai')
#        m.Split(5,5,2)
        workdirs=[]
        for d in m.DirLoop():
            workdirs.append(d)

          #  workdirs.append(d)
        self.assertEqual(5,len(workdirs))

        workdirs=[]
        for d in m.ResultsDirLoop():
            workdirs.append(d)

          #  workdirs.append(d)
        self.assertEqual(2,len(workdirs))
        res = m.ConcatenateResults('Flak_SB_spray.dlf', ['Temp 0-30','Temp 30-60'])

        k=0




if __name__ == '__main__':
    unittest.main()
