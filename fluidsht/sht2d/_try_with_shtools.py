"""Class using SHTOOLS (:mod:`fluidsht.sht2d.with_shtools`)
===========================================================

.. autoclass:: SHT2DWithSHTOOLS
   :members:

"""
from collections import namedtuple
from functools import partial
from warnings import warn

import numpy as np
from pyshtools import shtools


Normalization = namedtuple(
    "normalization", ("orthonormal", "fourpi", "schmidt", "unnormalized"))
options_norm = Normalization(
    4, 1, 2, 3
    # "ortho", "4pi", "schmidt", "unnorm"
)
# Condon-Shortley phase factor to the associated Legendre functions
Flags = namedtuple(
    "flags",
    ("csphase", "no_csphase")
)
options_flags = Flags(-1, 1)



class SHT2DWithSHTOOLS:

    def __init__(
        self,
        nlat=None,
        nlon=None,
        lmax=15,
        norm=None,
        grid_type="gaussian",
        flags=options_flags.no_csphase,
    ):
        self.norm = norm if norm else options_norm.fourpi
        self.flags = flags
        self.grid_type = grid_type

        if grid_type == "gaussian":
            self._zeros, self._weights = shtools.SHGLQ(lmax)
            self._sht = shtools.SHExpandGLQ
            self._isht = shtools.MakeGridGLQ
            # TODO: implement lmax_calc to allow truncation
            if nlat:
                assert nlat == lmax + 1

            self.nlat = lmax + 1

            if nlon:
                assert nlon == 2 * lmax + 1

            self.nlon = 2 * lmax + 1

            self.lats, self.lons = shtools.GLQGridCoord(lmax)
        else:
            raise NotImplementedError

        self.LONS, self.LATS = np.meshgrid(self.lons, self.lats)

    def sht(self, field):
        return self._sht(
            field,
            w=self._weights,
            zero=self._zeros,
            norm=self.norm,
            csphase=self.flags
        )

    def isht(self, field_sh):
        return self._isht(
            field_sh,
            zero=self._zeros,
            norm=self.norm,
            csphase=self.flags
        )