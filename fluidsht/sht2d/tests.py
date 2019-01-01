import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
from fluidsht.sht2d.operators import OperatorsSphereHarmo2D


class TestOperators2D(unittest.TestCase):
    sht_class = "default"

    @classmethod
    def setUpClass(cls):
        cls.oper = oper = OperatorsSphereHarmo2D(sht=cls.sht_class)
        cls.arrays_spat = [oper.create_array_spat(1.) for i in range(2)]
        cls.arrays_sh = [oper.create_array_sh_random() for i in range(2)]
        for array in cls.arrays_sh:
            array[np.logical_not(oper.where_l2_idx_positive)] = 0.0

    # def test_transform_vec_vsh(self):
    #     arrays_vec = self.arrays_spat
    #     arrays_vsh = self.oper.vsh_from_vec(*arrays_vec)
    #     arrays_vec2 = self.oper.vec_from_vsh(*arrays_vsh)
    #     for i in range(2):
    #         assert_array_almost_equal(arrays_vec[i], arrays_vec2[i])

    def test_transform_vsh_divrotsh(self):
        arrays_vsh = self.arrays_sh
        arrays_divrotsh = self.oper.divrotsh_from_vsh(*arrays_vsh)
        arrays_vsh2 = self.oper.vsh_from_divrotsh(*arrays_divrotsh)
        for i in range(2):
            assert_array_almost_equal(arrays_vsh[i], arrays_vsh2[i], decimal=8)

if __name__ == "__main__":
    unittest.main()