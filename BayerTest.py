import unittest
from Daisy import DaisyDlf
from parExtract import BayerExtract

class Test_BayerTest(unittest.TestCase):
    def test_A(self):
        drain=DaisyDlf('Flak_SB_drain_data.dlf', r'.\TestData\daisy.log0.zip')
        d=DaisyDlf('Flak_SB_spray.dlf', r'.\TestData\daisy.log0.zip')
        b=BayerExtract('flak','barley')
        res = b.Extract(drain.Data, d)

if __name__ == '__main__':
    unittest.main()
