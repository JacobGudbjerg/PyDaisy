import unittest
import sys
import numpy as np
sys.path.append(r'../')
from pydaisy.DaisyTools import *

class Test_DaisyToolsTest(unittest.TestCase):
    def test_vanGenuchten(self):
        vg = vanGenuchten();
        tf = vg.thetaFun(np.linspace(-10, 0, 50))


if __name__ == '__main__':
    unittest.main()
