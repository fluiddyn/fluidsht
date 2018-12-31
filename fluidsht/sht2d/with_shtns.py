"""Class using SHTns (:mod:`fluidsht.sht2d.with_shtns`)
=========================================================

.. autoclass:: SHT2DWithSHTns
   :members:

"""
import functools
# to get a clear ImportError in case...
import shtns

from fluiddyn.calcul.sphericalharmo import EasySHT, radius_earth
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


class SHT2DWithSHTns(EasySHT):
    __doc__ = EasySHT.__doc__

    def __init__(
        self,
        nlat=None,
        nlon=None,
        lmax=15,
        mmax=None,
        mres=1,
        norm=None,
        flags=None,
        polar_opt=1.0e-8,
        nl_order=2,
        radius=1, # radius_earth,
    ):
        super().__init__(
            lmax, mmax, mres, norm, nlat, nlon, flags, polar_opt, nl_order, radius
        )

    # functions for 2D vectorial spherical harmonic transforms

    def set_grid(self, grid_type="gaussian"):
        nlat = self.nlat
        nlon = self.nlon

        if grid_type == 'gaussian':
            self.sh.set_grid(
                nlat,
                nlon,
            #    options_flags.gauss_fly | options_flags.phi_contiguous,
                options_flags.quick_init | options_flags.phi_contiguous,
                1.e-10
            )
        elif grid_type == 'regular':
            self.sh.set_grid(
                nlat,
                nlon,
                options_flags.reg_dct | options_flags.phi_contiguous,
                1.e-10
            )

    def vec_from_divrotsh(self, div_lm, rot_lm, u=None, v=None):
        """Velocities u, v from horizontal divergence, and vertical vorticity
        (u and v are overwritten).

        """
        if u is None:
            u = self.create_array_spat()
            v = self.create_array_spat()
        # uD_lm = self.create_array_sh(0.0)
        # uR_lm = self.create_array_sh(0.0)

        # Reuse arrays
        uD_lm = u
        uR_lm = v

        self.uDuRsh_from_divrotsh(div_lm, rot_lm, uD_lm, uR_lm)
        self.sh.SHsphtor_to_spat(uD_lm, uR_lm, v, u)
        return u, v

    def vec_from_rotsh(self, rot_sh):
        return self.vec_from_divrotsh(self._zeros_sh, rot_sh)

    def vec_from_divsh(self, div_sh):
        return self.vec_from_divrotsh(div_sh, self._zeros_sh)

    def divrotsh_from_vec(self, u, v, div_lm=None, rot_lm=None):
        """Compute horizontal divergence, and vertical vorticity from u, v
        (div_lm and rot_lm are overwritten).

        """
        if div_lm is None:
            div_lm = self.create_array_sh()
            rot_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     v = -v
        # print('order_lat',self.order_lat)
        self.sh.spat_to_SHsphtor(v, u, div_lm, rot_lm)
        # in fact there is uD_lm in div_lm and
        #                  uR_lm in rot_lm
        # we compute div_lm and rot_lm
        return self.divrotsh_from_vsh(
            uD_lm=div_lm,
            uR_lm=rot_lm,  # Inputs
            div_lm=div_lm,
            rot_lm=rot_lm,  # Buffers to be overwritten
        )

    def vec_from_vsh(self, uD_lm, uR_lm, u=None, v=None):
        """Compute velocities u, v from vector spherical harmonics uD, uR (u and v
        are overwritten).

        """
        if u is None:
            u = self.create_array_spat()
            v = self.create_array_spat()
        self.sh.SHsphtor_to_spat(uD_lm, uR_lm, v, u)

        # if self.order_lat == 'south_to_north':
        #    v[:] = -v+0       # because SHTns uses colatitude basis

        return u, v

    def vsh_from_vec(self, u, v, uD_lm=None, uR_lm=None):
        """Compute vector spherical harmonics uD_lm, uR_lm from from velocities u,
        v (uD_lm and uR_lm are overwritten).

        Note
        ----
        `Vector spherical harmonics (VSH)
        <https://en.wikipedia.org/wiki/Vector_spherical_harmonics>`__ in 2D are in
        fact equivalent to Helholtz decomposition as it is represented by a
        divergent and rotational components as transformed quantities.

        """
        if uD_lm is None:
            uD_lm = self.create_array_sh()

        if uR_lm is None:
            uR_lm = self.create_array_sh()

        # if self.order_lat == 'south_to_north':
        #     v = -v
        # print('order_lat', self.order_lat)
        self.sh.spat_to_SHsphtor(v, u, uD_lm, uR_lm)
        # remove minus
        uD_lm[:] = -uD_lm[:]
        uR_lm[:] = -uR_lm[:]
        # print(self.radius)
        return uD_lm, uR_lm

    def gradf_from_fsh(self, f_lm, gradf_lon=None, gradf_lat=None):
        """Compute the gradient of a function f from its spherical
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
        #    sign_inv_v = -1
        # else:
        #    sign_inv_v = 1
        # sign_inv_v = 1
        gradf_lat[:] = +gradf_lat / self.radius  # *sign_inv_v
        gradf_lon[:] = +gradf_lon / self.radius
        # print('radius', self.radius)
        return gradf_lon, gradf_lat

    # Method aliases
    divrotsh_from_vsh = EasySHT.hdivrotsh_from_uDuRsh
    vsh_from_divrotsh = EasySHT.uDuRsh_from_hdivrotsh
    create_array_spat_random = functools.partialmethod(
        EasySHT.create_array_spat, "rand"
    )
    create_array_sh_random = functools.partialmethod(
        EasySHT.create_array_sh, "rand"
    )


SHTclass = SHT2DWithSHTns
