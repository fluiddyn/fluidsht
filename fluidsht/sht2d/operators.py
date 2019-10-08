"""Operators 2D (:mod:`fluidfft.sht2d.operators`)
=================================================

.. autoclass:: OperatorsSphereHarmo2D
   :members:
   :undoc-members:

"""
from contextlib import suppress
import numpy as np
from transonic import boost
from .. import create_sht_object
from ..compat import cached_property


Af = "float64[:]"
Ac = "complex128[:]"
Ac_optional = "complex128[:] or None"


def get_simple_2d_method() -> str:
    """Easily select an available SHT library. Used by the operators class when
    ``sht="default"`` is specified.

    """
    try:
        import shtns

        sht = "sht2d.with_shtns"
    except ImportError:
        # sht = "sht2d.with_shtools"
        raise NotImplementedError

    return sht


@boost
class OperatorsSphereHarmo2D:
    r"""Perform 2D SHT and operations on data.

    Parameters
    ----------

    nlat : int

      Global dimension over the theta-axis (?? dimension for the real arrays).

    nlon : int

      Global dimension over the phi-axis (?? dimension for the real arrays).

    lmax : int

      Truncation degree.

    norm : str

      Normalization for SHT transforms. See ``options_norm`` in the respective
      modules for available options.

    cs_phase : bool

      Disable (default) or enables the Condon-Shortley phase factor to the
      associated Legendre functions;

    radius : float

      Radius of the sphere

    sht: str or SHT classes

      Name of module or string characterizing a method. It has to correspond to a
      module of fluidsht. The first part "fluidsht." of the module "path" can be
      omitted.

    Notes
    -----
    Some of the class attributes and their equivalent mathematical definitions

    .. math::

        \texttt{l2_idx} &= l(l+1) \\
        \texttt{K2} &= \frac{l(l+1)}{r^2} &= -\Delta \\
        \texttt{K2_r} &= \texttt{K2} \times r &= \frac{l(l+1)}{r} \\
        \texttt{inv_K2_r} &= \texttt{K2_r}^{-1} &= \frac{r}{l(l+1)}

    where, :math:`\Delta = \nabla^2 :=` Laplacian operator.
    """
    nlm: int
    K2: Af
    inv_K2_not0: Af
    K2_r: Af
    inv_K2_r: Af

    def __init__(
        self,
        nlat=None,
        nlon=None,
        lmax=15,
        norm="orthonormal",
        cs_phase=False,
        grid_type="gaussian",
        radius=1,
        sht=None,
    ):
        if sht is None or sht == "default":
            sht = get_simple_2d_method()

        if isinstance(sht, str):
            if any([sht.startswith(s) for s in ["fluidsht.", "sht2d."]]):
                opsht = create_sht_object(
                    sht,
                    nlat,
                    nlon,
                    lmax=lmax,
                    norm=norm,
                    cs_phase=False,
                    grid_type=grid_type,
                    radius=radius,
                )
                print(f"{sht}: nlat={opsht.nlat}, nlon={opsht.nlon}")
            else:
                raise ValueError(
                    (
                        "Cannot instantiate %s. Expected something like "
                        "'default', 'fluidsht.sht2d.<method>' or "
                        "'sht2d.<method>'"
                    )
                    % sht
                )

        self.opsht = opsht
        self.type_sht = opsht.__class__.__module__

        for attr in (
            "nlat",
            "nlon",
            "lats",
            "lons",
            "LATS",
            "LONS",
            "deltax",
            "deltay",  # FIXME: deltay
            "shapeX",
            "shapeX_loc",
            "shapeX_seq",
            "shapeK",
            "shapeK_loc",
            "shapeK_seq",
            "nlm",
            "l2_idx",  # l(l+1)
            "radius",
            "K2",
            "K4",
            "K8",
            "K2_not0",
            "_zeros_sh",
        ):
            self.copyattr(attr)

        # for fluidsim plotting
        self.x_seq = self.lons
        self.y_seq = self.lats

        self.lmax = lmax
        self.norm = norm
        self.cs_phase = cs_phase
        self.grid_type = grid_type

        for method in (
            # Initialization methods
            "create_array_spat",
            "create_array_spat_random",
            "create_array_sh",
            "create_array_sh_random",
            # Generic transformations
            "sht",
            "isht",
            "sht_as_arg",
            "isht_as_arg",
            # Velocity vector <-> Spherical Harmonics transformations methods
            "vec_from_vsh",
            "vsh_from_vec",
            # Gradient
            "gradf_from_fsh",
            # Misc.
            "dealiasing",  # FIXME: Implement properly
            # Post-processing
            "sum_wavenumbers",
            # Informational
            "produce_str_describing_oper",
            "produce_long_str_describing_oper",
        ):
            self.copyattr(method)

    @cached_property
    def inv_K2_not0(self):
        inv_K2_not0 = 1.0 / self.K2_not0
        inv_K2_not0[self.l2_idx == 0] = 0.0
        return inv_K2_not0

    @cached_property
    def K2_r(self):
        r"""Compute :math:`r \Delta = [l(l+1)] / r`"""
        return self.l2_idx / self.radius

    @cached_property
    def inv_K2_r(self):
        r"""Compute :math:`(r \Delta)^{-1} = r / [l(l+1)]`"""
        return self.inv_K2_not0 / self.radius

    @cached_property
    def where_l2_idx_positive(self):
        return self.l2_idx > 0

    def copyattr(self, attr):
        """Copies attributes / methods from ``opsht`` instance."""
        # For short term development.
        # To be removed when the backends are the same.
        with suppress(AttributeError):
            setattr(self, attr, getattr(self.opsht, attr))

    @boost
    def laplacian_sh(self, a_lm: Ac, negative: bool = False):
        r"""Compute the Laplacian, :math:`\nabla^{n} a^{lm}`

        Parameters
        ----------
        a_lm : ndarray

        negative: bool, optional
            Negative of the result.

        """
        if negative:
            return self.K2 * a_lm
        else:
            return -self.K2 * a_lm

    @boost
    def invlaplacian_sh(self, a_lm: Ac, negative: bool = False):
        r"""Compute the Laplacian, :math:`\nabla^{n} a^{lm}`

        Parameters
        ----------
        a_lm : ndarray

        negative: bool, optional
            Negative of the result.

        """
        if negative:
            return self.inv_K2_not0 * a_lm
        else:
            return -self.inv_K2_not0 * a_lm

    @boost
    def divrotsh_from_vsh(
        self,
        uD_lm: Ac,
        uR_lm: Ac,
        div_lm: Ac_optional = None,
        rot_lm: Ac_optional = None,
    ):
        """Compute divergence and curl from vector spherical harmonics uD, uR
        (``div_lm`` and ``rot_lm`` are overwritten).

        """
        if div_lm is None:
            # div_lm = self.create_array_sh()
            div_lm = np.empty(self.nlm, complex)

        if rot_lm is None:
            # rot_lm = self.create_array_sh()
            rot_lm = np.empty(self.nlm, complex)

        div_lm[:] = -self.K2_r * uD_lm
        rot_lm[:] = self.K2_r * uR_lm
        return div_lm, rot_lm

    @boost
    def vsh_from_divrotsh(
        self,
        div_lm: Ac,
        rot_lm: Ac,
        uD_lm: Ac_optional = None,
        uR_lm: Ac_optional = None,
    ):
        """Compute VSH from divergence and curl spherical harmonics ``div_lm``,
        ``rot_lm`` (``uD_lm`` and ``uR_lm`` are overwritten).

        """
        if uD_lm is None:
            # uD_lm = self.create_array_sh()
            uD_lm = np.empty(self.nlm, complex)

        if uR_lm is None:
            # uR_lm = self.create_array_sh()
            uR_lm = np.empty(self.nlm, complex)

        uD_lm[:] = -div_lm * self.inv_K2_r
        uR_lm[:] = rot_lm * self.inv_K2_r
        return uD_lm, uR_lm

    def vec_from_divrotsh(self, div_lm, rot_lm, u=None, v=None):
        """Velocities u, v from horizontal divergence, and vertical vorticity
        (u and v are overwritten).

        """
        if u is None:
            u = self.create_array_spat()
        if v is None:
            v = self.create_array_spat()

        uD_lm, uR_lm = self.vsh_from_divrotsh(div_lm, rot_lm)
        return self.vec_from_vsh(uD_lm, uR_lm, u, v)

    def vec_from_rotsh(self, rot_sh, u=None, v=None):
        """Velocities u, v from vertical vorticity alone (u and v are
        overwritten).

        """
        return self.vec_from_divrotsh(self._zeros_sh, rot_sh, u, v)

    def vec_from_divsh(self, div_sh, u=None, v=None):
        """Velocities u, v from horizontal divergence alone (u and v are
        overwritten).

        """
        return self.vec_from_divrotsh(div_sh, self._zeros_sh, u, v)

    def divrotsh_from_vec(self, u, v, div_lm=None, rot_lm=None):
        """Compute horizontal divergence, and vertical vorticity from u, v
        (div_lm and rot_lm are overwritten).

        """
        if div_lm is None:
            div_lm = self.create_array_sh()
        if rot_lm is None:
            rot_lm = self.create_array_sh()

        # Reuse arrays
        uD_lm = div_lm
        uR_lm = rot_lm

        self.vsh_from_vec(u, v, uD_lm, uR_lm)
        return self.divrotsh_from_vsh(
            uD_lm, uR_lm, div_lm, rot_lm  # Inputs  # Buffers to be overwritten
        )
