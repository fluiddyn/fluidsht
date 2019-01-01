import numpy as np
from fluidpythran import boost
from .. import create_sht_object
from ..compat import cached_property

# pythran import numpy as np
Af = "float64[:]"
Ac = "complex128[:]"


def get_simple_2d_method():
    try:
        import shtns

        sht = "sht2d.with_shtns"
    except ImportError:
        # sht = "sht2d.with_shtools"
        raise NotImplementedError

    return sht


@boost
class OperatorsSphereHarmo2D:
    r"""Perform 2D FFT and operations on data.

    Parameters
    ----------

    nlat : int

      Global dimension over the theta-axis (?? dimension for the real arrays).

    nlon : int

      Global dimension over the phi-axis (?? dimension for the real arrays).

    lmax : int

      Truncation degree

    sht: str or SHT classes

      Name of module or string characterizing a method. It has to correspond to a
      module of fluidsht. The first part "fluidsht." of the module "path" can be
      omitted.

    Notes
    -----
    Class attributes and their equivalent mathematical definitions

    .. math::

        l2_idx = l(l+1)
        K2 = \frac{l(l+1)}{r^2} = -\Del
        K2_r = K2 \times r = \frac{l(l+1)}{r}
        inv_K2_r = K2_r^{-1} = \frac{r}{l(l+1)}

    where, `:math:\Del := Laplacian operator`.
    """
    nlm: int
    K2_r: Af
    inv_K2_r: Af

    def __init__(
        self, nlat=None, nlon=None, lmax=15, norm="fourpi", flags=0,
        sht=None
    ):
        if sht is None or sht == "default":
            sht = get_simple_2d_method()

        if isinstance(sht, str):
            if any([sht.startswith(s) for s in ["fluidsht.", "sht2d."]]):
                opsht = create_sht_object(
                    sht, nlat, nlon, lmax=lmax, norm=norm, flags=flags
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
            "nlm",
            "l2_idx",  # l(l+1)
            "radius",
            "K2",
            "K2_not0",
        ):
            self.copyattr(attr)

        self.lmax = lmax
        self.norm = norm
        self.flags = flags

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
            "vec_from_divsh",
            "vec_from_rotsh",
            "vec_from_divrotsh",
            "vsh_from_vec",
            "divrotsh_from_vec",
            "gradf_from_fsh",
        ):
            self.copyattr(method)

    @cached_property
    def K2_r(self):
        return self.l2_idx / self.radius

    @cached_property
    def inv_K2_r(self):
        inv_K2_r = 1.0 / (self.radius * self.K2_not0)
        # inv_K2_r[0] = 0.0
        return inv_K2_r

    @cached_property
    def where_l2_idx_positive(self):
        return self.l2_idx > 0

    def copyattr(self, attr):
        setattr(self, attr, getattr(self.opsht, attr))

    # FIXME: default arguments does not work
    # @boost
    def divrotsh_from_vsh(
        self, uD_lm: Ac, uR_lm: Ac, div_lm: Ac = None, rot_lm: Ac = None
    ):
        if div_lm is None:
            # div_lm = self.create_array_sh()
            div_lm = np.empty(self.nlm, complex)

        if rot_lm is None:
            # rot_lm = self.create_array_sh()
            rot_lm = np.empty(self.nlm, complex)

        div_lm[:] = -self.K2_r * uD_lm
        rot_lm[:] = self.K2_r * uR_lm
        return div_lm, rot_lm

    # FIXME: default arguments does not work
    # @boost
    def vsh_from_divrotsh(
        self, div_lm: Ac, rot_lm: Ac, uD_lm: Ac = None, uR_lm: Ac = None
    ):
        if uD_lm is None:
            # uD_lm = self.create_array_sh()
            uD_lm = np.empty(self.nlm, complex)

        if uR_lm is None:
            # uR_lm = self.create_array_sh()
            uR_lm = np.empty(self.nlm, complex)

        uD_lm[:] = -div_lm * self.inv_K2_r
        uR_lm[:] = rot_lm * self.inv_K2_r
        return uD_lm, uR_lm