"""Class using SHTOOLS (:mod:`fluidsht.sht2d.with_shtools`)
===========================================================

.. autoclass:: SHT2DWithSHTOOLS
   :members:

"""
from collections import namedtuple
import functools
from warnings import warn

import numpy as np
from pyshtools import shtools
from ..compat import cached_property

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
        if not nlat or not nlon:
            warn("Truncation not implemented yet")
        self.lmax = lmax
        if grid_type == "gaussian":
            # Fortran function aliases
            self._sht = shtools.SHExpandGLQC
            self._isht = shtools.MakeGridGLQC
            self._make_grid_coeffs = shtools.SHGLQ
            self.set_grid = shtools.GLQGridCoord

            # TODO: implement lmax_calc to allow truncation
            if nlat:
                assert nlat == lmax + 1
            self.nlat = lmax + 1

            if nlon:
                assert nlon == 2 * lmax + 1
            self.nlon = 2 * lmax + 1
        else:
            raise NotImplementedError
        
        # TODO: implement the rest using getattr and dictionary 
        if norm == options_norm.fourpi:
            self._Pl = shtools.PlBar
            self._Pl_d1 = shtools.PlBar_d1
            self._Plm = shtools.PlmBar
            self._Plm_d1 = shtools.PlmBar_d1

        self.shapeX = (self.nlat, self.nlon)
        self.lats, self.lons = self.set_grid(lmax)
        self.LONS, self.LATS = np.meshgrid(self.lons, self.lats)

        self.nlm = (lmax + 1) * (lmax + 2) // 2
        self.shapeK = (self.nlm,)
        # self.l2_idx = 

    @cached_property
    def _grid_coeffs(self):
        zeros, weights = self._make_grid_coeffs(self.lmax)
        return (zeros, weights)

    def create_array_sh(self, value=None, dtype=complex):
        """Create an array representing a field in spectral space."""
        if value is None:
            field_lm = np.empty(self.nlm, dtype)
        elif value == "rand":
            field_lm = np.random.randn(self.nlm) + 1.j * np.random.randn(self.nlm)
        elif value == 0:
            field_lm = np.zeros(self.nlm, dtype)
        else:
            field_lm = value * np.ones(self.nlm, dtype)
        return field_lm

    def create_array_spat(self, value=None):
        """Create an array representing a field in spatial space."""
        if value is None:
            field = np.empty(self.shapeX)
        elif value == "rand":
            field = np.random.randn(self.nlat, self.nlon)
        elif value == 0:
            field = np.zeros(self.shapeX)
        else:
            field = value * np.ones(self.shapeX)
        # a spatial array matching a grid build with SHT_PHI_CONTIGUOUS
        return field

    def sht(self, field):
        """Forward transform from spatial grid to spherical harmonics (analysis)."""
        zeros, weights = self._grid_coeffs
        return self._sht(
            field,
            w=weights,
            zero=zeros,
            norm=self.norm,
            csphase=self.flags
        )

    def isht(self, field_sh):
        """Inverse transform from spherical harmonics to spatial grid (sythesis)."""
        zeros = self._grid_coeffs[0]
        return self._isht(
            field_sh,
            zero=zeros,
            norm=self.norm,
            csphase=self.flags
        ).real

    create_array_spat_random = functools.partialmethod(
        create_array_spat, "rand"
    )
    create_array_sh_random = functools.partialmethod(
        create_array_sh, "rand"
    )

SHTclass = SHT2DWithSHTOOLS