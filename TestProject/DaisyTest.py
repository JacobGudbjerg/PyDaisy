import unittest
import sys
from datetime import datetime

#Insert the path so it does not take the installed version.
sys.path.insert(0, r'../')
from pydaisy.Daisy import *


class Test_DaisyTest(unittest.TestCase):

    def test_try_cast_float(self):
        self.assertEqual(4.8, try_cast_float('4.8'))
        self.assertEqual(4, try_cast_number('4'))



    def test_daisyModel(self):
        """
        Test on reading the Exercise01.dai file distributed with Daisy
        """
        d= DaisyModel(r'./../TestData/Exercise01.dai')
        self.assertEqual(17, len(d.Input.Children))
        self.assertEqual(1993, d.starttime.time.year)

        self.assertEqual(3, len(d.Input['defhorizon']))

        d.save_as(r'./../TestData/Exercise01_saved.dai')
        d_saved = DaisyModel(r'./../TestData\Exercise01_saved.dai')
        self.assertEqual(d.endtime, d_saved.endtime)

        notthere = d.Input['NotThere']
        self.assertIsNone(notthere)

        self.assertTrue(d.daisy_installed())
        status = d.run()
        if  sys.version_info >= (3, 0):
            self.assertEqual(0, status.returncode)
        else:
            self.assertEqual(0, status)

        d.daisyexecutable='NotThere'
        self.assertFalse(d.daisy_installed())
        status = d.run()
        if  sys.version_info >= (3, 0):
            self.assertEqual(1, status.returncode)
        else:
            self.assertEqual(1, status)




        modelwitherror = DaisyModel(r'./../TestData/Exercise01_witherror.dai')
        status = modelwitherror.run()
        if  sys.version_info >= (3, 0):
            self.assertEqual(1, status.returncode)
        else:
            self.assertEqual(1, status)




        #test that we do not have to provide a path
        samedir = DaisyModel('Exercise01.dai')
        samedir.save()





    #Taastrup weather file
    def test_daisyweatherfile(self):
        """
        Test on Taastrup weather file distributed with Daisy
        """
        dwf = DaisyDlf(r'./../TestData\Taastrup6201.dwf')
        self.assertEqual(14435, len(dwf.Data.index))
        self.assertEqual('GlobRad', dwf.Data.columns[0])
        self.assertEqual('AirTemp', dwf.Data.columns[1])
        self.assertEqual('Precip', dwf.Data.columns[2])
        self.assertEqual('RefEvap', dwf.Data.columns[3])
        dwf.save(r'./../TestData\Taastrup6201_saved.dwf')

        dwf2 = DaisyDlf(r'./../TestData\Withdates.dwf')
        self.assertEqual(48, len(dwf2.Data.index))

        self.assertEqual(24, dwf2.get_index(datetime(1962,1,2)))
        self.assertEqual(0, dwf2.get_index(datetime(1962,1,1)))
        self.assertEqual(1, dwf2.get_index(datetime(1962,1,1,1)))
        dwf2.timestep=None
        self.assertEqual(24, dwf2.get_index(datetime(1962,1,2)))
        self.assertEqual(0, dwf2.get_index(datetime(1962,1,1)))
        self.assertEqual(1, dwf2.get_index(datetime(1962,1,1,1)))

    def test_daisyDlfFile(self):
        """
        Test on a 2d dlf file with soil water content
        """

        dlf_harvest = DaisyDlf(r'./../TestData\DailyP-harvest.dlf')


        dlf = DaisyDlf(r'./../TestData\soil_water_content.dlf')

        npdata = dlf.numpydata
        nldata = dlf.numpydata

        nldata[0][0]=11
        self.assertEqual(npdata[0][0], nldata[0][0])

        self.assertEqual(dlf.Data.values[0][0], nldata[0][0])


        dlz = DaisyDlf('Flak_SB_spray.dlf', r'./../TestData\daisy.log0.zip')
        self.assertEqual(7490, len(dlz.Data.index))

        dlz_sub = DaisyDlf('daisy.log1/subdir/Flak_SB_spray.dlf', r'./../TestData\daisy.log1.zip')
        self.assertEqual(7490, len(dlz_sub.Data.index))

        dlf_harvest = DaisyDlf(r'./../TestData\harvest.dlf')
        self.assertEqual(4.86207, dlf_harvest.Data['stem_DM'][0])
        self.assertEqual('M5_2D', dlf_harvest.Data['column'][0])

    

if __name__ == '__main__':
    unittest.main()
