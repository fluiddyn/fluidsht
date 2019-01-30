import unittest
from warnings import warn
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_less
from fluidsht.sht2d.operators import OperatorsSphereHarmo2D


def as_iterable(args):
    if isinstance(args, np.ndarray):
        return (args,)
    else:
        return args


class TestOperators2D(unittest.TestCase):
    sht_class = "default"

    @classmethod
    def setUpClass(cls):
        """Setup operator with default SHT class and parameters
        such that no truncation occurs.

        """
        lmax = 15
        cls.oper = oper = OperatorsSphereHarmo2D(
            nlat=lmax + 1, nlon=2 * lmax + 1, lmax=lmax, sht=cls.sht_class
        )
        cls.arrays_spat = [oper.create_array_spat(1.0) for i in range(2)]
        cls.arrays_sh = [oper.create_array_sh_random() for i in range(2)]
        for array in cls.arrays_sh:
            array[np.logical_not(oper.where_l2_idx_positive)] = 0.0

    def assert_reversible(self, arrays_in, forward, inverse):
        try:
            forward = getattr(self.oper, forward)
        except AttributeError:
            warn(forward, "not implemented!")
            return
        try:
            inverse = getattr(self.oper, inverse)
        except AttributeError:
            warn(inverse, "not implemented!")
            return

        arrays_transformed = forward(*as_iterable(arrays_in))
        arrays_out = inverse(*as_iterable(arrays_transformed))

        assert_array_almost_equal(arrays_in, arrays_out)

    def test_not0(self):
        """Arrays which are expected to have small values when :math:`l(l+1) == 0`."""
        oper = self.oper
        COND = oper.l2_idx == 0
        for attr in ("K2_not0", "inv_K2_not0", "inv_K2_r"):
            array = getattr(oper, attr)
            try:
                assert_array_less(array[COND], 1e-14)
            except AssertionError:
                raise AssertionError(
                    f"Array {attr} is non-negligible where it should be."
                )

    def test_transform_vec_vsh(self):
        self.assert_reversible(self.arrays_spat, "vsh_from_vec", "vec_from_vsh")

    def test_transform_vsh_divrotsh(self):
        self.assert_reversible(
            self.arrays_sh, "divrotsh_from_vsh", "vsh_from_divrotsh"
        )

    def test_transform_vec_divrotsh(self):
        self.assert_reversible(
            self.arrays_spat, "divrotsh_from_vec", "vec_from_divrotsh"
        )

    def test_sht_isht(self):
        self.assert_reversible(self.arrays_spat[0], "sht", "isht")

    def test_laplacian_invlaplacian(self):
        self.assert_reversible(
            self.arrays_sh[0], "laplacian_sh", "invlaplacian_sh"
        )


@unittest.SkipTest
class TestOperators2DWithSHTOOLS(TestOperators2D):
    sht_class = "sht2d._try_with_shtools"


if __name__ == "__main__":
    unittest.main()
