import unittest
from datetime import datetime

from pydaisy.Daisy import *


class Test_DaisyTest(unittest.TestCase):
    def test_daisyModel(self):
        """
        Test on reading the Exercise01.dai file distributed with Daisy
        """
        d= DaisyModel(r'./../TestData/Exercise01.dai')
        self.assertEqual(17, len(d.Input.Children))
        self.assertEqual(1993, d.starttime.time.year)
        d.save_as(r'./../TestData/Exercise01_saved.dai')
        d_saved = DaisyModel(r'./../TestData\Exercise01_saved.dai')
        self.assertEqual(d.endtime, d_saved.endtime)

        status = d.run()
        self.assertEqual(0, status)
        modelwitherror = DaisyModel(r'./../TestData/Exercise01_witherror.dai')
        status = modelwitherror.run()
        self.assertEqual(1, status)



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
        dlf = DaisyDlf(r'./../TestData\soil_water_content.dlf')

        dlz = DaisyDlf('Flak_SB_spray.dlf', r'./../TestData\daisy.log0.zip')

        self.assertEqual(7490, len(dlz.Data.index))

        dlz = DaisyDlf(r'./../TestData\Ror_WW_surface_chemicals.dlf')
        
    def test_splitDaisy(self):
        """
        Test of the Multi Daisy functionality.
        """
        m=SplitDaisy(r'./../TestData\DaisyModel.dai')
        m.Split(5,5,2, overwrite=False)

        RunSubFolders(m.workdir, 'DaisyModel.dai', UseStatusFiles=True)


        workdirs=list(m.DirLoop())
        self.assertEqual(5,len(workdirs))

        #No models have run.
        workdirs=list(m.ResultsDirLoop())
        self.assertEqual(0,len(workdirs))

        res = m.ConcatenateResults('Flak_SB_spray.dlf')
        self.assertIsNone(res);

        m.SetModelStatus(DaisyModelStatus.Done)

        res = m.ConcatenateResults('Flak_SB_spray.dlf')
        self.assertIsNotNone(res)


    def test_multiDaisy(self):

        m=SplitDaisy(r'./../TestData\DaisyModel.dai')
        m.SetModelStatus(DaisyModelStatus.NotRun)

        RunSingle([r'./../TestData\MultiDaisy\0\DaisyModel.dai', DaisyModelStatus.NotRun.name, DaisyModelStatus.Queue.name, DaisyModelStatus.Done.name ])


        RunSubFolders(r'./../TestData\MultiDaisy', 'DaisyModel.dai')

        RunSubFolders(r'./../TestData\MultiDaisy', 'DaisyModel.dai', UseStatusFiles=True)
        
        RunSubFolders(r'./../TestData\MultiDaisy', 'DaisyModel.dai', UseStatusFiles=True)




if __name__ == '__main__':
    unittest.main()
