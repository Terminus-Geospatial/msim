
#  Python Standard Libraries
import unittest

#  Numerical Python
import numpy as np

#  Terminus Libraries
import tmns.geo.coordinate as crd

class geographic_tests(unittest.TestCase):

    def test_ecf_geographic(self):

        lla_coord = np.array( [[-104], [39], [1800]], dtype = np.float64 )

        ecf_coord = crd.geographic_to_ecf( lla_coord ).flatten()

        lla_out = crd.ecf_to_geographic( ecf_coord ).flatten()

        self.assertAlmostEqual( lla_coord[0], lla_out[0], 0.001 )
        self.assertAlmostEqual( lla_coord[1], lla_out[1], 0.001 )
        self.assertAlmostEqual( lla_coord[2], lla_out[2], 0.001 )
