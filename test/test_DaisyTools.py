import unittest
import sys
import numpy as np
#Insert the path so it does not take the installed version.
sys.path.insert(0, r'../')
from pydaisy.DaisyTools import vanGenuchten

class Test_DaisyToolsTest(unittest.TestCase):
    def test_vanGenuchten(self):
        vg = vanGenuchten()

        viltingpoint = vg.thetaFun(-15.0)
        tf = vg.thetaFun(np.linspace(-15, 0, 50))


if __name__ == '__main__':
    unittest.main()
