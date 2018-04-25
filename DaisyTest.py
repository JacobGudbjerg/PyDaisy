import unittest
from Daisy import *


class Test_DaisyTest(unittest.TestCase):
    #Exercise01
    def test_daisyModel(self):
        d= DaisyModel(r'./TestData/Exercise01.dai')
        self.assertEqual(17, len(d.Input.Children))
        self.assertEqual(1993, d.starttime.time.year)

    #Taastrup weather file
    def test_daisyweatherfile(self):
        dwf = DaisyDlf(r'.\TestData\Taastrup6201.dwf')
        self.assertEqual(14435, len(dwf.Data.index))
        self.assertEqual('GlobRad', dwf.Data.columns[0])
        self.assertEqual('AirTemp', dwf.Data.columns[1])
        self.assertEqual('Precip', dwf.Data.columns[2])
        self.assertEqual('RefEvap', dwf.Data.columns[3])

    def test_daisyDlfFile(self):
        dlf = DaisyDlf(r'.\TestData\soil_water_content.dlf')

if __name__ == '__main__':
    unittest.main()
