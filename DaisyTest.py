import unittest
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

    def test_daisyDlfFile(self):
        """
        Test on a 2d dlf file with soil water content
        """
        dlf = DaisyDlf(r'.\TestData\soil_water_content.dlf')

    def test_multiDaisy(self):
        """
        Test of the Multi Daisy functionality.
        """
        m=MultiDaisy(r'.\TestData\DaisyModel.dai')
        m.Split(5,5,2)

if __name__ == '__main__':
    unittest.main()