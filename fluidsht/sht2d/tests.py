import unittest
from numpy.testing import assert_array_almost_equal
from fluidsht.sht2d.operators import OperatorsSphereHarmo2D


class TestOperators2D(unittest.TestCase):
    sht_class = "default"

    @classmethod
    def setUpClass(cls):
        cls.oper = oper = OperatorsSphereHarmo2D(sht=cls.sht_class)
        cls.arrays_spat = [oper.create_array_spat(1.) for i in range(2)]
        cls.arrays_sh = [oper.create_array_sh_random() for i in range(2)]

    def test_transform_vec_vsh(self):
        arrays_vec = self.arrays_spat
        arrays_vsh = self.oper.vsh_from_vec(*arrays_vec)
        arrays_vec2 = self.oper.vec_from_vsh(*arrays_vsh)
        for i in range(2):
            assert_array_almost_equal(arrays_vec[i], arrays_vec2[i])

if __name__ == "__main__":
    unittest.main()