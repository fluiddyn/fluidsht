import numpy as np
from fluidpythran import boost
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
    """Perform 2D FFT and operations on data.

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

    """
    nlm: int
    K2_r: Af
    inv_K2_r: Af

    def __init__(
        self, nlat=None, nlon=None, lmax=15, norm="fourpi", flags=None,
        sht=None
    ):
        self.nlat = nlat
        self.nlon = nlon
        self.lmax = lmax
        self.norm = norm
        self.flags = flags

        if sht is None or sht == "default":
            sht = get_simple_2d_method()

        if isinstance(sht, str):
            if any([sht.startswith(s) for s in ["fluidsht.", "sht2d."]]):
                opsht = create_sht_object(sht, nlat, nlon, lmax)
            else:
                raise ValueError(
                    (
                        "Cannot instantiate %s. Expected something like "
                        "'sequential', 'fluidsht.sht2d.<method>' or "
                        "'sht2d.<method>'"
                    )
                    % sht
                )

        self.opsht = opsht
        self.type_sht = opsht.__class__.__module__

        self.sht = self.opsht.sht
        self.isht = self.opsht.isht

        self.sht_as_arg = opsht.sht_as_arg
        self.isht_as_arg = opsht.isht_as_arg


    @cached_property
    def K2_r(self):
        return self.l2_idx / self.radius

    @cached_property
    def inv_K2_r(self):
        inv_K2_r = self.radius / self.K2_not0
        inv_K2_r[0] = 0.0
        return inv_K2_r

    @boost
    def hdivrotsh_from_uDuRsh(
        self, uD_lm: Ac, uR_lm: Ac, hdiv_lm: Ac = None, hrot_lm: Ac = None
    ):
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
    def uDuRsh_from_hdivrotsh(
        self, hdiv_lm: Ac, hrot_lm: Ac, uD_lm: Ac = None, uR_lm: Ac = None
    ):
        if uD_lm is None:
            # uD_lm = self.create_array_sh()
            uD_lm = np.empty(self.nlm, complex)

        if uR_lm is None:
            # uR_lm = self.create_array_sh()
            uR_lm = np.empty(self.nlm, complex)

        uD_lm[:] = -hdiv_lm * self.inv_K2_r
        uR_lm[:] = hrot_lm * self.inv_K2_r
        return uD_lm, uR_lm

