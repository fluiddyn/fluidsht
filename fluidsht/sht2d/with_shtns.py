"""Class using SHTns (:mod:`fluidsht.sht2d.with_shtns`)
=========================================================

.. autoclass:: SHT2DWithSHTns
   :members:

"""
import numpy as np
# to get a clear ImportError in case...
import shtns

from fluiddyn.calcul.sphericalharmo import EasySHT, radius_earth
from fluidpythran import boost
from fluidsht.util import make_namedtuple_from_module


keys_norm = ("orthonormal", "fourpi", "schmidt")

keys_flags = (
    "gauss",
    "auto",
    "reg_fast",
    "reg_dct",
    "quick_init",
    "reg_poles",
    "gauss_fly",
    "theta_contiguous",
    "phi_contiguous",
    "no_cs_phase",
    "real_norm",
    "scalar_only",
    "south_pole_first",
)

options_norm = make_namedtuple_from_module(
    shtns, "sht_{}", "normalization", keys_norm
)

options_flags = make_namedtuple_from_module(shtns, "sht_{}", "flags", keys_flags)

# pythran import numpy as np

Af = "float64[:]"
Ac = "complex128[:]"

@boost
class OperatorsSphereHarmo2D:
    nlm: int
    K2_r: Af
    inv_K2_r: Af

    @boost
    def hdivrotsh_from_uDuRsh(self, uD_lm: Ac, uR_lm: Ac, hdiv_lm: Ac=None, hrot_lm: Ac=None):
        if hdiv_lm is None:
            # hdiv_lm = self.create_array_sh()
            hdiv_lm = np.empty(self.nlm, complex)

        if hrot_lm is None:
            # hrot_lm = self.create_array_sh()
            hrot_lm = np.empty(self.nlm, complex)

        hdiv_lm[:] = -self.K2_r * uD_lm
        hrot_lm[:] = self.K2_r * uR_lm
        return hdiv_lm, hrot_lm

    @boost
    def uDuRsh_from_hdivrotsh(self, hdiv_lm: Ac, hrot_lm: Ac, uD_lm: Ac=None, uR_lm: Ac=None):
        if uD_lm is None:
            # uD_lm = self.create_array_sh()
            uD_lm = np.empty(self.nlm, complex)

        if uR_lm is None:
            # uR_lm = self.create_array_sh()
            uR_lm = np.empty(self.nlm, complex)

        uD_lm[:] = -hdiv_lm * self.inv_K2_r
        uR_lm[:] = hrot_lm * self.inv_K2_r
        return uD_lm, uR_lm


# FIXME: @boost
class SHT2DWithSHTns(EasySHT):
    __doc__ = EasySHT.__doc__

    def __init__(
        self,
        lmax=15,
        mmax=None,
        mres=1,
        norm=None,
        nlat=None,
        nlon=None,
        flags=None,
        polar_opt=1.0e-8,
        nl_order=2,
        radius=radius_earth,
    ):
        super().__init__(
             lmax, mmax, mres, norm, nlat, nlon, flags, polar_opt, nl_order, radius
        )
        self.K2_r = self.l2_idx / self.radius
        self.inv_K2_r = self.radius / self.K2_not0
        self.inv_K2_r[0] = 0.
        pass

    # functions for 2D vectorial spherical harmonic transforms

    def uv_from_hdivrotsh(self, hdiv_lm, hrot_lm, u=None, v=None):
        """Velocities u, v from horizontal divergence, and vertical vorticity
        (u and v are overwritten).

        """
        if uu is None:
            uu = self.create_array_spat()
            vv = self.create_array_spat()
        uD_lm = self.create_array_sh(0.)
        uR_lm = self.create_array_sh(0.)
        self.uDuRsh_from_hdivrotsh(hdiv_lm, hrot_lm, uD_lm, uR_lm)
        self.sh.SHsphtor_to_spat(uD_lm, uR_lm, vv, uu)
        return uu, vv

    def hdivrotsh_from_uv(self, uu, vv, hdiv_lm=None, hrot_lm=None):
        """Compute horizontal divergence, and vertical vorticity from u, v
        (div_lm and rot_lm are overwritten).

        """
        if hdiv_lm is None:
            hdiv_lm = self.create_array_sh()
            hrot_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     vv = -vv
        # print('order_lat',self.order_lat)
        self.sh.spat_to_SHsphtor(vv, uu, hdiv_lm, hrot_lm)
        # in fact there is uD_lm in hdiv_lm and
        #                  uR_lm in hrot_lm
        # we compute div_lm and rot_lm
        return self.hdivrotsh_from_uDuRsh(
            uD_lm=hdiv_lm, uR_lm=hrot_lm,  # Inputs
            hdiv_lm=hdiv_lm, hrot_lm=hrot_lm  # Buffers to be overwritten
        )

    def uv_from_uDuRsh(self, uD_lm, uR_lm, uu=None, vv=None):
        """Compute velocities uu, vv from uD, uR (uu and vv are overwritten).

        """
        if uu is None:
            uu = self.create_array_spat()
            vv = self.create_array_spat()
        self.sh.SHphtor_to_spat(uD_lm, uR_lm, vv, uu)

        # if self.order_lat == 'south_to_north':
        #    vv[:] = -vv+0       # because SHTns uses colatitude basis

        return uu, vv

    def uDuRsh_from_uv(self, uu, vv, uD_lm=None, uR_lm=None):
        """Compute helmholtz decomposition of the velocities from uu, vv.
        (uD_lm and uR_lm are overwritten).

        """
        if uD_lm is None:
            uD_lm = self.create_array_sh()

        if uR_lm is None:
            uR_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     vv = -vv
        # print('order_lat', self.order_lat)
        self.sh.spat_to_SHsphtor(vv, uu, uD_lm, uR_lm)
        # removed minus
        uD_lm[:] = -uD_lm[:]
        uR_lm[:] = -uR_lm[:]
        # print(self.radius)
        return uD_lm, uR_lm

    def gradf_from_fsh(self, f_lm, gradf_lon=None, gradf_lat=None):
        """gradf from fsh.

        Compute the gradient of a function f from its spherical
        harmonic coeff f_lm (gradf_lon and gradf_lat are overwritten)

        """
        if gradf_lon is None:
            gradf_lon = self.create_array_spat(0)
            gradf_lat = self.create_array_spat(0)  # becareful bug if not 0!!!
        #       We do not use SHsph_to_spat() because it seems that there is a 
        #       problem (av: what exactly? does it still exist?)
        #       self.sh.SHsph_to_spat(f_lm, gradf_lat, gradf_lon)
        #       instead we use SHsphtor_to_spat(...) with tor_lm= zeros_lm
        # zeros_lm = self.create_array_sh(0.)
        self.sh.SHsphtor_to_spat(f_lm, self._zeros_sh, gradf_lat, gradf_lon)

        # if self.order_lat == 'south_to_north':
        #    sign_inv_vv = -1
        # else:
        #    sign_inv_vv = 1
        # sign_inv_vv = 1
        gradf_lat[:] = +gradf_lat / self.radius  # *sign_inv_vv
        gradf_lon[:] = +gradf_lon / self.radius
        # print('radius', self.radius)
        return gradf_lon, gradf_lat


SHTclass = SHT2DWithSHTns
