import unittest
from Daisy import *


class Test_DaisyTest(unittest.TestCase):
    def test_A(self):
        d= DaisyModel(r'./TestData/Exercise01.dai')
        self.assertEqual(17, len(d.Input.Children))
        self.assertEqual(1993, d.starttime.time.year)

if __name__ == '__main__':
    unittest.main()
